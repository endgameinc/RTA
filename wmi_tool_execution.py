# Name: Suspicious execution via WMI
# rta: wmi_tool_execution.py
# ATT&CK: T1047
# Description: Uses the WMI command-line utility to execute built-in Windows commands which are unusual or unexpected.

import common


def main():
    common.log("Executing suspicious processes via WMI")
    command = [
        "cscript.exe",
        "mshta.exe /?",
        "odbcconf.exe",
        "powershell.exe exit'",
    ]

    for command in command:
        common.execute(["wmic.exe", "process", "call", "create", command])

    # kill straggler processes
    common.log("Cleanup stray processes", "-")
    strays = ["odbcconf.exe", "mshta.exe"]
    for stray in strays:
        common.execute(["taskkill.exe", "/f", "/im", stray])


if __name__ == "__main__":
    exit(main())
