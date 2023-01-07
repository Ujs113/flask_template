from flask import Flask, flash, make_response, redirect, render_template, request
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
@app.route('/index')
@app.route('/home')
def home_page():
    user = request.cookies.get('user')
    if user:
        return render_template('index.html', user=user)

    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if user_auth(username, password):
            flash("Login successfull", 'success')
            resp = make_response(redirect('/'))
            resp.set_cookie('user', username)
            return resp
        else:
            flash("Wrong username or password", 'error')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('user')
    return resp

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    conn = sqlite3.connect('./database.db')
    c = conn.cursor()
    query = """
    insert into user values (?, ?)
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = (username, password)
        c.execute(query, user)
        conn.commit()
        resp = make_response(redirect('/login'))
        return resp
    return render_template('signup.html')


def user_auth(username, password):
    conn = sqlite3.connect('./database.db')
    c = conn.cursor()
    c.execute("""
    select * from user
    """)
    users = c.fetchall()
    record = (username, password)
    if record in users:
        return True
    return False

if __name__ == '__main__':
    app.run()