# Name: MsBuild with Network Activity
# RTA: msbuild_network.py
# ATT&CK: T1127
# Description: Generates network traffic from msbuild.exe

import re
import common


MS_BUILD = 'C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\msbuild.exe'


@common.dependencies(MS_BUILD)
def main():
    common.log("MsBuild Beacon")
    server, ip, port = common.serve_web()
    common.clear_web_cache()

    common.log("Updating the callback http://%s:%d" % (ip, port))
    target_task = "tmp-file.csproj"
    common.copy_file(common.get_path("bin", "BadTasks.csproj"), target_task)
    new_callback = "http://%s:%d" % (ip, port)
    common.patch_regex(target_task, common.CALLBACK_REGEX, new_callback)

    common.execute([MS_BUILD, target_task])
    common.remove_file(target_task)

    server.shutdown()


if __name__ == "__main__":
    exit(main())
