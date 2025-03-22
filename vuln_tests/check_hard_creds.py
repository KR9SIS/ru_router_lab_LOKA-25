"""
Explain vulnerability
"""

from argparse import ArgumentParser

from requests import RequestException, post


def check_for_cred(ip: str):
    """
    Chekcs for the common hardcoded credentials
    """
    print("# Checking for common hardcoded credentials...")

    # TP-Link uses admin as user and admin as passwd
    common_creds = [("admin", "admin"), ("root", "root"), ("admin", "12345")]

    for user, password in common_creds:
        try:
            res = post(
                f"http://{ip}/login",
                data={"username": user, "password": password},
                timeout=5,
            )
            if res:
                # Somtimes routers display "Welcome, Admin". Reason behind welcome
                if "welcome" in res.text.lower():
                    print(f"- *Weak credential found!: {user}:{password}*")

                # Checks for status code 200
                elif res.status_code == 200 and "dashboard" in res.text.lower():
                    print(f"- *Weak credential found!: {user}:{password}*")
            else:
                print(
                    f"- Check for Hardcoded Credentials: {user}:{password}\nError occured, return status: {res.status_code}"
                )
        except RequestException as e:
            print(
                f"- Check for Hardcoded Credentials: {user}:{password}\nRequest raised exception: {e}"
            )

        print()


if __name__ == "__main__":
    parser = ArgumentParser(prog="check_for_cred")
    parser.add_argument("-ip", action="store", type=str)
    args = parser.parse_args()
    check_for_cred(args.ip)
