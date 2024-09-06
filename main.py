import time
from logistics import get_response
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import smtplib
import csv
import markdown
from merger import parser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

EMAIL = '<your-email-here>'
PASSWORD = 'your-password-here'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = '<your-database-url-here>'
db = SQLAlchemy()
db.init_app(app)

# Configure Flask-Login's Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

def get_id(self):
    return self.email


# Create a user_loader callback
@login_manager.user_loader
def load_user(email):
    return User.query.get(email)

# CREATE TABLE IN DB with the UserMixin
class User(UserMixin, db.Model):
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    city = db.Column(db.String(1000))
    number = db.Column(db.Integer)

    def get_id(self):
        return self.email


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # Passing True or False if the user is authenticated.
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        try:
            send_mail(to=email, subject="Subject:Welcome to Logistics\n\nYou have successfully signed up.")
        except Exception as e:
            flash("Invalid Email Address. Failed to Sign-Up!")
            return redirect(url_for('register'))
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            password=hash_and_salted_password,
            name=request.form.get('name'),
            city=request.form.get('city'),
            number=request.form.get('number')
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("secrets"))
    # Passing True or False if the user is authenticated.
    return render_template("register.html", logged_in=current_user.is_authenticated)



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home', logged_in=current_user.is_authenticated))
    # Passing True or False if the user is authenticated.
    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/admin-login', methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        if email == "polyglots@gmail.com" and password == "yyhj":
            session['email'] = email
            return render_template('lorry.html')
        else:
            flash("You are not authorized to access this page.")
            return redirect(url_for('admin_login'))
    # Passing True or False if the user is authenticated.
    return render_template("admin.html")


# Only logged-in users can access the route
@app.route('/secrets', methods=["GET", "POST"])
@login_required
def secrets():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        source = request.form.get('source')
        destination = request.form.get('destination')
        product = request.form.get('product')
        deadline = request.form.get('deadline')
        year, month, day = deadline.split('-')

        # Reformat the date to DD-MM-YYYY
        deadline = f"{day}-{month}-{year}"
        with open('data.csv', mode='a')as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([name,product, source, destination, deadline])
        send_mail(to=email, subject="Subject:Booking Confirmation\n\nYour Booking has been confirmed."
                                    "Booking Details : \nName: {}, Source: {}, Destination: {}, "
                                    "Delivery Deadline: {}, Product: {}".format(name, source, destination,
                                                                                deadline, product))
        return render_template("success.html")
    return render_template("secrets.html", name=current_user.name, logged_in=True)

@app.route('/logout')
def logout():
    logout_user()
    if "email" in session:
        session.pop("email", None)
    return redirect(url_for('home'))


@app.route('/admin/lorry')
def lorry():
    if "email" in session:
        return render_template('lorry.html')

@app.route('/admin/dispatch')
def dispatch():
    if "email" in session:
        parser("./data.csv")
        get_response()
        try:
            with open('answer.txt', 'r') as file:
                markdown_content = file.read()
            content = markdown.markdown(markdown_content)
        except FileNotFoundError:
            content = "File not found."
        with open("data.csv", mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(['Customer_name','Product_name','Source','Destination','Delivery_deadline'])
        return render_template('answer.html', content=content)


def send_mail(to, subject):
    with smtplib.SMTP('smtp.gmail.com', port=587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(
            from_addr=EMAIL,
            to_addrs=to,
            msg=subject
        )


if __name__ == "__main__":
    app.run(debug=True)