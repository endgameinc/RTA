# Name: msxsl.exe Network
# RTA: msxsl_network.py
# ATT&CK: T1127
# Description: Generates network traffic from msxsl.exe

import common

MS_XSL = common.get_path("bin", "msxsl.exe")
XML_FILE = common.get_path("bin", "customers.xml")
XSL_FILE = common.get_path("bin", "cscript.xsl")


@common.dependencies(MS_XSL, XML_FILE, XSL_FILE)
def main():
    common.log("MsXsl Beacon")
    server, ip, port = common.serve_web()
    common.clear_web_cache()

    new_callback = "http://%s:%d" % (ip, port)
    common.log("Updating the callback to %s" % new_callback)
    common.patch_regex(XSL_FILE, common.CALLBACK_REGEX, new_callback)

    common.execute([MS_XSL, XML_FILE, XSL_FILE])
    server.shutdown()


if __name__ == "__main__":
    exit(main())

