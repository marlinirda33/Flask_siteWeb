from flask import render_template, url_for, redirect, request, flash
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import sqlite3





app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///ecommercial.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key =True)
    name = db.Column(db.String(200) ,nullable=False , unique=True)
    mail = db.Column(db.String(300), nullable=False , unique=True)
    passwd = db.Column(db.String(20) ,nullable=False)
    passwd2 = db.Column(db.String(20) ,nullable=False)

db.create_all()

def sign_up_User_to_db(name,passwd):
    con = sqlite3.connect('ecommercial.db')
    cur = con.cursor()
    cur.execute('INSERT INTO User (name,passwd,mail,passwd2) values (?,?)', (name,passwd))

def check_User(name,passwd):
    con = sqlite3.connect('ecommercial,db')
    cur = con.cursor()
    cur.execute('SELECT name,passwd from users where name=? passwd=?', (name,passwd))

    result = cur.fetchone()
    if result:
        return True
    else:
        return False


@app.route('/')
def index():
     return render_template("pageaccueil.html")
 
@app.route('/sign_up')
def sign_up():
    return render_template("sign_up.html")

@app.route('/sign_up', methods = ['POST','GET'])
def signupp():
    if request.method =="POST":
        name = request.form['name']
        mail = request.form['mail']
        passwd = request.form['passwd']
        passwd2 = request.form['passwd2']


        user = User(name=name,mail=mail,passwd=passwd,passwd2=passwd2)
        db.session.add(user)
        db.session.commit()
        return render_template("login.html")
           


@app.route("/login")
def login():
    return render_template("login.html")
    
@app.route("/login", methods = ['GET','POST'])
def login_():
    passwd = request.form['passwd']
    mail = request.form['mail']
    user = User.query.filter_by(mail=mail).first()

    return render_template("connexion.html")

@app.route("/logout")
def log():
    return render_template("login.html")
    
@app.route("/login", methods = ['GET','POST'])
def logout():
    passwd = request.form['passwd']
    mail = request.form['mail']
    user = User.query.filter_by(mail=mail).first()

    return render_template("login.html")



if __name__ == '__main__':
    app.run(debug= True)