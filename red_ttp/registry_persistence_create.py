# Name: Registry persistence creation
# rta: registry_persistence_create.py
# ATT&CK: T1015, T1103
# Description: Creates registry persistence for mock malware in Run and RunOnce keys, Services and debuggers.

import _winreg as wreg
import time
import common

TARGET_APP = common.get_path("bin", "myapp.exe")


def pause():
    time.sleep(0.5)


def write_reg_string(hive, key, value, data, delete=True):
    hkey = wreg.CreateKey(hive, key)
    key = key.rstrip('\\')
    common.log("Writing to registry %s\\%s -> %s" % (key, value, data))
    wreg.SetValueEx(hkey, value, 0, wreg.REG_SZ, data)
    stored, code = wreg.QueryValueEx(hkey, value)
    if data != stored:
        common.log("Wrote %s but retrieved %s" % (data, stored), log_type="-")

    if delete:
        pause()
        common.log("Removing %s\\%s" % (key, value), log_type="-")
        wreg.DeleteValue(hkey, value)

    hkey.Close()
    pause()
    print("")


@common.dependencies(TARGET_APP)
def main():
    common.log("Suspicious Registry Persistence")

    for hive in (wreg.HKEY_LOCAL_MACHINE, wreg.HKEY_CURRENT_USER):
        write_reg_string(hive, "Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce\\", "RunOnceTest", TARGET_APP)
        write_reg_string(hive, "Software\\Microsoft\\Windows\\CurrentVersion\\Run\\", "RunTest", TARGET_APP)

    # create Services subkey for "ServiceTest"
    common.log("Creating ServiceTest registry key")
    hkey = wreg.CreateKey(wreg.HKEY_LOCAL_MACHINE, "System\\CurrentControlSet\\Services\\ServiceTest\\")

    # create "ServiceTest" data values
    common.log("Updating ServiceTest metadata")
    wreg.SetValueEx(hkey, "Description", 0, wreg.REG_SZ, "A fake service")
    wreg.SetValueEx(hkey, "DisplayName", 0, wreg.REG_SZ, "ServiceTest Service")
    wreg.SetValueEx(hkey, "ImagePath", 0, wreg.REG_SZ, "c:\\ServiceTest.exe")
    wreg.SetValueEx(hkey, "ServiceDLL", 0, wreg.REG_SZ, "C:\\ServiceTest.dll")

    # modify contents of ServiceDLL and ImagePath
    common.log("Modifying ServiceTest binary")
    wreg.SetValueEx(hkey, "ImagePath", 0, wreg.REG_SZ, "c:\\ServiceTestMod.exe")
    wreg.SetValueEx(hkey, "ServiceDLL", 0, wreg.REG_SZ, "c:\\ServiceTestMod.dll")

    hkey.Close()
    pause()

    # delete Service subkey for "ServiceTest"
    common.log("Removing ServiceTest", log_type="-")
    hkey = wreg.CreateKey(wreg.HKEY_LOCAL_MACHINE, "System\\CurrentControlSet\\Services\\")
    wreg.DeleteKeyEx(hkey, "ServiceTest")

    hkey.Close()
    pause()

    # Additional persistence
    hklm = wreg.HKEY_LOCAL_MACHINE
    common.log("Adding AppInit DLL")
    windows_base = "Software\\Microsoft\\Windows NT\\CurrentVersion\\Windows\\"
    write_reg_string(hklm, windows_base, "AppInit_Dlls", "evil.dll", delete=False)
    write_reg_string(hklm, windows_base, "AppInit_Dlls", "", delete=False)

    hkey.Close()
    pause()

    debugger_targets = ["normalprogram.exe", "sethc.exe", "utilman.exe", "magnify.exe",
                        "narrator.exe", "osk.exe", "displayswitch.exe", "atbroker.exe"]

    for victim in debugger_targets:
        common.log("Registering Image File Execution Options debugger for %s -> %s" % (victim, TARGET_APP))
        base_key = "Software\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\%s" % victim
        write_reg_string(wreg.HKEY_LOCAL_MACHINE, base_key, "Debugger", TARGET_APP, delete=True)


if __name__ == "__main__":
    exit(main())
