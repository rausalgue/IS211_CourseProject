#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignemnt Week 13 - Flask App"""

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import re
import sqlite3 as lite
from contextlib import closing
import pprint

DATABASE = 'book.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)

con = lite.connect('book.db')

cur = con.cursor()

cur.executescript("""
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS books;
    DROP TABLE IF EXISTS clouds;
    DROP TABLE IF EXISTS items;
    CREATE TABLE users(
        Identifier INTEGER PRIMARY KEY, 
        FirstName TEXT, 
        LastName TEXT, 
        UserId TEXT, 
        UserPassword TEXT
    );
    CREATE TABLE books(
        Identifier INTEGER PRIMARY KEY, 
        Title TEXT, 
        Author TEXT,
        PageCount INTEGER,
        AverageRating INTEGER
    );
    CREATE TABLE clouds(
        Identifier INTEGER PRIMARY KEY, 
        UserObject INTEGER, 
        Name TEXT, 
        FOREIGN KEY (UserObject) REFERENCES users(Identifier)
    );
    CREATE TABLE items (
      Identifier INTEGER PRIMARY KEY,
      UserObject INTEGER,
      CloudObject INTEGER,
      ContentObject INTEGER,
      FOREIGN KEY (UserObject) REFERENCES users(Identifier),
      FOREIGN KEY (CloudObject) REFERENCES clouds(Identifier),
      FOREIGN KEY (ContentObject) REFERENCES books(Identifier)
    );
    """)
#Create Base User
cur.execute('INSERT into users VALUES (517101,"Admin","User","admin","password");')
cur.execute('INSERT into users VALUES (517102,"System","User","system","password");')

#Create 2 Content Objects
cur.execute('INSERT into books VALUES (9781449372620,"Flask Web Development","Miguel Grinberg",237,0);')
cur.execute('INSERT into books VALUES (9780446310789,"To Kill a Mockingbird","Harper Lee",384,4.5);')

#Create 2 Clouds for Base User
cur.execute('INSERT into clouds VALUES (1,517101,"Favorite Books");')
cur.execute('INSERT into clouds VALUES (2,517101,"Books to Read");')
cur.execute('INSERT into clouds VALUES (3,517102,"My Books");')
cur.execute('INSERT into clouds VALUES (4,517102,"Terrible Books");')

#Create Items under Favorite Books
cur.execute('INSERT into items VALUES (11701,517101,1,9781449372620);')
cur.execute('INSERT into items VALUES (11702,517101,2,9780446310789);')

con.commit()

def connect_db():
    return lite.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#app = Flask(__name__)
app.secret_key = 'lasso91'


def getSessionInfo ():
    token = ''
    print session
    if len(session)>0:
        if session['User_Id']>0:
            token = True

    return token

@app.route('/')
def index():
    print session
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None

    # Check if we alredy have sessionInfo
    if len(session) == 0 or session['Logged_In']=='N':
        if request.method == 'POST':
            print 'entering login POST'

            user_data = LoginUser(request.form['email'],request.form['password'])

            #if request.form['email'] == 'admin' and request.form['password'] == 'password':
            if user_data['Success']:
                session['Logged_In'] = 'Y'
                session['User_Name'] = user_data['First Name']
                session['User_Id'] = user_data['UserID']
                return redirect("/dashboard")
            else:
                session['Logged_In'] = 'N'
                error = 'Incorrect login or password'
                return render_template('Login.html', error=error)
        else:
            return render_template('Login.html')
    else:
        #validate Sessions Info
        #return render_template('login.html', error=error)
        return redirect('/dashboard')

@app.route('/signup', methods=['GET','POST'])
def createUser():
    session.pop('User_Id', None)
    session.pop('Logged_In', None)
    session.pop('User_Name', None)
    error = None

    print session

    if request.method == 'POST':
        print 'entering Sign Up POST'

        conns = g.db.execute('SELECT MAX(Identifier) FROM users')
        greatest_id = 0
        for row in conns.fetchall():
            greatest_id = row[0]

        greatest_id += 1

        #Create New User Record
        g.db.execute('insert into users (Identifier, FirstName, LastName, UserId, UserPassword) values (?, ?, ?, ?, ?)',
                     [greatest_id, request.form['fName'], request.form['lName'], request.form['userId'], request.form['userPassword']])
        g.db.commit()

        session['Logged_In'] = 'Y'
        session['User_Name'] = request.form['fName']
        session['User_Id'] = request.form['userId']

        print session

        return redirect("/dashboard")

    else:
        #validate Sessions Info
        return render_template('newuser.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('User_Id', None)
    session.pop('Logged_In', None)
    session.pop('User_Name', None)
    return redirect(url_for('index'))

def LoginUser(userid,password):
    conns = g.db.execute('select Identifier, FirstName, LastName, UserId, UserPassword from users')
    users = [dict(Identifier=row[0], FirstName=row[1], LastName=row[2], UserId=row[3], UserPassword=row[4])
             for row in conns.fetchall()]

    print 'entering login'
    print users

    for value in users:
        if userid == value['UserId']:
            if password == value['UserPassword']:
                user_data = {
                    "First Name": value["FirstName"],
                    "UserID": value["Identifier"],
                    "Success": True
                }
                print "Matching Id and Password"
                return user_data

    print userid
    print password

    error = 'Incorrect login or password'

    user_data = {
        "Success": False,
        "ErrorMessage": error
    }

    return user_data

@app.route('/dashboard')
def dashboard():
    valid = getSessionInfo()

    userName = session['User_Name']

    user_object = (session['User_Name'],session['User_Id'],)


    conns = g.db.execute('select Identifier, UserObject, Name from clouds')
    clouds = [dict(Identifier=row[0], UserId=row[1], Name=row[2])
               for row in conns.fetchall()]

    conns = g.db.execute('select Identifier, Title, Author, PageCount, AverageRating from books')
    books = [dict(Identifier=row[0], Title=row[1], Author=row[2], PageCount=row[3], AverageRating=row[4])
                for row in conns.fetchall()]

    conns = g.db.execute('select Identifier, FirstName, LastName, UserId, UserPassword from users')
    users = [dict(Identifier=row[0], FirstName=row[1], LastName=row[2], UserId=row[3], UserPass=row[4])
               for row in conns.fetchall()]


    if valid:
        return render_template('dashboard.html', user_object=user_object, clouds=clouds, books=books, users=users)
    else:
        return redirect(url_for('index'))

@app.route('/cloud/add', methods=['GET', 'POST'])
def newCloud():
    valid = getSessionInfo()

    if valid:
        conns = g.db.execute('SELECT MAX(Identifier) FROM clouds')
        greatest_id = 0
        for row in conns.fetchall():
            greatest_id = row[0]

        if request.method == 'POST':
            greatest_id += 1
            g.db.execute('insert into clouds (Identifier, UserObject, Name) values (?, ?, ?)',
                         [greatest_id,session['User_Id'], request.form['name']])
            g.db.commit()
            return redirect('/dashboard')
        return render_template("newcloud.html")
    else:
        return redirect(url_for('index'))

@app.route('/cloud/<identifier>')
def getCloudData(identifier):
    valid = getSessionInfo()

    print identifier

    if valid:
        conns = g.db.execute('SELECT * FROM items '
                           'JOIN users ON items.UserObject = users.Identifier '
                           'JOIN books ON items.ContentObject = books.Identifier ')
        items = conns.fetchall()

        print (items)

        conns = g.db.execute('SELECT Identifier, UserObject, Name FROM clouds where Identifier = (?)',
                             (identifier,))

        cloud_object = conns.fetchone()

        print cloud_object
        user_object = (session['User_Name'], session['User_Id'],)

        return render_template('cloudDetails.html', user_object=user_object, cloud_object=cloud_object, items=items)

    else:
        return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def getBookInfo():
    valid = getSessionInfo()

    if valid:
        user_object = (session['User_Name'], session['User_Id'],)

        print 'Valid',valid
        print user_object

        if request.method == 'POST':
            print len(request.form['searchId']),request.form['searchId']

            if len(request.form['searchId']) != 13:
                error = 'Please enter a valid ISBN Number'
                return render_template('search.html', user_object=user_object, error=error)
            else:
                print 'need to search for ISBN'
                error = 'Searching...'
                return render_template('search.html', user_object=user_object, error=error)
        else:
            return render_template('search.html', user_object=user_object)

    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()