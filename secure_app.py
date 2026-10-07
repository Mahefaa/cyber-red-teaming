from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<body>
    <h2>Login (Secured)</h2>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p style="color:green;">{{ message }}</p>
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
        
        # SECURE: Using parameterized queries
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        if user:
            message = f"Welcome, {user[1]}! Authentication successful."
        else:
            message = "Invalid credentials."
        conn.close()
            
    return render_template_string(HTML_TEMPLATE, message=message)

if __name__ == '__main__':
    print("[*] Starting Secured App on http://127.0.0.1:5001")
    app.run(debug=False, port=5001)
