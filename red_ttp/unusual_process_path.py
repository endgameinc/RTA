# Name: Processes in Unusual Paths
# rta: unusual_process_path.py
# ATT&CK: T1158
# Description: Executes processes from the WBEM directory

import os
import common
import sys


def run_from_directory(target_program, directory):
    common.log("Running %s out of %s" % (target_program, directory))

    temp_path = os.path.join(directory, "temp-app.exe")
    common.copy_file(target_program, temp_path)
    common.execute([temp_path])
    common.remove_file(temp_path)


def main(target_program=common.get_path("bin", "myapp.exe")):
    common.log("Processes in Unusual Paths")
    if not common.check_dependencies(target_program):
        return common.MISSING_DEPENDENCIES

    # user tmp
    directories = [
        "C:\\Windows\\system32\\wbem"
    ]

    for directory in directories:
        exists = os.path.exists(directory)
        if not exists:
            os.mkdir(directory)

        run_from_directory(target_program, directory)

        if not exists:
            os.rmdir(directory)


if __name__ == "__main__":
    exit(main(*sys.argv[1:]))
