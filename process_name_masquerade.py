# Name: Windows Core Process Masquerade
# RTA: process_name_masquerade.py
# ATT&CK: T1036
# Description: Creates several processes which mimic core Windows process names but that are not those executables.

import os
import common

MY_APP = common.get_path("bin", "myapp.exe")


@common.dependencies(MY_APP)
def main():
    masquerades = [
        "svchost.exe",
        "lsass.exe",
        "services.exe",
        "csrss.exe",

    ]

    for name in masquerades:
        path = os.path.abspath(name)
        common.copy_file(MY_APP, path)
        common.execute(path, timeout=3, kill=True)
        common.remove_file(path)


if __name__ == "__main__":
    exit(main())
