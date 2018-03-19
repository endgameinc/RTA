# Name: Recursive Password Search
# RTA: findstr_pw_search.py
# ATT&CK: T1081
# Description: Recursively searches files looking for the string "password".

import common


def main():
    path = "c:\\"
    common.log("Searching for passwords on %s" % path)
    common.execute("dir %s /s /b | findstr password" % path, shell=True)


if __name__ == "__main__":
    exit(main())
