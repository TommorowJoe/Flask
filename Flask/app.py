from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# база данных SQLite
conn = sqlite3.connect('site.db')
cursor = conn.cursor()

# Тут таблица
cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INT PRIMARY KEY, message TEXT NOT NULL)''')
conn.commit()

@app.route('/')
def index():
# Получение сообщений из базы данных
    cursor.execute('SELECT  *  FROM messages ORDER BY id DESC LIMIT 10')
    messages = cursor.fetchall()
    return render_template('index.html', messages=messages)

@app.route('/post', methods=['POST'])
def post_message():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    message = request.form['message']
    cursor.execute('INSERT INTO messages (id, message) VALUES (?, ?)', (None, message))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return '<h1>Login Failed</h1>'
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <button type="submit">Login</button>
        </form>'''

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


