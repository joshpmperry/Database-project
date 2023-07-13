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

@app.route('/reservation/<int:id>')
def reservation(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM vehicle WHERE vehicle_ID = '{id}'"
    cur.execute(query)
    vehicle = cur.fetchall()
    cur.close()

    return render_template('reservation.html', cars=vehicle)

@app.route('/maintenance/<int:id>')
def maintenance(id):
    vehicle_id = request.args.get('vehicle_ID')  # Access the URL parameter

    cur = mysql.connection.cursor()
    query = "SELECT * FROM vehicle_maintenance_history WHERE vehicle_ID = %s"
    cur.execute(query, (vehicle_id,))
    vehicle = cur.fetchall()
    cur.close()

    return render_template('maintenance.html', cars=vehicle)

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

@app.route('/suvarnhabumi/')
def suvarnhabumi():
    cur = mysql.connection.cursor()
    resultValue =  cur.execute("SELECT * FROM vehicle where location_ID = 1")
    print(resultValue)
    if resultValue > 0:
        vehicle = cur.fetchall()
        cur.close()
        return render_template('car.html', cars=vehicle)
    cur.close()
    return render_template('car.html', cars=None)

@app.route('/chiangmai/')
def chiangmai():
    cur = mysql.connection.cursor()
    resultValue =  cur.execute("SELECT * FROM vehicle where location_ID = 2")
    print(resultValue)
    if resultValue > 0:
        vehicle = cur.fetchall()
        cur.close()
        return render_template('car.html', cars=vehicle)
    cur.close()
    return render_template('car.html', cars=None)

@app.route('/phuket/')
def phuket():
    cur = mysql.connection.cursor()
    resultValue =  cur.execute("SELECT * FROM vehicle where location_ID = 3")
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

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        userDetails = request.form
        
        if userDetails['customer_password'] != userDetails['customer_confirm_password']:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        
        p1 = userDetails['customer_firstname']
        p2 = userDetails['customer_lastname']
        p3 = userDetails['customer_dob']
        p4 = userDetails['customer_password']
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

        hashed_pw = generate_password_hash(p4)    
        queryStatement = (
            f"INSERT INTO "
            f"customer(customer_firstname,customer_lastname, customer_dob, customer_password, customer_gender, customer_email, customer_phone_number, customer_address, customer_identification_number, customer_passport, customer_payment_type, customer_payment_card_number, customer_payment_card_cvc, customer_payment_card_expiry_date) "
            f"VALUES('{p1}', '{p2}', '{p3}','{hashed_pw}','{p5}','{p6}','{p7}','{p8}','{p9}','{p10}','{q1}', '{q2}', '{q3}', '{q4}')"
        )
        print(queryStatement)
        cur = mysql.connection.cursor()
        cur.execute(queryStatement)
        mysql.connection.commit()
        flash("Form Submitted Successfully.", "success")
        return redirect('/')    
    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        username = loginForm['customer_email']
        cur = mysql.connection.cursor()
        queryStatement = f"SELECT * FROM customer WHERE customer_email = '{username}'"
        numRow = cur.execute(queryStatement)
        if numRow > 0:
            user =  cur.fetchone()
            if check_password_hash(user['customer_password'], loginForm['customer_password']):

                # Record session information
                session['login'] = True
                session['email'] = user['customer_email']
                session['firstName'] = user['customer_firstname']
                session['lastName'] = user['customer_lastname']
                session['dob'] = user['customer_dob']
                session['gender'] = user['customer_gender']
                session['Phone_number'] = user['customer_phone_number']
                session['address'] = user['customer_address']
                session['id'] = user['customer_ID']
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
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')

@app.route('/profile/')
def profile():
    if session['login'] != True:
        return redirect('/register')
    else:
        cur = mysql.connection.cursor()
        query = f"SELECT * FROM appointment WHERE customer_ID = '{session['id']}'"
        cur.execute(query)
        appointments = cur.fetchall()
        cur.close()
    return render_template('profile.html', appointments=appointments, )

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


@app.route('/adminhome/')
def adminhome():
    cur = mysql.connection.cursor()
    resultValue =  cur.execute("SELECT * FROM vehicle")
    print(resultValue)
    if resultValue > 0:
        blogs = cur.fetchall()
        cur.close()
        return render_template('adminhome.html', blogs=blogs)
    cur.close()
    return render_template('adminhome.html', blogs=None)


@app.route('/admin_vehicle/')
def admin_vehicle():
    cur = mysql.connection.cursor()
    resultValue =  cur.execute("SELECT * FROM vehicle")
    print(resultValue)
    if resultValue > 0:
        vehicle = cur.fetchall()
        cur.close()
        return render_template('car.html', cars=vehicle)
    cur.close()
    return render_template('car.html', cars=None)


if __name__ == '__main__':
    app.run(
        debug=True
    )