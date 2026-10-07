import requests
import argparse
import concurrent.futures

def check_path(url, path):
    full_url = f"{url}/{path.strip()}"
    try:
        res = requests.get(full_url, timeout=3)
        if res.status_code in [200, 301, 302, 401, 403]:
            return f"[+] Found: {full_url} (Status: {res.status_code})"
    except requests.exceptions.RequestException:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description="Multi-threaded Directory Brute-forcer")
    parser.add_argument("-u", "--url", required=True, help="Target URL (e.g. http://target.local)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads")
    args = parser.parse_args()

    print(f"[*] Starting Brute-force on {args.url} with {args.threads} threads...")
    
    with open(args.wordlist, 'r') as f:
        paths = f.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(check_path, args.url, p): p for p in paths}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(result)

if __name__ == "__main__":
    main()
