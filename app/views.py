from app import app
from flask import render_template, request, session
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='root',
    database='epytodo',
)

@app.route('/', methods=['GET'])
def index_route():
    return render_template('home.html',
                            title='Home page',
                            my_content='user')

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    if 'username' in session:
        session.pop('username', None)
        return '<p>Successfuly logged out!</p>'
    else:
        return '<p>You\'re not logged in!</p>'

@app.route('/user', methods=['GET'])
def user():
    if 'username' in session:
        username = session['username']
        return render_template('user.html', my_content=username)
    else:
        return render_template('user.html', my_content="Please log in first.")

@app.route('/signin', methods=['GET', 'POST'])
def user_route():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur = mydb.cursor()
        cur.execute("SELECT * FROM user WHERE username = '%s' AND password = '%s'"%(username, password))
        check = cur.fetchone()
        if check:
            session['username'] = check[0]
            msg = 'Successfuly logged in !'
        elif not username or not password:
            msg = 'Username or password cant be empty!'
        else:
            msg = 'Wrong password/username !'
        cur.close()
    return render_template('signin.html',
                            title='Sign in',
                            msg=msg)

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cur = mydb.cursor()
        cur.execute("SELECT * FROM user WHERE username = '%s' AND password = '%s' AND email = '%s'"%(username, password, email))
        check = cur.fetchone()
        if check:
            msg = 'Account already exists !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cur.execute("INSERT INTO user(username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            mydb.commit()
            msg = 'Sucessfuly register !'
        cur.close()
    elif request.method == 'POST':
        msg = 'Fill out the form !'
    return render_template('register.html',
                            title='Register',
                            msg=msg)