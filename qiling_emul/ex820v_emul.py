"""
Script to emulate the TP-Link EX820v router
"""

from pathlib import Path
from socket import AF_UNIX, SOCK_STREAM, socket
from threading import Thread, Event

from qiling import Qiling
from qiling.const import QL_VERBOSE

running_event = Event()
running_event.set()


def patcher(ql):
    """
    Docstring
    """
    br0_addr = ql.mem.search("br0".encode("utf-8") + b"\x00")
    for addr in br0_addr:
        ql.mem.write(addr, b"lo\x00")


def nvram_listener():
    """
    Docstring
    """
    server_address: Path = Path("squashfs-root/var/cfm_socket")
    data = ""

    try:
        server_address.unlink()
    except OSError:
        if server_address.exists():
            raise

    # Create UDS socket
    sock = socket(AF_UNIX, SOCK_STREAM)
    sock.bind(str(server_address))
    sock.listen(1)

    while running_event.is_set():
        connection, _ = sock.accept()
        try:
            while running_event.is_set():
                data += str(connection.recv(1024).decode("utf-8", errors="ignore"))

                if "lan.webiplansslen" in data:
                    connection.send(
                        "192.168.170.169".encode("utf-8")
                    )  # TODO Figure out what IP to replace this with
                elif "wan_ifname" in data:
                    connection.send("eth0".encode("utf-8"))
                elif "wan_ifnames" in data:
                    connection.send("eth0".encode("utf-8"))
                elif "wan0_ifname" in data:
                    connection.send("eth0".encode("utf-8"))
                elif "wan0_ifnames" in data:
                    connection.send("eth0".encode("utf-8"))
                elif "sys.workmode" in data:
                    connection.send("bridge".encode("utf-8"))
                elif "wan1.ip" in data:
                    connection.send("1.1.1.1".encode("utf-8"))
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
    ql.hook_address(patcher, ql.loader.elf_entry)
    ql.run()


if __name__ == "__main__":
    nvram_listener_thread = Thread(target=nvram_listener, daemon=True)
    nvram_listener_thread.start()
    my_sandbox(["squashfs-root/bin/httpd"], "squashfs-root")
    running_event.clear()
    nvram_listener_thread.join()
