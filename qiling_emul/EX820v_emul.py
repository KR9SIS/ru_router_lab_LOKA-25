"""
Script to emulate the TP-Link EX820v router
"""

import socket
from pathlib import Path
from threading import Thread

from qiling import Qiling
from qiling.const import QL_VERBOSE

run = True


def patcher(ql):
    """
    Docstring
    """
    br0_addr = ql.mem.search("br0".encode() + b"\x00")
    for addr in br0_addr:
        ql.mem.write(addr, b"lo\x00")


def nvram_listener():
    """
    Docstring
    """
    server_address: Path = Path("rootfs/var/cfm_socket")
    data = ""

    try:
        server_address.unlink()
    except OSError:
        if server_address.exists():
            raise

    # Create UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(str(server_address))
    sock.listen(1)

    while run:
        connection, _ = sock.accept()
        try:
            while run:
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
    """
    Docstring
    """
    ql: Qiling = Qiling(path, rootfs, verbose=QL_VERBOSE.DEBUG)
    ql.add_fs_mapper("/dev/urandom", "/dev/urandom")
    ql.hook_address(patcher, ql.loader.elf_entry)
    ql.run()


if __name__ == "__main__":
    nvram_listener_thread = Thread(target=nvram_listener, daemon=True)
    nvram_listener_thread.start()
    my_sandbox(["rootfs/bin/httpd"], "rootfs")
    run = False
    nvram_listener_thread.join()
