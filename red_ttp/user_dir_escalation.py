# Name: SYSTEM Escalation from User Directory
# rta: user_dir_escalation.py
# ATT&CK: T1044
# Description: Spawns mock malware written to a regular user directory and executes as System.

import shutil
import os
import common


@common.dependencies(common.PS_EXEC)
def main():
    # make sure path is absolute for psexec
    status = common.run_system()
    if status is not None:
        return status

    common.log("Run a user-writeable file as system")
    source_path = common.get_path("bin", "myapp.exe")

    target_directory = "c:\\users\\fake_user_rta-%d" % os.getpid()
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    target_path = os.path.join(target_directory, "user_file.exe")
    common.copy_file(source_path, target_path)
    common.execute(target_path)

    common.remove_directory(target_directory)

    
if __name__ == "__main__":
    exit(main())