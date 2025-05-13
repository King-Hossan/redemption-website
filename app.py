from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# === Database Setup ===
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# === Home Page ===
@app.route('/')
def home():
    return render_template('index.html')

# === Subjects Page ===
@app.route('/subjects')
def subjects():
    return render_template('subjects.html')

# === Math Subject Selection Page ===
@app.route('/math')
def math():
    return render_template('math_selection.html')

# === Grade 9 Mathematics Page ===
@app.route('/grade9math')
def grade_9_math():
    return render_template('grade_9_math.html')

# === Grade 8 Mathematics Page ===
@app.route('/grade8math')
def grade_8_math():
    return render_template('grade_8_math.html')

# === Signup Page ===
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Email already registered."
        finally:
            conn.close()
    return render_template('sign_up.html')

# === Login Page ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()
        if user:
            return redirect(url_for('subjects'))
        else:
            return "Invalid credentials."
    return render_template('login.html')

# === Premium Page ===
@app.route('/premium')
def premium():
    return render_template('premium.html')

# === Initialize DB always, even on deployment ===
init_db()

# === Run Server Locally ===
if __name__ == '__main__':
    app.run()
