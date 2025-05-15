from werkzeug.security import generate_password_hash, check_password_hash
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

from flask import render_template

@app.route('/choose_exam')
def choose_exam():
    return render_template('choose_exam.html')

# === Subjects Page ===
@app.route('/subjects')
def subjects():
    return render_template('subjects.html')

@app.route('/exam_paper')
def exam_paper():
    # Optionally get query parameters for grade or exam type
    grade = request.args.get('grade')
    exam = request.args.get('exam')
    return render_template('exam_paper.html', grade=grade, exam=exam)

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
import random
from flask_mail import Message

confirmation_codes = {}  # Store temporarily; use database in production

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        code = str(random.randint(100000, 999999))
        confirmation_codes[email] = {'code': code, 'username': username, 'password': password}

        msg = Message("Redemption Confirmation Code", sender="your_email@gmail.com", recipients=[email])
        msg.body = f"Your confirmation code is: {code}"
        mail.send(msg)

        return redirect(url_for('confirm_email', email=email))
    return render_template('sign_up.html')

#Confirmation Page
@app.route('/confirm_email', methods=['GET', 'POST'])
def confirm_email():
    email = request.args.get('email')
    if request.method == 'POST':
        entered_code = request.form['code']
        actual = confirmation_codes.get(email)

        if actual and entered_code == actual['code']:
            # Save user to DB here
            username = actual['username']
            password = actual['password']  # Hash it before saving

            # TODO: save_user_to_database(username, email, password)

            confirmation_codes.pop(email)  # Remove after success
            flash('Account confirmed! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid confirmation code.', 'danger')

    return render_template('confirm_email.html', email=email)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        raw_password = request.form['password']
        hashed_password = generate_password_hash(raw_password)

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
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
        input_password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[3], input_password):  # user[3] is the hashed password
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

from flask_mail import Mail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # or your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_app_password'  # not your Gmail password

mail = Mail(app)
