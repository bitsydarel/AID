#!/usr/bin/emv python

#importing dependencary 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, validators
from flask_socketio import SocketIO, send

#defining config
app = Flask(__name__)
#initiating the database
db = SQLAlchemy(app)
#setting the database credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:darel242@localhost:5435/aid_server'
#setting secret key 
app.config['SECRET_KEY'] = 'Qwerty'
#defining socket io app
socketio = SocketIO(app)

#creating user in database
class User(db.Model):
    """Class that help to create user in the database"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

#form for the create user page 
class CreateUserForm(Form):
    """Class that help to create user form for the html page"""
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Create User')

#form for the user login page
class LoginUserForm(Form):
    """Class that create the user form for the html page"""
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.DataRequired()])
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginUserForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        pass
    return render_template('index.html')

#create user page
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    #create a object
    form = CreateUserForm(request.form)
    #checking the request method
    if request.method == 'POST' and form.validate_on_submit():
            #taking the data from the form and parsing it as arg for the create user class
            user = User(form.username.data, form.password.data)
            db.session.add(user)

            db.session.commit()
            return redirect(url_for('success'))
    return render_template('create_user.html', form=form)

#page that confirm if user has been successfully created
@app.route('/success')
def success():
    return render_template('success.html')

#bot channel page
@app.route('/aid_bot')
def aid_bot():
    return render_template('aid_bot.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
