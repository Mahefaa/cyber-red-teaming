from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    c.execute('DELETE FROM users')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'supersecret')")
    conn.commit()
    conn.close()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<body>
    <h2>Login (SQLi Lab)</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p style="color:red;">{{ message }}</p>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        # VULNERABLE TO SQL INJECTION
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        
        try:
            c.execute(query)
            user = c.fetchone()
            if user:
                message = f"Welcome, {user[1]}! Authentication successful."
            else:
                message = "Invalid credentials."
        except sqlite3.Error as e:
            message = f"Database Error: {e}"
        finally:
            conn.close()
            
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    init_db()
    print("[*] Starting Vulnerable SQLi Lab on http://127.0.0.1:5000")
    app.run(debug=False, port=5000)
