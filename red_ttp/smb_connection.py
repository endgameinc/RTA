# Name: Outbound SMB from a User Process
# rta: smb_connection.py
# ATT&CK: T1105
# Description: Initiates an SMB connection to a target machine, without going through the normal Windows APIs.

import socket
import sys
import common

SMB_PORT = 445


def main(ip=common.LOCAL_IP):
    # connect to rpc
    common.log("Connecting to {}:{}".format(ip, SMB_PORT))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 445))
    common.log("Sending HELLO")
    s.send("HELLO!")
    common.log("Shutting down the conection...")
    s.close()
    common.log("Closed connection to {}:{}".format(ip, SMB_PORT))


if __name__ == "__main__":
    exit(main(*sys.argv[1:]))

