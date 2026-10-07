import requests
import sys

def dir_brute(url, wordlist):
    print(f"[*] Brute-forcing directories on {url}...")
    for word in wordlist:
        res = requests.get(f"{url}/{word}")
        if res.status_code != 404:
            print(f"[+] Found: /{word} ({res.status_code})")

if __name__ == "__main__":
    dir_brute("http://target.local", ["admin", "login", "config", "backup"])
