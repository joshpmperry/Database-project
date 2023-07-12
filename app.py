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
    cur = mysql.connection.cursor()
    resultValue =  cur.execute("SELECT * FROM vehicle")
    print(resultValue)
    if resultValue > 0:
        blogs = cur.fetchall()
        cur.close()
        return render_template('index.html', blogs=blogs)
    cur.close()
    return render_template('index.html', blogs=None)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/location/')
def location():
    return render_template('location.html')

@app.route('/reservation/')
def reservation():
    return render_template('reservation.html')

@app.route('/vehicle/')
def vehicle():
    return render_template('vehicle.html')


@app.route('/sedan/')
def sedan():
    cur = mysql.connection.cursor()
    resultValue =  cur.execute("SELECT * FROM vehicle where vehicle_type = 'sedan'")
    print(resultValue)
    if resultValue > 0:
        vehicle = cur.fetchall()
        cur.close()
        return render_template('car.html', cars=vehicle)
    cur.close()
    return render_template('car.html', cars=None)

@app.route('/suv/')
def suv():
    cur = mysql.connection.cursor()
    resultValue =  cur.execute("SELECT * FROM vehicle where vehicle_type = 'suv'")
    print(resultValue)
    if resultValue > 0:
        vehicle = cur.fetchall()
        cur.close()
        return render_template('car.html', cars=vehicle)
    cur.close()
    return render_template('car.html', cars=None)

@app.route('/truck/')
def truck():
    cur = mysql.connection.cursor()
    resultValue =  cur.execute("SELECT * FROM vehicle where vehicle_type = 'suv'")
    print(resultValue)
    if resultValue > 0:
        vehicle = cur.fetchall()
        cur.close()
        return render_template('car.html', cars=vehicle)
    cur.close()
    return render_template('car.html', cars=None)

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/payment/', methods=['GET', 'POST'])
def payment():
    if request.method == 'GET':
        return render_template('paymentpage.html')
    elif request.method == 'POST':
        userDetails = request.form
        
        p1 = userDetails['customer_firstname']
        p2 = userDetails['customer_lastname']
        p3 = userDetails['customer_dob']
        p5 = userDetails['customer_gender']
        p6 = userDetails['customer_email']
        p7 = userDetails['customer_phone_number']
        p8 = userDetails['customer_address']
        p9 = userDetails['customer_identification_number']
        p10 = userDetails['customer_passport']
        
        q1 = userDetails['customer_payment_type']
        q2 = userDetails['customer_payment_card_number']
        q3 = userDetails['customer_payment_card_cvc']
        q4 = userDetails['customer_payment_card_expiry_date']

        queryStatement = (
            f"INSERT INTO "
            f"customer(customer_firstname,customer_lastname, customer_dob, customer_gender, customer_email, customer_phone_number, customer_address, customer_identification_number, customer_passport, customer_payment_type, customer_payment_card_number, customer_payment_card_cvc, customer_payment_card_expiry_date) "
            f"VALUES('{p1}', '{p2}', '{p3}','{p5}','{p6}','{p7}','{p8}','{p9}','{p10}','{q1}', '{q2}', '{q3}', '{q4}')"
        )
        print(queryStatement)
        cur = mysql.connection.cursor()
        cur.execute(queryStatement)
        mysql.connection.commit()
        flash("Form Submitted Successfully.", "success")
        return redirect('/')    
    return render_template('paymentpage.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        username = loginForm['customer_email']
        cur = mysql.connection.cursor()
        queryStatement = f"SELECT * FROM user WHERE username = '{username}'"
        numRow = cur.execute(queryStatement)
        if numRow > 0:
            user =  cur.fetchone()
            if check_password_hash(user['customer_password'], loginForm['customer_password']):

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
    return render_template('paymentpage.html')

@app.route('/my-blogs/')
def my_blogs():
    try:
        username = session['username']
    except:
        flash('Please sign in first', 'danger')
        return redirect('/login')

    cur = mysql.connection.cursor()
    queryStatement = f"SELECT * FROM blog WHERE username = '{username}'"
    print(queryStatement)
    result_value = cur.execute(queryStatement) 
    if result_value > 0:
        my_blogs = cur.fetchall()
        return render_template('my-blogs.html', my_blogs=my_blogs)
    else:
        return render_template('my-blogs.html',my_blogs=None)

if __name__ == '__main__':
    app.run(
        debug=True
    )