"""
Script to emulate the TP-Link EX820v router
"""

import os
import socket
import sys
import threading

sys.path.append("..")
from qiling import Qiling
from qiling.const import QL_VERBOSE


def patcher(ql):
    """"""
    br0_addr = ql.mem.search("br0".encode() + b"\x00")
    for addr in br0_addr:
        ql.mem.write(addr, b"lo\x00")


def nvram_listener():
    """"""
    server_address = "rootfs/var/cfm_socket"
    data = ""

    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise

    # Create UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen(1)

    while True:
        connection, _ = sock.accept()
        try:
            while True:
                data += str(connection.recv(1024))

                if "lan.webiplansslen" in data:
                    connection.send("192.168.170.169".encode())
                elif "wan_ifname" in data:
                    connection.send("eth0".encode())
                elif "wan_ifnames" in data:
                    connection.send("eth0".encode())
                elif "wan0_ifname" in data:
                    connection.send("eth0".encode())
                elif "wan0_ifnames" in data:
                    connection.send("eth0".encode())
                elif "sys.workmode" in data:
                    connection.send("bridge".encode())
                elif "wan1.ip" in data:
                    connection.send("1.1.1.1".encode())
                else:
                    break
                data = ""
        finally:
            connection.close()


def my_sandbox(path, rootfs):
    """ """
    ql: Qiling = Qiling(path, rootfs, verbose=QL_VERBOSE.DEBUG)
    ql.add_fs_mapper("/dev/urandom", "/dev/urandom")
    ql.hook_address(patcher, ql.loader.elf_entry)
    ql.run()


if __name__ == "__main__":
    nvram_listener_therad = threading.Thread(target=nvram_listener, daemon=True)
    nvram_listener_therad.start()
    my_sandbox(["rootfs/bin/httpd"], "rootfs")
