import re
from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3

from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.secret_key = 'nekomotsu9029'

def getCurrentUser():
    if 'email' in session:
        email = session['email']
        db = sqlite3.connect('hotel_db.db')

        sentencia = "SELECT * FROM user where email='"+email+"'"
        
        cursor = db.cursor()
        cursor.execute(sentencia)
        data = cursor.fetchall()

        db.close()

        if(len(data) > 0):
            user = {
            "id": data[0][0],
            "name": data[0][1],
            "rol": data[0][3],
            "email": data[0][4]
            }
            return {
                "login": 1,
                "user": user
            }
        else:
            return {
                "login": 0,
                "user": ""
            }
    else:
        return {
            "login": 0,
            "user": ""
        }

@app.route('/signIn', methods=["POST"])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = sqlite3.connect('hotel_db.db')

        sentencia = "SELECT * FROM user where email='"+email+"'"
        
        cursor = db.cursor()
        cursor.execute(sentencia)
        data = cursor.fetchall()

        db.close()

        if(str(data) == "[]"):
            message="El correo no existe en nuestra bd :("
            return render_template('home.html', session = {"login": 0, "message": message})
        else:
            if(check_password_hash(data[0][4], password)):
                session['email'] = email
                return redirect(url_for('index'))
            else:
                message="La contraseña no coincide :("
                return render_template('home.html', session = {"login": 0, "message": message})

@app.route('/signUp', methods=["POST"])
def signup():
    #conectamos con la bd
    db = sqlite3.connect('hotel_db.db')
    cursor = db.cursor()

    name = request.form['name']
    role = "usuario"
    #request.form['role']
    email = request.form['email']
    password = request.form['password']
    password = generate_password_hash(password, 'sha256', 30)

    sentencia = 'INSERT INTO user(name, role, email, password) VALUES("%s", "%s", "%s", "%s")' % (name, role, email, password)

    cursor.execute(sentencia)
    db.commit()

    db.close()
    session['email'] = email
    return redirect(url_for('index'))

@app.route('/')
def index():
    tempSession = getCurrentUser()
    return render_template('home.html', session = {"login": tempSession["login"], "user": tempSession["user"]})


@app.route("/home")
def logged_page():
    return render_template('loggedIn.html')

# def getInicio():
#     conn=sqlite3.connect("baseTabla.db")
#     c = conn.cursor()
#     row=c.execute("SELECT * FROM tabla")
#     resultado =c.fetchall()
#     for res in resultado:
#       print(res)
#     conn.close()

# Obtener las habitaciones
def get_rooms():
    conn=sqlite3.connect("hotel_db.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM room")
    rows =cur.fetchall()
    print("rows:",rows)
    for res in rows:
      print(res)
    conn.close()
    return {"rows": rows}


@app.route("/feed")
def feed_page():
    rooms = get_rooms()
    tempSession = getCurrentUser()
    if request.method == "POST":
        data = request.form
        print(f'el usuario estaba en la habitación{data["room"]}')
        print(f'le da un puntaje de {data["rate"]}')
        print(f'y dice que {data["comment"]}')
    if rooms:
        print("estas son las habitaciones: ", rooms)
        return render_template('feedback.html', rooms = rooms["rows"], session = {"login": tempSession["login"], "user": tempSession["user"]})
    else:
        return render_template('feedback.html', rooms=["No hay habitaciones disponibles"], session = {"login": tempSession["login"], "user": tempSession["user"]})
    
    


@app.route("/dashboard")
@app.route("/dashboard/")
@app.route("/dashboard/usuarios")
def dashboard_page():
    tempSession = getCurrentUser()
    return render_template('user.dashboard.html', session = {"login": tempSession["login"], "user": tempSession["user"]})


@app.route("/dashboard/habitaciones")
def dashboard_habitacion_page():
    tempSession = getCurrentUser()
    return render_template('habitacion.dashboard.html', session = {"login": tempSession["login"], "user": tempSession["user"]})

@app.route("/comment", methods=["GET", "POST"])
def add_comment():
    data = request.form
    print(f'el usuario estaba en la habitación{data["room"]}')
    print(f'le da un puntaje de {data["rate"]}')
    print(f'y dice que {data["comment"]}')
    rooms=get_rooms()
    print("***************ROOMS****************")
    print(rooms)
    return render_template('feedback.html')

@app.route("/test")
def test_page():
    tempSession = getCurrentUser()
    return render_template('test.html', session = {"login": tempSession["login"], "user": tempSession["user"]})


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

if __name__ == '__main__':
    app.run(debug=True, port=5000)