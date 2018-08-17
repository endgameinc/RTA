import time
import os
import red_ttp.common
import subprocess
import sys


DELAY = 0


def main():
    errors = []
    for ttp_file in red_ttp.get_ttp_list():
        print("---- %s ----" % os.path.basename(ttp_file))
        p = subprocess.Popen([sys.executable, ttp_file], shell=True)
        p.wait()
        code = p.returncode

        if p.returncode:
            errors.append((ttp_file, code))

        time.sleep(DELAY)
        print("")

    return len(errors)


if __name__ == "__main__":
    exit(main())
