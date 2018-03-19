import subprocess
import socket
import time
import threading
import SimpleHTTPServer
import binascii
import shutil
import sys
import SocketServer
import re
import os
import getpass
import functools


try:
    HOSTNAME = socket.gethostname().lower()
    LOCAL_IP = socket.gethostbyname(HOSTNAME)
except socket.gaierror:
    LOCAL_IP = "127.0.0.1"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALL_IP = "0.0.0.0"
IP_REGEX = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
CALLBACK_REGEX = r"https?://" + IP_REGEX + r":\d+"
CMD_PATH = os.environ.get("COMSPEC")
USER_NAME = getpass.getuser().lower()

SUCCESS = 0
GENERAL_ERROR = 1
MISSING_DEPENDENCIES = 2
MISSING_PSEXEC = 3
UNSUPPORTED_RTA = 4
ACCESS_DENIED = 5


def check_dependencies(*paths):
    missing = []
    for path in paths:
        if not os.path.exists(path):
            log("Missing dependency %s" % path, "!")
            missing.append(path)
    return len(missing) == 0


def dependencies(*paths):
    missing = []
    for path in paths:
        if not os.path.exists(path):
            missing.append(path)

    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            if len(missing):
                log("Missing dependencies for %s:%s()" % (f.func_code.co_filename, f.func_code.co_name), "!")
                for dep in missing:
                    print("    - %s" % dep)
                return MISSING_DEPENDENCIES
            return f(*args, **kwargs)
        return decorated
    return decorator


def get_path(*path):
    return os.path.join(BASE_DIR, *path)


def execute(command, hide_log=False, mute=False, timeout=30, wait=True, kill=False, drop=False, shell=False):
    """Execute a process and get the output."""
    if isinstance(command, list):
        command = subprocess.list2cmdline([unicode(arg) for arg in command])

    if not hide_log:
        print("%s > %s" % (HOSTNAME, command))

    stdin = subprocess.PIPE
    stdout = subprocess.PIPE
    stderr = subprocess.STDOUT

    if drop or kill:
        devnull = open(os.devnull, "w")
        stdout = devnull
        stderr = devnull

    p = subprocess.Popen(command, stdin=stdin, stdout=stdout, stderr=stderr, shell=shell)

    if kill:
        delta = 0.5
        # Try waiting for the process to die
        for _ in xrange(int(timeout / delta) + 1):
            time.sleep(delta)
            if p.poll() is not None:
                return

        log("Killing process", str(p.pid))
        try:
            p.kill()
            time.sleep(0.5)
        except OSError:
            pass
    elif wait:
        output = ''
        p.stdin.write(os.linesep)
        while p.poll() is None:
            line = p.stdout.readline()
            if line:
                output += line
                if not (hide_log or mute):
                    print(line.rstrip())

        output += p.stdout.read()
        output = output.strip()

        if not (hide_log or mute):
            if p.returncode != 0:
                print("exit code = %d" % p.returncode)
            print("")
        return p.returncode, output
    else:
        return p


def log(message, log_type='+'):
    print('[%s] %s' % (log_type, message))


def copy_file(source, target):
    log('Copying %s -> %s' % (source, target))
    shutil.copy(source, target)


def remove_file(path):
    if os.path.exists(path):
        log('Removing %s' % path, log_type='-')
        os.remove(path)


def remove_directory(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            log('Removing directory %s' % path, log_type='-')
            shutil.rmtree(path)
        else:
            remove_file(path)


def is_64bit():
    return os.environ['PROCESSOR_ARCHITECTURE'] in ('x64', 'AMD64')


def remove_files(*paths):
    for path in paths:
        remove_file(path)


def clear_web_cache():
    log("Clearing temporary files", log_type="-")
    execute(["RunDll32.exe", "InetCpl.cpl,", "ClearMyTracksByProcess", "8"], hide_log=True)
    time.sleep(1)


def serve_web(ip=LOCAL_IP, port=None, directory=BASE_DIR):
    handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    if port is not None:
        server = SocketServer.TCPServer((ip, port), handler)
    else:
        # Otherwise, try to find a port
        for port in xrange(8000, 9000):
            try:
                server = SocketServer.TCPServer((ip, port), handler)
                break
            except socket.error:
                pass

    def server_thread():
        log("Starting web server on http://%s:%d for directory %s" % (ip, port, directory))
        os.chdir(directory)
        server.serve_forever()

    # Start this thread in the background
    thread = threading.Thread(target=server_thread)
    thread.setDaemon(True)
    thread.start()

    time.sleep(0.5)
    return server, ip, port


def patch_file(source_file, old_bytes, new_bytes, target_file=None):
    target_file = target_file or target_file
    log("Patching bytes %s [%s] --> %s [%s]" % (source_file, binascii.b2a_hex(old_bytes),
                                                target_file, binascii.b2a_hex(new_bytes)))

    with open(source_file, "rb") as f:
        contents = f.read()

    patched = contents.replace(old_bytes, new_bytes)

    with open(target_file, "wb") as f:
        f.write(patched)


def patch_regex(source_file, regex, new_bytes, target_file=None):
    target_file = target_file or source_file
    log("Patching by regex %s --> %s" % (source_file, target_file))

    with open(source_file, "rb") as f:
        contents = f.read()

    matches = re.findall(regex, contents)
    log("Changing %s -> %s" % (', '.join(matches), new_bytes))
    contents = re.sub(regex, new_bytes, contents)

    with open(target_file, "wb") as f:
        f.write(contents)


def wchar(s):
    return s.encode('utf-16le')

MAX_HOSTS = 64

def find_remote_host():
    log("Searching for remote Windows hosts")
    _, stdout = execute("net view", hide_log=True)
    hosts = re.findall(r"\\\\([\w\d\._-]+)", stdout)

    # _, current_user = execute("whoami", hide_log=True)
    pending = {}

    log("Discovery %d possible hosts" % len(hosts))
    for name in hosts[:MAX_HOSTS]:
        name = name.lower()
        if name.split('.')[0] == HOSTNAME.split('.')[0]:
            continue

        # log("Checking if %s has remote admin permissions to %s" % (current_user, name))
        dev_null = open(os.devnull, "w")
        p = subprocess.Popen('sc.exe \\\\%s query' % name,
                             stdout=dev_null,
                             stderr=dev_null,
                             stdin=subprocess.PIPE)
        pending[name] = p

    if len(pending) > 0:
        # See which ones return first with a success code, and use that host
        for _ in xrange(20):
            for hostname, pending_process in sorted(pending.items()):
                if pending_process.poll() is None:
                    pending_process.stdin.write(os.linesep)
                if pending_process.returncode == 0:
                    # Now need to get the IP address
                    ip = get_ipv4_address(hostname)
                    if ip is not None:
                        log('Using remote host %s (%s)' % (ip, hostname))
                        return ip
                    pending.pop(hostname)
            time.sleep(0.5)

    log("Unable to find a remote host to pivot to. Using local host %s" % HOSTNAME, log_type="!")
    return LOCAL_IP


def get_ipv4_address(hostname):
    if re.match(IP_REGEX, hostname):
        return hostname

    code, output = execute(["ping", hostname, "-4", "-n", 1], hide_log=True)
    if code != 0:
        return None

    addresses = re.findall(IP_REGEX, output)
    if len(addresses) == 0:
        return None
    return addresses[0]


def find_writeable_directory(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for d in dirs:
            subdir = os.path.join(base_dir, d)
            try:
                test_file = os.path.join(subdir, "test_file")
                f = open(test_file, "w")
                f.close()
                os.remove(test_file)
                return subdir
            except IOError:
                pass


def check_system():
    return USER_NAME == "system" or USER_NAME.endswith("$")


PS_EXEC = get_path("bin", "PsExec.exe")


def run_system(arguments=None):
    if check_system():
        return None

    if arguments is None:
        arguments = [sys.executable, os.path.abspath(sys.argv[0])] + sys.argv[1:]

    log("Attempting to elevate to SYSTEM using PsExec")
    if not os.path.exists(PS_EXEC):
        log("PsExec not found", log_type="-")
        return MISSING_PSEXEC

    code, _ = execute([PS_EXEC, "-w", os.getcwd(), "-accepteula", "-s", "-i"] + arguments)
    if code == 5:
        log("Failed to escalate to SYSTEM", "!")
    return code
