from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('home.html')


@app.route("/home")
def logged_page():
    return render_template('loggedIn.html')


@app.route("/feed")
def feed_page():
    return render_template('feedback.html')


@app.route("/dashboard")
@app.route("/dashboard/")
@app.route("/dashboard/usuarios")
def dashboard_page():
    return render_template('user.dashboard.html')


@app.route("/dashboard/habitaciones")
def dashboard_habitacion_page():
    return render_template('habitacion.dashboard.html')


@app.route("/test")
def test_page():
    return render_template('test.html')


@app.route("/testhttp", methods=["GET", "POST"])
def rest_http():
    if request.method == "POST":
        user = request.form
        print(user)
        # Connect to db
        db = sqlite3.connect('hotel_db.db')
        cursor = db.cursor()

        # Insert data into db
        cursor.execute('INSERT INTO user(name, role, email,password) VALUES("%s", "%s","%s","%s")' % (
            "daniel", "admin", "jose@gmail.com", "12345"))
        db.commit()

        # Close db connection
        db.close()
        return render_template('home.html', user=user)
    else:
        return render_template('home.html')


@app.route('/about/<username>')
def about_page(username):
    return f'<h1>About page of {username}</h1>'
