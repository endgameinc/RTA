# Name: Invalid Process Trees in Windows
# rta: unusual_parent.py
# ATT&CK: T1093
# Description: Runs several Windows core processes directly, instead of from the proper parent in Windows.

import common
import os
import sys


def main():
    common.log("Running Windows processes with an unexpected parent of %s" % os.path.basename(sys.executable))
    process_names = [
        # "C:\\Windows\\System32\\smss.exe", BSOD (avoid this)
        # "C:\\Windows\\System32\\csrss.exe", BSOD (avoid this)
        # "C:\\Windows\\System32\\wininit.exe", BSOD (avoid this)
        # "C:\\Windows\\System32\\services.exe", BSOD (avoid this)
        "C:\\Windows\\System32\\winlogon.exe",
        "C:\\Windows\\System32\\lsass.exe",
        "C:\\Windows\\System32\\taskhost.exe",  # Win7
        "C:\\Windows\\System32\\svchost.exe",
    ]

    for process in process_names:
        # taskhostw.exe isn't on all versions of windows
        if os.path.exists(process):
            common.execute([process], timeout=2, kill=True)
        else:
            common.log("Skipping %s" % process, "-")


if __name__ == "__main__":
    exit(main())
