# Name: Emulate Suspect MS Office Child Processes
# RTA: suspect_office_children.py
# ATT&CK: T1064
# Description: Generates various children processes from emulated Office processes.

import common
import os


def main():
    common.log("MS Office unusual child process emulation")
    suspicious_apps = [
        "msiexec.exe /i blah /quiet",
        "powershell.exe exit",
        "wscript.exe //b",
    ]
    cmd_path = "c:\\windows\\system32\\cmd.exe"

    for office_app in ["winword.exe", "excel.exe"]:

        common.log("Emulating %s" % office_app)
        office_path = os.path.abspath(office_app)
        common.copy_file(cmd_path, office_path)

        for command in suspicious_apps:
            common.execute('%s /c %s' % (office_path, command), timeout=5, kill=True)

        common.log('Cleanup %s' % office_path)
        common.remove_file(office_path)


if __name__ == "__main__":
    exit(main())
