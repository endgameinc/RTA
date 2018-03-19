# Name: Unexpected Network Activity from Microsoft Tools
# RTA: findstr_pw_search.py
# ATT&CK: T1127
# Description: Creates network traffic from a process which is named to match common administration and developer tools
#              that do not typically make network traffic unless being used maliciously.

import os
import shutil
import sys
import common

process_names = [
    "bginfo.exe",
    "rcsi.exe",
    "control.exe",
    "odbcconf.exe"
]


def http_from_process(name, ip, port):
    path = os.path.join(common.BASE_DIR, name)
    common.log("Making HTTP GET from %s" % path)
    shutil.copy(sys.executable, path)
    common.execute([path, "-c", "import urllib; urllib.urlopen('http://%s:%d')" % (ip, port)])
    common.remove_file(path)


def main():
    server, ip, port = common.serve_web()

    for process in process_names:
        http_from_process(process, ip, port)

    server.shutdown()


if __name__ == "__main__":
    exit(main())
