from os import name
import re
from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
from flask_cors import CORS, cross_origin
from datetime import date

from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
CORS(app)
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
            "role": data[0][2],
            "email": data[0][3]
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

@app.route('/logout')
def logout():
    print("logout")
    if 'email' in session:
        session.pop('email', None)
        pass
    return redirect(url_for('index'))

@app.route('/')
def index():
    tempSession = getCurrentUser()
    rooms = get_rooms()
    return render_template('home.html', session = {"login": tempSession["login"], "user": tempSession["user"]}, rooms = rooms['rows'])


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
    rows = cur.fetchall()
    print("rows:",rows)
    for res in rows:
      print(res)
    conn.close()
    return {"rows": rows}

def get_comments():
    conn=sqlite3.connect("hotel_db.db")
    cur = conn.cursor()
    cur.execute("SELECT name, id_room, message, rating FROM comments inner join user using (id_user)")
    rows =cur.fetchall()
    print("rows:",rows)
    for res in rows:
      print(res)
    conn.close()
    return {"rows": rows}

@cross_origin
@app.route("/room/<startDate>/<targetDate>")
def room_availability(startDate,targetDate):
    # Connect to db
    db = sqlite3.connect('hotel_db.db')
    cursor = db.cursor()

    # get data into db
    cursor.execute('select id_room FROM room where id_room not in(select id_room from reservation where visibility=="0" OR state=="0" OR startDate between "%s" and "%s" OR targetDate between "%s" and "%s" OR "%s" between startDate and targetDate OR "%s" between startDate and targetDate );' % (startDate,targetDate,startDate,targetDate,startDate,targetDate))
    rows =cursor.fetchall()
    # Close db connection
    db.close()
    return {"rows": rows}

@app.route("/reservation",methods=["POST"])
def add_reservation():
    startDate = request.json["startDate"]
    targetDate = request.json["targetDate"]
    id_user = getCurrentUser()["user"]["id"]
    id_room = request.json["id_room"]
    state = 1
    if startDate and targetDate and id_user and id_room:
        # Connect to db
        db = sqlite3.connect('hotel_db.db')
        cursor = db.cursor()
        # Insert data into db
        cursor.execute('INSERT INTO reservation(id_user, id_room, startDate, targetDate, state) VALUES("%s", "%s","%s","%s","%s")' % (id_user, id_room, startDate, targetDate, state))
        db.commit()
        # Close db connection
        db.close()
        return {"message": "reservation added", "data":request.json}
    else:
        return {"message": "data missing"}


@app.route("/feed", methods=["GET","POST"])
def feed_page():
    tempSession = getCurrentUser()
    user = tempSession["user"]
    if request.method == "POST":
        data = request.form
        if(user):
            print(f'El usuario {user["name"]}')
            print(f'el usuario estaba en la habitación{data["room"]}')
            print(f'le da un puntaje de {data["rate"]}')
            print(f'y dice que {data["comment"]}')
            # Connect to db
            db = sqlite3.connect('hotel_db.db')
            cursor = db.cursor()

            # Insert data into db
            cursor.execute('INSERT INTO comments(id_user, id_room, message, rating) VALUES("%s", "%s","%s","%s")' % (user["id"],request.form["room"],request.form["comment"] ,request.form["rate"]))
            db.commit()
            # Close db connection
            db.close()
    rooms = get_rooms()
    comments = get_comments()
    if rooms:
        print("estas son las habitaciones: ", rooms)
        return render_template('feedback.html', rooms = rooms["rows"],comments = comments["rows"][::-1] , session = {"login": tempSession["login"], "user": tempSession["user"]})
    else:
        return render_template('feedback.html', rooms=["No hay habitaciones disponibles"], comments = comments["rows"],session = {"login": tempSession["login"], "user": tempSession["user"]})

@app.route('/rooms')
def get_rooms2():
    conn=sqlite3.connect("hotel_db.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM room")
    rows = cur.fetchall()
    print("rows:",rows)
    for res in rows:
      print(res)
    conn.close()
    return {"rows": rows}

def get_user():
    conn=sqlite3.connect("hotel_db.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    print("rows:",rows)
    for res in rows:
      print(res)
    conn.close()
    return rows
def delete_user(user_id):
    # Connect to db
    db = sqlite3.connect('hotel_db.db')
    cursor = db.cursor()
    # delete data into db
    cursor.execute('DELETE FROM user WHERE id_user ="%s"' % (user_id))
    db.commit()
    # Close db connection
    db.close()

def update_user(user_id, name, email):
    # Connect to db
    db = sqlite3.connect('hotel_db.db')
    cursor = db.cursor()
    # update data into db
    cursor.execute('UPDATE user SET name ="%s", email="%s" WHERE id_user ="%s"' % (name, email, user_id))
    db.commit()
    # Close db connection
    db.close()

def update_user_role(user_id,role):
    # Connect to db
    db = sqlite3.connect('hotel_db.db')
    cursor = db.cursor()
    # update data into db
    cursor.execute('UPDATE user SET role="%s" WHERE id_user ="%s"' % (role, user_id))
    db.commit()
    # Close db connection
    db.close()

@app.route("/dashboard/usuario", methods=["GET", "POST"])
def dashboard_page():
    print("request.method:    ",request.method)
    print("request.form",request.form)
    if request.method=="POST":
        name = request.form["name"]
        email = request.form["email"]
        id = int(request.form["id"])
        update_user(id, name, email)
    users = get_user()
    tempSession = getCurrentUser()
    return render_template('user.dashboard.html',users=users ,session = {"login": tempSession["login"], "user": tempSession["user"]})

@app.route("/dashboard/usuario/<id>")
def dashboard_Delete(id):
    delete_user(id)
    users = get_user()
    tempSession = getCurrentUser()
    return render_template('user.dashboard.html',users=users ,session = {"login": tempSession["login"], "user": tempSession["user"]})

def get_admins():
    conn=sqlite3.connect("hotel_db.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE role=='admin'")
    rows = cur.fetchall()
    print("rows:",rows)
    for res in rows:
      print(res)
    conn.close()
    return rows

@app.route("/dashboard/admin", methods=["GET", "POST"])
def dashboard_admin_page():
    print("request.method:    ",request.method)
    print("request.form",request.form)
    if request.method=="POST":
        name = request.form["name"]
        email = request.form["email"]
        id = int(request.form["id"])
        role = request.form["role"]
        print("XXXXXXXXXXXXXX role:", role)
        update_user_role(id, role)
        update_user(id, name, email)
    
    if request.method=="DELETE":
        id = request.form["id"]
        delete_user(id)
    users = get_admins()
    tempSession = getCurrentUser()
    return render_template('admins.dashboard.html',users=users ,session = {"login": tempSession["login"], "user": tempSession["user"]})
@app.route('/dashboard/admin/crear', methods=["POST"])
def dashboard_admin_create():
    

    name = request.form['name']
    role = request.form['role']
    email = request.form['email']
    password = request.form['password']
    password = generate_password_hash(password, 'sha256', 30)
    #conectamos con la bd
    db = sqlite3.connect('hotel_db.db')
    cursor = db.cursor()

    sentencia = 'INSERT INTO user(name, role, email, password) VALUES("%s", "%s", "%s", "%s")' % (name, role, email, password)
    cursor.execute(sentencia)
    db.commit()
    db.close()
    users = get_admins()
    tempSession = getCurrentUser()
    return render_template('admins.dashboard.html',users=users ,session = {"login": tempSession["login"], "user": tempSession["user"]})

@app.route("/dashboard/admin/delete/<id>")
def dashboard_admin_delete(id):
    delete_user(id)
    users = get_user()
    tempSession = getCurrentUser()
    return render_template('user.dashboard.html',users=users ,session = {"login": tempSession["login"], "user": tempSession["user"]})

def get_room():
    conn=sqlite3.connect("hotel_db.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM room")
    rows = cur.fetchall()
    print("rows:",rows)
    for res in rows:
      print(res)
    conn.close()
    return rows

def add_room(state, visibility, floor):
    # Connect to db
    db = sqlite3.connect('hotel_db.db')
    cursor = db.cursor()

    # Insert data into db
    cursor.execute('INSERT INTO room(state, visibility, floor) VALUES("%s", "%s","%s")' % (state, visibility, floor))
    db.commit()

    # Close db connection
    db.close()
def delete_room(room_id):
    # Connect to db
    db = sqlite3.connect('hotel_db.db')
    cursor = db.cursor()
    # delete data into db
    cursor.execute('DELETE FROM room WHERE id_room ="%s"' % (room_id))
    db.commit()
    # Close db connection
    db.close()

def update_room(room_id, state, visibility, floor):
    # Connect to db
    db = sqlite3.connect('hotel_db.db')
    cursor = db.cursor()
    # update data into db
    cursor.execute('UPDATE room SET state ="%s", visibility="%s", floor="%s" WHERE id_room ="%s"' % (state, visibility, floor, room_id))
    db.commit()
    # Close db connection
    db.close()
@app.route("/dashboard/habitaciones", methods=["GET", "POST"])
def dashboard_habitacion_page():
    if request.method == "POST":
        state=request.form["state"]
        visibility=request.form["visibility"]
        floor=request.form["floor"]
        add_room(state, visibility, floor)
    rooms=get_room()
    tempSession = getCurrentUser()
    return render_template('habitacion.dashboard.html',rooms=rooms, session = {"login": tempSession["login"], "user": tempSession["user"]})

@app.route("/dashboard/habitaciones/<action>/<id_room>", methods=["GET", "POST"])
def dashboard_habitacion_update_delete(action,id_room):
    if request.method == "POST":
        if action=="editar":
            state=request.form["state"]
            visibility=request.form["visibility"]
            floor=request.form["floor"]
            update_room(id_room, state, visibility, floor)
        elif action == "eliminar":
            delete_room(id_room)
    rooms=get_room()
    tempSession = getCurrentUser()
    return render_template('habitacion.dashboard.html',rooms=rooms, session = {"login": tempSession["login"], "user": tempSession["user"]})

@app.route("/dashboard/reservaciones", methods=["GET", "POST"])
def dashboard_reservaciones_page():
    tempSession = getCurrentUser()
    conn=sqlite3.connect("hotel_db.db")
    cur = conn.cursor()
    cur.execute('select name, id_room, startDate, targetDate, email from reservation INNER JOIN user USING (id_user)')
    rows = cur.fetchall()
    conn.close()
    length = len(rows)
    rows=list(rows)[::-1]
    newRows= map(addPrice, rows)
    return render_template('reservations.dashboard.html',len=length, rows=newRows, session = {"login": tempSession["login"], "user": tempSession["user"]})

@app.route("/disponibility", methods=["GET", "POST"])
def look_for_disponibility():
    data = request.form
    print(f'el usuario estaba en la habitación{data["room"]}')
    print(f'le da un puntaje de {data["rate"]}')
    print(f'y dice que {data["comment"]}')
    rooms=get_rooms()
    print("***************ROOMS****************")
    print(rooms)
    return render_template('feedback.html')

def addPrice(row):
    vec = list(row)
    print(f'xxxxxxxxx', row[2])
    start = row[2].split("-")
    end = row[3].split("-")
    print(f'xxxxxxxxx', start, end)
    d0 = date(int(start[0]), int(start[1]), int(start[2]))
    d1 = date(int(end[0]), int(end[1]), int(end[2]))
    delta = d1 - d0
    print("XXXXXXXXXXXXXXXXX vec: ", vec)
    vec.append((delta.days+1)*100000)
    return vec
@app.route("/reservation", methods=["GET", "POST"])
def reservation_page():
    tempSession = getCurrentUser()
    id_user = tempSession["user"]["id"]
    conn=sqlite3.connect("hotel_db.db")
    cur = conn.cursor()
    cur.execute('SELECT * FROM reservation WHERE id_user ="%s" ORDER BY startDate ' % (id_user))
    rows = cur.fetchall()
    conn.close()
    length = len(rows)
    rows=list(rows)[::-1]
    newRows= map(addPrice, rows)
    return render_template('reservation.html',len=length, rows=newRows, session = {"login": tempSession["login"], "user": tempSession["user"]})
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

#q se ejeucte algo antes de cualquier peticion
# como un mildelware
@app.before_request
def cargarSelect():
    tempSession = getCurrentUser()
    logged = tempSession["login"]
    user = tempSession["user"]
    if logged==0 and request.endpoint in ["feed_page", "dashboard_page", "dashboard_habitacion_page", "dashboard_admin_page", "dashboard_admin_create","dashboard_admin_delete"]:
        return redirect(url_for("index"))
    if logged==1:
        if user["role"]!="admin" and request.endpoint in ["dashboard_page", "dashboard_habitacion_page", "dashboard_admin_page", "dashboard_admin_create","dashboard_admin_delete"]:
            return redirect(url_for("index"))
    if logged==1:
        if user["role"]!="superadmin" and request.endpoint in ["dashboard_admin_page", "dashboard_admin_create", "dashboard_admin_delete"]:
            return redirect(url_for("index"))
if __name__ == '__main__':
    app.run(debug=True, port=5000)