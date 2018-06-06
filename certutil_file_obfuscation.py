# Name: Certutil Endcode / Decode
# RTA: certutil_file_obfuscation.py
# ATT&CK: T1140
# Description: Uses certutil to create an encoded copy of cmd.exe. Then uses certutil to decode that copy.

import common
import os


def main():
    common.log("Encoding target")
    encoded_file = os.path.abspath('encoded.txt')
    decoded_file = os.path.abspath('decoded.exe')
    common.execute("c:\\Windows\\System32\\certutil.exe -encode c:\\windows\\system32\\cmd.exe \"%s\"" % encoded_file)

    common.log("Decoding target")
    common.execute("c:\\Windows\\System32\\certutil.exe -decode \"%s\" \"%s\"" % (encoded_file, decoded_file))

    common.log("Cleaning up")
    common.remove_file(encoded_file)
    common.remove_file(decoded_file)


if __name__ == "__main__":
    exit(main())
