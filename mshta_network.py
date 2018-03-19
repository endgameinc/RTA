# Name: Microsoft HTA tool (mshta.exe) with Network Callback
# RTA: mshta_network.py
# ATT&CK: T1170
# Description: Generates network traffic from mshta.exe

import common

HTA_FILE = common.get_path("bin", "beacon.hta")


@common.dependencies(HTA_FILE)
def main():
    # http server will terminate on main thread exit
    # if daemon is True
    common.log("MsHta Beacon")
    server, ip, port = common.serve_web()
    common.clear_web_cache()

    new_callback = "http://%s:%d" % (ip, port)
    common.log("Updating the callback to %s" % new_callback)
    common.patch_regex(HTA_FILE, common.CALLBACK_REGEX, new_callback)

    mshta = 'mshta.exe'
    common.execute([mshta, HTA_FILE], timeout=10, kill=True)
    server.shutdown()


if __name__ == "__main__":
    exit(main())
