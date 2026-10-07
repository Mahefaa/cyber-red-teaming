import sqlite3

def vulnerable_login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # VULNERABLE: Direct string concatenation
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"Executing: {query}")
    
    try:
        cursor.execute(query)
        if cursor.fetchone():
            print("[+] Login Successful (SQLi triggered!)")
        else:
            print("[-] Login Failed")
    except sqlite3.OperationalError as e:
        print(f"[!] DB Error: {e}")

if __name__ == "__main__":
    # Payload: ' OR '1'='1
    print("Testing SQL Injection Payload...")
    vulnerable_login("admin' OR '1'='1", "anything")
