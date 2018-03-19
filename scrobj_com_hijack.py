# Name: COM Hijack via Script Object
# rta: scrobj_com_hijack.py
# ATT&CK: T1122
# Description: Modifies the Registry to create a new user-defined COM broker, "scrobj.dll".

import _winreg as winreg
import common


def main():
    key = "SOFTWARE\\Classes\\CLSID\\{00000000-0000-0000-0000-0000DEADBEEF}\\InprocServer32"
    scrobj = "C:\\WINDOWS\\system32\\scrobj.dll"
    hkey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key)

    common.log("Setting up COM Server registry key")
    winreg.SetValue(hkey, "", winreg.REG_SZ, scrobj)

    common.log("Cleaning up COM Server from registry", log_type="-")
    winreg.DeleteValue(hkey, "")
    winreg.DeleteKey(hkey, "")
    winreg.CloseKey(hkey)
    
    hkey = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Classes\\CLSID")
    winreg.DeleteKey(hkey, "{00000000-0000-0000-0000-0000DEADBEEF}")
    winreg.CloseKey(hkey)


if __name__ == "__main__":
    exit(main())
