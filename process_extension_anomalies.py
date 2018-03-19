# Name: Executable with Unusual Extensions
# RTA: process_extension_anomalies.py
# ATT&CK: T1036
# Description: Creates processes with anomalous extensions

import sys
import common

MY_APP = common.get_path("bin", "myapp.exe")


@common.dependencies(MY_APP)
def main():
    anomalies = [
        "evil.com",
        "bad.pif",
        "evil.cmd",
        "weird.scr"
    ]

    for path in anomalies:
        common.log("Masquerading python as %s" % path)
        common.copy_file(MY_APP, path)
        common.execute([path])
        common.remove_file(path)


if __name__ == "__main__":
    exit(main())
