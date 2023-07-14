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
        return render_template('customerSide/index.html', blogs=blogs)
    cur.close()
    return render_template('customerSide/index.html', blogs=None)


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/location/')
def location():
    return render_template('customerSide/location.html')

@app.route('/reservation/<int:id>')
def reservation(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM vehicle WHERE vehicle_ID = '{id}'"
    cur.execute(query)
    vehicle = cur.fetchall()
    cur.close()

    return render_template('customerSide/reservation.html', cars=vehicle)

@app.route('/maintenance/<int:id>')
def maintenance(id):
    vehicle_id = request.args.get('vehicle_ID')

    cur = mysql.connection.cursor()
    query = "SELECT * FROM vehicle_maintenance_history WHERE vehicle_ID = %s"
    cur.execute(query, (vehicle_id,))
    vehicle = cur.fetchall()
    cur.close()

    return render_template('customerSide/maintenance.html', cars=vehicle)

@app.route('/vehicle/')
def vehicle():
    return render_template('customerSide/vehicle.html')

@app.route('/appointment/', methods=['GET', 'POST'])
def appointment():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        resultValue =  cur.execute("SELECT * FROM location")
        print(resultValue)
        if resultValue > 0:
            locations = cur.fetchall()
            cur.close()
            return render_template('customerSide/appointment.html', locations=locations)
    elif request.method == 'POST':
        formDetail = request.form
        if session['login'] != True:
            return redirect('/login')
        else:
            l1 = session['id']
            l2 = formDetail['location_ID']
            l3 = formDetail['appointment_date']
            l4 = formDetail['appointment_time']
            l5 = formDetail['appointment_request']
            
            queryStatement = (
                f"INSERT INTO "
                f"appointment(customer_ID, location_ID, appointment_date, appointment_time, appointment_request)"
                f"VALUES('{l1}', '{l2}', '{l3}', '{l4}', '{l5}')"
            )
            cur = mysql.connection.cursor()
            cur.execute(queryStatement)
            mysql.connection.commit()
            flash("Form Submitted Successfully.", "success")
            cur.close()
            return render_template("customerSide/index.html")
    return render_template('customerSide/appointment.html')

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


@app.route('/test/', methods=['GET', 'POST'])
def test():
    return render_template('customerSide/test.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('customerSide/register.html')
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
        cur.close()
        flash("Form Submitted Successfully.", "success")
        return redirect('/login/')    
    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        user = loginForm['customer_email']
        if ("@admin.co.th" in user):
            cur = mysql.connection.cursor()
            queryStatement = f"SELECT * FROM admin WHERE admin_email = '{user}'"
            numRow = cur.execute(queryStatement)
            if numRow > 0:
                user =  cur.fetchone()
                if check_password_hash(user['admin_password'], loginForm['customer_password']):

                # Record session information
                    session['login'] = True
                    session['email'] = user['admin_email']
                    session['firstName'] = user['admin_firstname']
                    session['lastName'] = user['admin_lastname']
                    session['dob'] = user['admin_dob']
                    session['gender'] = user['admin_gender']
                    session['Phone_number'] = user['admin_phonenumber']
                    session['address'] = user['admin_address']
                    session['id'] = user['admin_ID']
                    flash('Welcome ' + session['firstName'], 'success')
                #flash("Log In successful",'success')
                    return render_template('adminSide/adminIndex.html')
                else:
                    cur.close()
                flash("Password doesn't not match", 'danger')
            else:
                cur.close()
                flash('User not found', 'danger')
                return render_template('login.html')
        else:
            cur = mysql.connection.cursor()
            queryStatement = f"SELECT * FROM customer WHERE customer_email = '{user}'"
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
    try:
        user = session['login']
    except:
        flash('Please sign in first', 'danger')
        return redirect('/login')
    
    if session['login'] != True:
        return redirect('/register')
    else:
        cur = mysql.connection.cursor()
        query = f"SELECT * FROM appointment WHERE customer_ID = '{session['id']}'"
        cur.execute(query)
        appointments = cur.fetchall()
        cur.close()
    return render_template('customerSide/profile.html', appointments=appointments, )

@app.route('/adminhome/')
def adminhome():
    cur = mysql.connection.cursor()

    # Retrieve data from customer table
    cur.execute("SELECT * FROM customer")
    customers = cur.fetchall()

    # Retrieve data from vehicle table
    cur.execute("SELECT * FROM vehicle")
    vehicles = cur.fetchall()

    # Retrieve data from location table
    cur.execute("SELECT * FROM location")
    locations = cur.fetchall()

    # Retrieve data from appointment table
    cur.execute("SELECT * FROM appointment")
    appointments = cur.fetchall()

    # Retrieve data from review table
    cur.execute("SELECT * FROM review")
    reviews = cur.fetchall()

    # Retrieve data from rental table
    cur.execute("SELECT * FROM rental")
    rentals = cur.fetchall()

    # Retrieve data from transaction table
    cur.execute("SELECT * FROM transaction")
    transactions = cur.fetchall()

    # Retrieve data from report table
    cur.execute("SELECT * FROM report")
    reports = cur.fetchall()

    # Retrieve data from payment table
    cur.execute("SELECT * FROM payment")
    payments = cur.fetchall()

    # Retrieve data from vehicle_maintenance_history table
    cur.execute("SELECT * FROM vehicle_maintenance_history")
    maintenance_history = cur.fetchall()
    
    # Retrieve data from admin table
    cur.execute("SELECT * FROM admin")
    admin = cur.fetchall()

    cur.close()
    return render_template('adminSide/adminhome.html', customers=customers, vehicles=vehicles, locations=locations,
                           appointments=appointments, reviews=reviews, rentals=rentals, transactions=transactions,
                           reports=reports, payments=payments, maintenance_history=maintenance_history, admin=admin)




@app.route('/admin/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'GET':
        return render_template('adminSide/add_customer.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        customer_firstname = form_details['customer_firstname']
        customer_lastname = form_details['customer_lastname']
        customer_dob = form_details['customer_dob']
        customer_gender = form_details['customer_gender']
        customer_email = form_details['customer_email']
        customer_phone_number = form_details['customer_phone_number']
        customer_address = form_details['customer_address']
        customer_identification_number = form_details['customer_identification_number']
        customer_passport = form_details['customer_passport']
        customer_payment_type = form_details['customer_payment_type']
        customer_payment_card_number = form_details['customer_payment_card_number']
        customer_payment_card_cvc = form_details['customer_payment_card_cvc']
        customer_payment_card_exp = form_details['customer_payment_card_expiry_date']
        customer_password = form_details['customer_password']

        # Hash the password
        hashed_password = generate_password_hash(customer_password)

        # Save the customer details to the database
        cur = mysql.connection.cursor()
        query = (
            "INSERT INTO customer "
            "(customer_firstname, customer_lastname, customer_dob, customer_gender, customer_email, customer_phone_number, "
            "customer_address, customer_identification_number, customer_passport, customer_payment_type, "
            "customer_payment_card_number, customer_payment_card_cvc, customer_payment_card_expiry_date, customer_password) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        values = (
            customer_firstname, customer_lastname, customer_dob, customer_gender, customer_email, customer_phone_number,
            customer_address, customer_identification_number, customer_passport, customer_payment_type,
            customer_payment_card_number, customer_payment_card_cvc, customer_payment_card_exp, hashed_password
        )
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        flash("Customer added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminside/add_customer.html')

@app.route('/admin/add_admin', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'GET':
        return render_template('adminside/add_admin.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        admin_firstname = form_details['admin_firstname']
        admin_lastname = form_details['admin_lastname']
        admin_dob = form_details['admin_dob']
        admin_gender = form_details['admin_gender']
        admin_email = form_details['admin_email']
        admin_phonenumber = form_details['admin_phonenumber']
        admin_address = form_details['admin_address']
        admin_appointment_count = form_details['admin_appointment_count']
        admin_password = form_details['admin_password']

        # Save the admin details to the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO admin (admin_firstname, admin_lastname, admin_dob, admin_gender, admin_email, admin_phonenumber, admin_address, admin_appointment_count, admin_password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (admin_firstname, admin_lastname, admin_dob, admin_gender, admin_email, admin_phonenumber, admin_address, admin_appointment_count, admin_password))
        mysql.connection.commit()
        cur.close()

        flash("Admin added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminSide/add_admin.html')


@app.route('/admin/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'GET':
        return render_template('adminSide/add_location.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        location_country = form_details['location_country']
        location_state = form_details['location_state']
        location_city = form_details['location_city']
        location_address = form_details['location_address']
        location_name = form_details['location_name']

        # Save the location details to the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO location (location_country, location_state, location_city, location_address, location_name) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (location_country, location_state, location_city, location_address, location_name))
        mysql.connection.commit()
        cur.close()

        flash("Location added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminSide/add_location.html')


@app.route('/admin/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'GET':
        return render_template('adminside/add_appointment.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        customer_ID = form_details['customer_ID']
        location_ID = form_details['location_ID']
        appointment_date = form_details['appointment_date']
        appointment_time = form_details['appointment_time']
        appointment_request = form_details['appointment_request']

        # Save the appointment details to the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO appointment (customer_ID, location_ID, appointment_date, appointment_time, appointment_request) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (customer_ID, location_ID, appointment_date, appointment_time, appointment_request))
        mysql.connection.commit()
        cur.close()

        flash("Appointment added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminside/add_appointment.html')


@app.route('/admin/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'GET':
        return render_template('adminside/add_vehicle.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        location_ID = form_details['location_ID']
        vehicle_type = form_details['vehicle_type']
        vehicle_brand = form_details['vehicle_brand']
        vehicle_model = form_details['vehicle_model']
        vehicle_color = form_details['vehicle_color']
        vehicle_gasoline_type = form_details['vehicle_gasoline_type']
        vehicle_license_plate = form_details['vehicle_license_plate']
        vehicle_insured = form_details.get('vehicle_insured') == 'on'  # Convert checkbox value to boolean
        vehicle_insurance_expiry = form_details['vehicle_insurance_expiry']
        vehicle_condition = form_details['vehicle_condition']
        vehicle_milage = form_details['vehicle_milage']
        vehicle_passenger = form_details['vehicle_passenger']
        vehicle_gear_type = form_details['vehicle_gear_type']
        vehicle_available = form_details.get('vehicle_available') == 'on'  # Convert checkbox value to boolean
        vehicle_price_per_day = form_details['vehicle_price_per_day']

        # Save the vehicle details to the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO vehicle (location_ID, vehicle_type, vehicle_brand, vehicle_model, vehicle_color, vehicle_gasoline_type, vehicle_license_plate, vehicle_insured, vehicle_insurance_expiry, vehicle_condition, vehicle_milage, vehicle_passenger, vehicle_gear_type, vehicle_available, vehicle_price_per_day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (location_ID, vehicle_type, vehicle_brand, vehicle_model, vehicle_color, vehicle_gasoline_type, vehicle_license_plate, vehicle_insured, vehicle_insurance_expiry, vehicle_condition, vehicle_milage, vehicle_passenger, vehicle_gear_type, vehicle_available, vehicle_price_per_day))
        mysql.connection.commit()
        cur.close()

        flash("Vehicle added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminside/add_vehicle.html')



@app.route('/admin/add_review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'GET':
        return render_template('adminside/add_review.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        vehicle_ID = form_details['vehicle_ID']
        customer_ID = form_details['customer_ID']
        review_content = form_details['review_content']
        review_date_time = form_details['review_date_time']
        review_value_for_money = form_details['review_value_for_money']
        review_easy_to_find = form_details['review_easy_to_find']
        review_drop_off_speed = form_details['review_drop_off_speed']
        review_pick_up_speed = form_details['review_pick_up_speed']
        review_car_cleanliness = form_details['review_car_cleanliness']
        review_helpfulness = form_details['review_helpfulness']
        review_car_condition = form_details['review_car_condition']

        # Save the review details to the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO review (vehicle_ID, customer_ID, review_content, review_date_time, review_value_for_money, review_easy_to_find, review_drop_off_speed, review_pick_up_speed, review_car_cleanliness, review_helpfulness, review_car_condition) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (vehicle_ID, customer_ID, review_content, review_date_time, review_value_for_money, review_easy_to_find, review_drop_off_speed, review_pick_up_speed, review_car_cleanliness, review_helpfulness, review_car_condition))
        mysql.connection.commit()
        cur.close()

        flash("Review added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminside/add_review.html')


@app.route('/admin/add_rental', methods=['GET', 'POST'])
def add_rental():
    if request.method == 'GET':
        return render_template('adminside/add_rental.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        customer_ID = form_details['customer_ID']
        vehicle_ID = form_details['vehicle_ID']
        location_ID = form_details['location_ID']
        admin_ID = form_details['admin_ID']
        rental_loan_date = form_details['rental_loan_date']
        rental_return_date = form_details['rental_return_date']
        rental_loan_time = form_details['rental_loan_time']
        rental_return_time = form_details['rental_return_time']
        rental_total_payment = form_details['rental_total_payment']

        # Save the rental details to the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO rental (customer_ID, vehicle_ID, location_ID, admin_ID, rental_loan_date, rental_return_date, rental_loan_time, rental_return_time, rental_total_payment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (customer_ID, vehicle_ID, location_ID, admin_ID, rental_loan_date, rental_return_date, rental_loan_time, rental_return_time, rental_total_payment))
        mysql.connection.commit()
        cur.close()

        flash("Rental added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminside/add_rental.html')


@app.route('/admin/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'GET':
        return render_template('adminside/add_transaction.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        customer_ID = form_details['customer_ID']
        vehicle_ID = form_details['vehicle_ID']
        rental_ID = form_details['rental_ID']
        admin_ID = form_details['admin_ID']
        transaction_datetime = form_details['transaction_datetime']

        # Save the transaction details to the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO transaction (customer_ID, vehicle_ID, rental_ID, admin_ID, transaction_datetime) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (customer_ID, vehicle_ID, rental_ID, admin_ID, transaction_datetime))
        mysql.connection.commit()
        cur.close()

        flash("Transaction added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminside/add_transaction.html')


@app.route('/admin/add_report', methods=['GET', 'POST'])
def add_report():
    if request.method == 'GET':
        return render_template('adminside/add_report.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        rental_ID = form_details['rental_ID']
        transaction_ID = form_details['transaction_ID']
        report_datetime = form_details['report_datetime']

        # Save the report details to the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO report (rental_ID, transaction_ID, report_datetime) VALUES (%s, %s, %s)"
        cur.execute(query, (rental_ID, transaction_ID, report_datetime))
        mysql.connection.commit()
        cur.close()

        flash("Report added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminside/add_report.html')


@app.route('/admin/add_payment', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'GET':
        return render_template('adminside/add_payment.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        rental_ID = form_details['rental_ID']
        admin_ID = form_details['admin_ID']
        customer_ID = form_details['customer_ID']
        payment_amount = form_details['payment_amount']
        payment_added_charges = form_details['payment_added_charges']
        payment_datetime = form_details['payment_datetime']

        # Save the payment details to the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO payment (rental_ID, admin_ID, customer_ID, payment_amount, payment_added_charges, payment_datetime) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(query, (rental_ID, admin_ID, customer_ID, payment_amount, payment_added_charges, payment_datetime))
        mysql.connection.commit()
        cur.close()

        flash("Payment added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminside/add_payment.html')


@app.route('/admin/add_vehicle_maintenance', methods=['GET', 'POST'])
def add_vehicle_maintenance():
    if request.method == 'GET':
        return render_template('adminside/add_vehicle_maintenance.html')
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        vehicle_ID = form_details['vehicle_ID']
        maintenance_type = form_details['maintenance_type']
        maintenance_datetime = form_details['maintenance_datetime']
        maintenance_finished = form_details.get('maintenance_finished')

        # Save the vehicle maintenance details to the database
        cur = mysql.connection.cursor()
        query = "INSERT INTO vehicle_maintenance_history (vehicle_ID, maintenance_type, maintenance_datetime, maintenance_finished) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (vehicle_ID, maintenance_type, maintenance_datetime, maintenance_finished))
        mysql.connection.commit()
        cur.close()

        flash("Vehicle maintenance added successfully.", "success")
        return redirect('/adminhome')

    return render_template('adminside/add_vehicle_maintenance.html')


# edit  customer
@app.route('/admin/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM customer WHERE customer_ID = '{id}'"
    cur.execute(query)
    customer = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        return render_template('adminSide/edit_customer.html', customer=customer)
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        customer_firstname = form_details['customer_firstname']
        customer_lastname = form_details['customer_lastname']
        customer_dob = form_details['customer_dob']
        customer_gender = form_details['customer_gender']
        customer_email = form_details['customer_email']
        customer_phone_number = form_details['customer_phone_number']
        customer_address = form_details['customer_address']
        customer_identification_number = form_details['customer_identification_number']
        customer_passport = form_details['customer_passport']
        customer_payment_type = form_details['customer_payment_type']
        customer_payment_card_number = form_details['customer_payment_card_number']
        customer_payment_card_cvc = form_details['customer_payment_card_cvc']
        customer_payment_card_exp = form_details['customer_payment_card_expiry_date']
        customer_password = form_details['customer_password']
        
        hashed_pw = generate_password_hash(customer_password) 
        # Extract other customer details...

        # Update the customer details in the database
        cur = mysql.connection.cursor()
        query = (
                f"UPDATE customer SET customer_firstname = '{customer_firstname}', customer_lastname = '{customer_lastname}',"
                f"    customer_dob = '{customer_dob}', customer_gender = '{customer_gender}', customer_email = '{customer_email}',"
                f"    customer_phone_number = '{customer_phone_number}', customer_address = '{customer_address}',"
                f"    customer_identification_number = '{customer_identification_number}', customer_passport = '{customer_passport}',"
                f"    customer_payment_type = '{customer_payment_type}', customer_payment_card_number = '{customer_payment_card_number}',"
                f"    customer_payment_card_cvc = '{customer_payment_card_cvc}', customer_payment_card_expiry_date = '{customer_payment_card_exp}',"
                f"    customer_password = '{hashed_pw}'"
                f"    WHERE customer_ID = {customer['customer_ID']};"
                )
        
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return redirect('/adminhome')

    return render_template('adminSide/edit_customer.html', customer=customer, flash_message="Customer updated successfully.")

# Edit Admin
@app.route('/admin/edit_admin/<int:id>', methods=['GET', 'POST'])
def edit_admin(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM admin WHERE admin_ID = '{id}'"
    cur.execute(query)
    admin = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        return render_template('adminSide/edit_admin.html', admin=admin)
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        admin_firstname = form_details['admin_firstname']
        admin_lastname = form_details['admin_lastname']
        admin_dob = form_details['admin_dob']
        admin_gender = form_details['admin_gender']
        admin_email = form_details['admin_email']
        admin_phonenumber = form_details['admin_phonenumber']
        admin_address = form_details['admin_address']
        admin_appointment_count = form_details['admin_appointment_count']
        admin_password = form_details['admin_password']

        hashed_pw = generate_password_hash(admin_password)
        # Extract other admin details...

        # Update the admin details in the database
        cur = mysql.connection.cursor()
        query = (
                f"UPDATE admin SET admin_firstname = '{admin_firstname}', admin_lastname = '{admin_lastname}',"
                f"    admin_dob = '{admin_dob}', admin_gender = '{admin_gender}', admin_email = '{admin_email}',"
                f"    admin_phonenumber = '{admin_phonenumber}', admin_address = '{admin_address}',"
                f"    admin_appointment_count = '{admin_appointment_count}', admin_password = '{hashed_pw}'"
                f"    WHERE admin_ID = {admin['admin_ID']};"
                )
        
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return redirect('/adminhome')

    return render_template('adminSide/edit_admin.html', admin=admin, flash_message="Admin updated successfully.")

# Edit Location
@app.route('/admin/edit_location/<int:id>', methods=['GET', 'POST'])
def edit_location(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM location WHERE location_ID = '{id}'"
    cur.execute(query)
    location = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        return render_template('adminSide/edit_location.html', location=location)
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        location_country = form_details['location_country']
        location_state = form_details['location_state']
        location_city = form_details['location_city']
        location_address = form_details['location_address']
        location_name = form_details['location_name']

        # Update the location details in the database
        cur = mysql.connection.cursor()
        query = (
                f"UPDATE location SET location_country = '{location_country}', location_state = '{location_state}',"
                f"    location_city = '{location_city}', location_address = '{location_address}',"
                f"    location_name = '{location_name}'"
                f"    WHERE location_ID = {location['location_ID']};"
                )
        
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return redirect('/adminhome')

    return render_template('adminSide/edit_location.html', location=location, flash_message="Location updated successfully.")

# Edit Vehicle
@app.route('/admin/edit_vehicle/<int:id>', methods=['GET', 'POST'])
def edit_vehicle(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM vehicle WHERE vehicle_ID = '{id}'"
    cur.execute(query)
    vehicle = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        return render_template('adminSide/edit_vehicle.html', vehicle=vehicle)
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        location_ID = form_details['location_ID']
        vehicle_type = form_details['vehicle_type']
        vehicle_brand = form_details['vehicle_brand']
        vehicle_model = form_details['vehicle_model']
        vehicle_color = form_details['vehicle_color']
        vehicle_gasoline_type = form_details['vehicle_gasoline_type']
        vehicle_license_plate = form_details['vehicle_license_plate']
        vehicle_insured = form_details['vehicle_insured']
        vehicle_insurance_expiry = form_details['vehicle_insurance_expiry']
        vehicle_condition = form_details['vehicle_condition']
        vehicle_milage = form_details['vehicle_milage']
        vehicle_passenger = form_details['vehicle_passenger']
        vehicle_gear_type = form_details['vehicle_gear_type']
        vehicle_available = form_details['vehicle_available']
        vehicle_price_per_day = form_details['vehicle_price_per_day']

        # Update the vehicle details in the database
        cur = mysql.connection.cursor()
        query = (
                f"UPDATE vehicle SET location_ID = '{location_ID}', vehicle_type = '{vehicle_type}',"
                f"    vehicle_brand = '{vehicle_brand}', vehicle_model = '{vehicle_model}', vehicle_color = '{vehicle_color}',"
                f"    vehicle_gasoline_type = '{vehicle_gasoline_type}', vehicle_license_plate = '{vehicle_license_plate}',"
                f"    vehicle_insured = '{vehicle_insured}', vehicle_insurance_expiry = '{vehicle_insurance_expiry}',"
                f"    vehicle_condition = '{vehicle_condition}', vehicle_milage = '{vehicle_milage}',"
                f"    vehicle_passenger = '{vehicle_passenger}', vehicle_gear_type = '{vehicle_gear_type}',"
                f"    vehicle_available = '{vehicle_available}', vehicle_price_per_day = '{vehicle_price_per_day}'"
                f"    WHERE vehicle_ID = {vehicle['vehicle_ID']};"
                )
        
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return redirect('/adminhome')

    return render_template('adminSide/edit_vehicle.html', vehicle=vehicle, flash_message="Vehicle updated successfully.")

# Edit Review
@app.route('/admin/edit_review/<int:id>', methods=['GET', 'POST'])
def edit_review(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM review WHERE review_ID = '{id}'"
    cur.execute(query)
    review = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        return render_template('adminSide/edit_review.html', review=review)
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        vehicle_ID = form_details['vehicle_ID']
        customer_ID = form_details['customer_ID']
        review_content = form_details['review_content']
        review_date_time = form_details['review_date_time']
        review_value_for_money = form_details['review_value_for_money']
        review_easy_to_find = form_details['review_easy_to_find']
        review_drop_off_speed = form_details['review_drop_off_speed']
        review_pick_up_speed = form_details['review_pick_up_speed']
        review_car_cleanliness = form_details['review_car_cleanliness']
        review_helpfulness = form_details['review_helpfulness']
        review_car_condition = form_details['review_car_condition']

        # Update the review details in the database
        cur = mysql.connection.cursor()
        query = (
                f"UPDATE review SET vehicle_ID = '{vehicle_ID}', customer_ID = '{customer_ID}',"
                f"    review_content = '{review_content}', review_date_time = '{review_date_time}',"
                f"    review_value_for_money = '{review_value_for_money}', review_easy_to_find = '{review_easy_to_find}',"
                f"    review_drop_off_speed = '{review_drop_off_speed}', review_pick_up_speed = '{review_pick_up_speed}',"
                f"    review_car_cleanliness = '{review_car_cleanliness}', review_helpfulness = '{review_helpfulness}',"
                f"    review_car_condition = '{review_car_condition}'"
                f"    WHERE review_ID = {review['review_ID']};"
                )
        
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return redirect('/adminhome')

    return render_template('adminSide/edit_review.html', review=review, flash_message="Review updated successfully.")

# Edit Rental
@app.route('/admin/edit_rental/<int:id>', methods=['GET', 'POST'])
def edit_rental(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM rental WHERE rental_ID = '{id}'"
    cur.execute(query)
    rental = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        return render_template('adminSide/edit_rental.html', rental=rental)
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        customer_ID = form_details['customer_ID']
        vehicle_ID = form_details['vehicle_ID']
        location_ID = form_details['location_ID']
        admin_ID = form_details['admin_ID']
        rental_loan_date = form_details['rental_loan_date']
        rental_return_date = form_details['rental_return_date']
        rental_loan_time = form_details['rental_loan_time']
        rental_return_time = form_details['rental_return_time']
        rental_total_payment = form_details['rental_total_payment']

        # Update the rental details in the database
        cur = mysql.connection.cursor()
        query = (
                f"UPDATE rental SET customer_ID = '{customer_ID}', vehicle_ID = '{vehicle_ID}',"
                f"    location_ID = '{location_ID}', admin_ID = '{admin_ID}', rental_loan_date = '{rental_loan_date}',"
                f"    rental_return_date = '{rental_return_date}', rental_loan_time = '{rental_loan_time}',"
                f"    rental_return_time = '{rental_return_time}', rental_total_payment = '{rental_total_payment}'"
                f"    WHERE rental_ID = {rental['rental_ID']};"
                )
        
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return redirect('/adminhome')

    return render_template('adminSide/edit_rental.html', rental=rental, flash_message="Rental updated successfully.")

# Edit Transaction
@app.route('/admin/edit_transaction/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM transaction WHERE transaction_ID = '{id}'"
    cur.execute(query)
    transaction = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        return render_template('adminSide/edit_transaction.html', transaction=transaction)
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        customer_ID = form_details['customer_ID']
        vehicle_ID = form_details['vehicle_ID']
        rental_ID = form_details['rental_ID']
        admin_ID = form_details['admin_ID']
        transaction_datetime = form_details['transaction_datetime']

        # Update the transaction details in the database
        cur = mysql.connection.cursor()
        query = (
                f"UPDATE transaction SET customer_ID = '{customer_ID}', vehicle_ID = '{vehicle_ID}',"
                f"    rental_ID = '{rental_ID}', admin_ID = '{admin_ID}', transaction_datetime = '{transaction_datetime}'"
                f"    WHERE transaction_ID = {transaction['transaction_ID']};"
                )
        
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return redirect('/adminhome')

    return render_template('adminSide/edit_transaction.html', transaction=transaction, flash_message="Transaction updated successfully.")

# Edit Report
@app.route('/admin/edit_report/<int:id>', methods=['GET', 'POST'])
def edit_report(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM report WHERE report_ID = '{id}'"
    cur.execute(query)
    report = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        return render_template('adminSide/edit_report.html', report=report)
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        rental_ID = form_details['rental_ID']
        transaction_ID = form_details['transaction_ID']
        report_datetime = form_details['report_datetime']

        # Update the report details in the database
        cur = mysql.connection.cursor()
        query = (
                f"UPDATE report SET rental_ID = '{rental_ID}', transaction_ID = '{transaction_ID}',"
                f"    report_datetime = '{report_datetime}'"
                f"    WHERE report_ID = {report['report_ID']};"
                )
        
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return redirect('/adminhome')

    return render_template('adminSide/edit_report.html', report=report, flash_message="Report updated successfully.")

# Edit Payment
@app.route('/admin/edit_payment/<int:id>', methods=['GET', 'POST'])
def edit_payment(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM payment WHERE payment_ID = '{id}'"
    cur.execute(query)
    payment = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        return render_template('adminSide/edit_payment.html', payment=payment)
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        rental_ID = form_details['rental_ID']
        admin_ID = form_details['admin_ID']
        customer_ID = form_details['customer_ID']
        payment_amount = form_details['payment_amount']
        payment_added_charges = form_details['payment_added_charges']
        payment_datetime = form_details['payment_datetime']

        # Update the payment details in the database
        cur = mysql.connection.cursor()
        query = (
                f"UPDATE payment SET rental_ID = '{rental_ID}', admin_ID = '{admin_ID}',"
                f"    customer_ID = '{customer_ID}', payment_amount = '{payment_amount}',"
                f"    payment_added_charges = '{payment_added_charges}', payment_datetime = '{payment_datetime}'"
                f"    WHERE payment_ID = {payment['payment_ID']};"
                )
        
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return redirect('/adminhome')

    return render_template('adminSide/edit_payment.html', payment=payment, flash_message="Payment updated successfully.")

# Edit Vehicle Maintenance History
@app.route('/admin/edit_vehicle_maintenance_history/<int:id>', methods=['GET', 'POST'])
def edit_vehicle_maintenance_history(id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM vehicle_maintenance_history WHERE vehicle_maintenance_ID = '{id}'"
    cur.execute(query)
    vehicle_maintenance_history = cur.fetchone()
    cur.close()

    if request.method == 'GET':
        return render_template('adminSide/edit_vehicle_maintenance_history.html', vehicle_maintenance_history=vehicle_maintenance_history)
    elif request.method == 'POST':
        form_details = request.form

        # Extract form data
        vehicle_ID = form_details['vehicle_ID']
        maintenance_type = form_details['maintenance_type']
        maintenance_datetime = form_details['maintenance_datetime']
        maintenance_finished = form_details['maintenance_finished']

        # Update the vehicle maintenance history details in the database
        cur = mysql.connection.cursor()
        query = (
                f"UPDATE vehicle_maintenance_history SET vehicle_ID = '{vehicle_ID}', maintenance_type = '{maintenance_type}',"
                f"    maintenance_datetime = '{maintenance_datetime}', maintenance_finished = '{maintenance_finished}'"
                f"    WHERE vehicle_maintenance_ID = {vehicle_maintenance_history['vehicle_maintenance_ID']};"
                )
        
        cur.execute(query)
        mysql.connection.commit()
        cur.close()

        return redirect('/adminhome')

    return render_template('adminSide/edit_vehicle_maintenance_history.html', vehicle_maintenance_history=vehicle_maintenance_history, flash_message="Vehicle maintenance history updated successfully.")

# Delete customer
@app.route('/admin/delete_customer/<int:id>/')
def delete_customer(id):
    cur = mysql.connection.cursor()

    # Delete the customer

    query = f"DELETE FROM customer WHERE customer_ID = {id}"
    cur.execute(query)

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')



# Delete admin
@app.route('/admin/delete_admin/<int:id>', methods=['POST'])
def delete_admin(id):
    cur = mysql.connection.cursor()

    # Delete the customer
    query = f"SET foreign_key_checks = 0"
    cur.execute(query)
    cur.nextset()  

    query = f"DELETE FROM admin WHERE admin_ID = {id}"
    cur.execute(query)
    cur.nextset()  

    query = f"SET foreign_key_checks = 1"
    cur.execute(query)
    cur.nextset()  

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')

@app.route('/admin/delete_location/<int:id>/')
def delete_location(id):
    cur = mysql.connection.cursor()

    # Delete the customer
    query = f"SET foreign_key_checks = 0"
    cur.execute(query)
    cur.nextset()  

    query = f"DELETE FROM location WHERE location_ID = {id}"
    cur.execute(query)
    cur.nextset()  

    query = f"SET foreign_key_checks = 1"
    cur.execute(query)
    cur.nextset()  

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')


# Delete appointment
@app.route('/admin/delete_appointment/<int:id>', methods=['POST'])
def delete_appointment(id):
    cur = mysql.connection.cursor()

    # Delete the customer
    query = f"SET foreign_key_checks = 0"
    cur.execute(query)
    cur.nextset()  

    query = f"DELETE FROM appointment WHERE appointment_ID = {id}"
    cur.execute(query)
    cur.nextset()  

    query = f"SET foreign_key_checks = 1"
    cur.execute(query)
    cur.nextset()  

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')

# Delete vehicle
@app.route('/admin/delete_vehicle/<int:id>', methods=['POST'])
def delete_vehicle(id):
    cur = mysql.connection.cursor()

    # Delete the customer
    query = f"SET foreign_key_checks = 0"
    cur.execute(query)
    cur.nextset()  

    query = f"DELETE FROM vehicle WHERE vehicle_ID = {id}"
    cur.execute(query)
    cur.nextset()  

    query = f"SET foreign_key_checks = 1"
    cur.execute(query)
    cur.nextset()  

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')


# Delete review
@app.route('/admin/delete_review/<int:id>', methods=['POST'])
def delete_review(id):
    cur = mysql.connection.cursor()

    # Delete the customer
    query = f"SET foreign_key_checks = 0"
    cur.execute(query)
    cur.nextset()  

    query = f"DELETE FROM review WHERE review_ID = {id}"
    cur.execute(query)
    cur.nextset()  

    query = f"SET foreign_key_checks = 1"
    cur.execute(query)
    cur.nextset()  

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')


# Delete rental
@app.route('/admin/delete_rental/<int:id>', methods=['POST'])
def delete_rental(id):
    cur = mysql.connection.cursor()

    # Delete the customer
    query = f"SET foreign_key_checks = 0"
    cur.execute(query)
    cur.nextset()  

    query = f"DELETE FROM rental WHERE rental_ID = {id}"
    cur.execute(query)
    cur.nextset()  

    query = f"SET foreign_key_checks = 1"
    cur.execute(query)
    cur.nextset()  

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')

# Delete transaction
@app.route('/admin/delete_transaction/<int:id>', methods=['POST'])
def delete_transaction(id):
    cur = mysql.connection.cursor()

    # Delete the customer
    query = f"SET foreign_key_checks = 0"
    cur.execute(query)
    cur.nextset()  

    query = f"DELETE FROM transaction WHERE transaction_ID = {id}"
    cur.execute(query)
    cur.nextset()  

    query = f"SET foreign_key_checks = 1"
    cur.execute(query)
    cur.nextset()  

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')


# Delete report
@app.route('/admin/delete_report/<int:id>', methods=['POST'])
def delete_report(id):
    cur = mysql.connection.cursor()

    # Delete the customer
    query = f"SET foreign_key_checks = 0"
    cur.execute(query)
    cur.nextset()  

    query = f"DELETE FROM report WHERE report_ID = {id}"
    cur.execute(query)
    cur.nextset()  

    query = f"SET foreign_key_checks = 1"
    cur.execute(query)
    cur.nextset()  

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')


# Delete payment
@app.route('/admin/delete_payment/<int:id>', methods=['POST'])
def delete_payment(id):
    cur = mysql.connection.cursor()

    # Delete the customer
    query = f"SET foreign_key_checks = 0"
    cur.execute(query)
    cur.nextset()  

    query = f"DELETE FROM payment WHERE payment_ID = {id}"
    cur.execute(query)
    cur.nextset()  

    query = f"SET foreign_key_checks = 1"
    cur.execute(query)
    cur.nextset()  

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')


# Delete vehicle maintenance
@app.route('/admin/delete_vehicle_maintenance/<int:id>', methods=['POST'])
def delete_vehicle_maintenance(id):
    cur = mysql.connection.cursor()

    # Delete the customer
    query = f"SET foreign_key_checks = 0"
    cur.execute(query)
    cur.nextset()  

    query = f"DELETE FROM vehicle_maintenance_history WHERE vehicle_maintenance_ID = {id}"
    cur.execute(query)
    cur.nextset()  

    query = f"SET foreign_key_checks = 1"
    cur.execute(query)
    cur.nextset()  

    mysql.connection.commit()
    cur.close()

    flash("Customer deleted successfully.", "success")
    return redirect('/adminhome')



if __name__ == '__main__':
    app.run(
        debug=True
    )