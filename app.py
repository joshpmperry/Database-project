from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = "Never push this line to github public repo"

cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = cred['mysql_host']
app.config['MYSQL_USER'] = cred['mysql_user']
app.config['MYSQL_PASSWORD'] = cred['mysql_password']
app.config['MYSQL_DB'] = cred['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/blogs/<int:id>/')
def blogs(id):
    return render_template('blogs.html', blog_id = id)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        userDetails = request.form

        # Check the password and confirm password
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')

        p1 = userDetails['first_name']
        p2 = userDetails['last_name']
        p3 = userDetails['username']
        p4 = userDetails['email']
        p5 = userDetails['password']

        hashed_pw = generate_password_hash(p5)
        print(p1 + "," + p2 + "," + p3 + "," + p4 + "," + p5 + "," + hashed_pw)

        queryStatement = (
            f"INSERT INTO "
            f"user(first_name,last_name, username, email, password, role_id) "
            f"VALUES('{p1}', '{p2}', '{p3}', '{p4}','{hashed_pw}', 1)"
        )
        print(check_password_hash(hashed_pw, p5))
        print(queryStatement)
        cur = mysql.connection.cursor()
        cur.execute(queryStatement)
        mysql.connection.commit()
        cur.close()

        flash("Form Submitted Successfully.", "success")
        return redirect('/')    
    return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        username = loginForm['username']
        cur = mysql.connection.cursor()
        queryStatement = f"SELECT * FROM user WHERE username = '{username}'"
        numRow = cur.execute(queryStatement)
        if numRow > 0:
            user =  cur.fetchone()
            if check_password_hash(user['password'], loginForm['password']):

                # Record session information
                session['login'] = True
                session['username'] = user['username']
                session['userroleid'] = str(user['role_id'])
                session['firstName'] = user['first_name']
                session['lastName'] = user['last_name']
                print(session['username'] + " roleid: " + session['userroleid'])
                flash('Welcome ' + session['firstName'], 'success')
                #flash("Log In successful",'success')
                return redirect('/')
            else:
                cur.close()
                flash("Password doesn't not match", 'danger')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login.html')
        cur.close()
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')

@app.route('/write-blog/', methods=['GET', 'POST'])
def write_blog():
    return render_template('write-blog.html')

@app.route('/my-blogs/')
def my_blogs():
    return render_template('my-blogs.html')

@app.route('/edit-blog/<int:id>/', methods=['GET', 'POST'])
def edit_blog(id):
    return render_template('edit-blog.html')

@app.route('/delete-blog/<int:id>/', methods=['POST'])
def delete_blog(id):
    return 'success'


if __name__ == '__main__':
    app.run(debug=True)