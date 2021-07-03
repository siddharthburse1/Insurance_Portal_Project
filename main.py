from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from random import randint
from datetime import timedelta

app = Flask(__name__)

# Secret key for the application to avoid attacks
app.config['SECRET_KEY'] = '79b934dd40d4bfcbb7425bc9277db24ce6b6282dbf12032fecfd321707f9'
app.permanent_session_lifetime = timedelta(minutes=30)

# Setting up database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'insurance_portal'

mysql = MySQL(app)

@app.route("/")
def home():
    return "Home"

@app.route("/registration", methods=["POST", "GET"])
def registration():

    if "customer_name" in session:
        return redirect("/customer-home")

    # Storing regstration details from console into variables
    # console_name = input("Enter Name: ")
    # console_email = input("Enter Email: ")
    # console_password = input("Enter Password: ")
    # console_address = input("Enter Address: ")
    # console_contact = input("Enter Contact: ")
    # console_nominee = input("Enter Nominee Name: ")
    # console_relation = input("Enter Relationship with Nominee: ")

    # Storing varables into dictionary
    # registration_details = {
    #     "Name":console_name,
    #     "Email":console_email,
    #     "Password":console_password,
    #     "Address":console_address,
    #     "Contact":console_contact,
    #     "Nominee":console_nominee,
    #     "Relation":console_relation
    # }

    # Printing dictionary
    # print(registration_details)

    random_id = randint(1000000, 9999999)
    random_id = str(random_id)

    # IF the form is submitted
    if request.method == "POST":

        # Storing input data into variables
        customer_id = request.form["register_id"]
        form_name = request.form["register_name"]
        form_email = request.form["register_email"]
        form_password = request.form["register_password"]
        form_address = request.form["register_address"]
        form_contact = request.form["register_contact"]
        form_nominee = request.form["register_nominee"]
        form_relation = request.form["register_relation"]

        # Storing input data into a dictionary
        registration_form = {
            "Customer Id":customer_id,
            "Name":form_name,
            "Email":form_email,
            "Password":form_password,
            "Address":form_address,
            "Contact":form_contact,
            "Nominee":form_nominee,
            "Relation":form_relation
        }

        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO customer_registration(
                customer_id,
                customer_name,
                customer_email,
                customer_address,
                customer_password,
                customer_nominee,
                customer_relation,
                customer_contact
            ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            customer_id,
            form_name,
            form_email,
            form_address,
            form_password,
            form_nominee,
            form_relation,
            form_contact
        ))

        mysql.connection.commit()
        cursor.close()

        # Displaying Success message in console
        print("Customer Registration is Successful!")
        return render_template("Registration/SuccessfulRegistration.html", customer_id=customer_id, customer_name=form_name, customer_email=form_email)

    return render_template("/Registration/Registration.html", random_id=random_id)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Making session permanent
        session.permanent = True

        customer_name = request.form["login_name"]
        customer_password = request.form["login_password"]

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT customer_name, customer_password FROM customer_registration WHERE customer_name=%(customer_name)s", {"customer_name":customer_name})
        select_login = cursor.fetchone()
        if not select_login:
            print("Invalid Login Details!")
            return redirect("/login")
        else:
            if select_login[0] == customer_name:
                if select_login[1] == customer_password:
                    # Storing passenger name in the session
                    session["customer_name"] = customer_name

                    return render_template("Customer/CustomerHome.html", customer_name=customer_name)
                else:
                    return redirect("/login")
            else:
                return redirect("/login")

    else:

        # IF block gets executed if passenger name is in session
        if "customer_name" in session:
            customer_name = session["customer_name"]
            return render_template("Customer/CustomerHome.html", customer_name=customer_name)

        # ELSE block gets executed if passenger name is not in session
        else:
            return render_template("Login/Login.html")

@app.route("/customer-home")
def customerHome():

    # IF customer is logged in, then redirect to customer home pge
    if "customer_name" in session:
        customer_name = session["customer_name"]
        return render_template("Customer/CustomerHome.html", customer_name=customer_name)
    else:
        return redirect("/login")

@app.route("/logout")
def logout():

    # IF block gets executed if method is GET
    if request.method == "GET":

        # Deleting passenger name from session
        session.pop("customer_name", None)
        return redirect("/login")

@app.route("/choose-policy", methods=["POST", "GET"])
def choosePolicy():

    policy_number = randint(1000000,9999999)

    # IF requested method is GET
    if request.method == "POST":

        # Storing policy details in variables
        customer_id = request.form["customer_id"]
        policy_number = request.form["policy_number"]
        policy_type = request.form["policy_type"]
        policy_title = request.form["policy_title"]
        sum_assured = request.form["sum"]
        premium_amount = request.form["premium"]
        policy_term = request.form["term"]

        # Getting user input from the console
        # type = input("Enter policy type: ")
        # title = input("Enter policy title: ")
        # sum = input("Enter policy sum assured: ")
        # premium = input("Enter policy premium amount: ")
        # term = input("Enter policy policy term: ")

        # # Storing variables into a dictionary
        # policy_details = {
        #     "Policy Number":policy_number,
        #     "Policy Type":type,
        #     "Policy Title":title,
        #     "Sum Assured":sum,
        #     "Premium Amount":premium,
        #     "Policy Term":term
        # }

        # print(policy_details)

        # Creating cursor to the connection
        cursor = mysql.connection.cursor()

        # INSERT policy details into database.
        cursor.execute('''
            INSERT INTO customer_policy(policy_number, policy_date, policy_type, policy_title, premium_amount, sum_assured, customer_id)
            VALUES(%s,CURDATE(),%s,%s,%s,%s,%s)
        ''', (
            policy_number, policy_type, policy_title, premium_amount, sum_assured, customer_id
        ))

        # Commiting all the changes
        mysql.connection.commit()
        cursor.close()

        # Displaying Success message in console
        print("Policy Taken Successfully!")

        return render_template("Customer/PolicyChosen.html", policy_number=policy_number, policy_type=policy_type, policy_title=policy_title)

    # IF user has already logged in
    if "customer_name" in session:
        customer_name = session["customer_name"]
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT customer_id FROM customer_registration WHERE customer_name=%(customer_name)s", {"customer_name":customer_name})
        select_id = cursor.fetchone()
        cust_id = select_id[0]
        return render_template("Customer/ChoosePolicy.html", policy_number=policy_number, cust_id=cust_id)
    else:
        return redirect("/login")

@app.route("/view-policy", defaults={"table":1})
@app.route("/view-policy/table/<int:table>")
def view_policy(table):
    if request.method == "GET":

        # Only 5 records per table
        limit = 5
        offset = table * limit - limit

        # If user is logged in, then IF block gets executed
        if "customer_name" in session:
            customer_name = session["customer_name"]

            # Creating a cursor
            cursor = mysql.connection.cursor()

            # SELECT query for getting the passenger id of the logged in user
            cursor.execute("SELECT customer_id FROM customer_registration WHERE customer_name=%(customer_name)s", {"customer_name":customer_name})

            # Fetching the passenger id
            select_id = cursor.fetchone()

            # IF block gets executed if passenger id is fetched
            if select_id:

                # Storing passenger id in the variable
                customer_id = select_id[0]
                customer_id = str(customer_id)

            # Variable for next and previous table(pagination)
            next = table + 1
            prev = table - 1

            # SELECT query for getting the booking history of passenger
            cursor.execute("SELECT * FROM customer_policy WHERE customer_id=%s LIMIT %s OFFSET %s", (customer_id, limit, offset))

            # Fetching booking history
            select_all = list(cursor.fetchall())
            for data in select_all:
                commence_date = data[1]

                # Displaying policy details in the console
                print(data)

            # Adding 1 year in the commence date
            td = timedelta(365)
            next_due = commence_date + td
            
            print(next_due)

            return render_template("Customer/ViewPolicy.html", customer_id=customer_id, next_due=next_due, title="View Policy", policy_history=select_all, next=next, prev=prev)
        
        # Redirect to login if not in session
        else:
            return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)