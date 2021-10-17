from flask import Flask, render_template

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

@app.route('/about/<username>')
def about_page(username):
    return f'<h1>About page of {username}</h1>'