from flask import Flask, redirect, url_for, render_template, make_response, request, flash
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import SelectField, SubmitField, TextField, StringField, PasswordField
import time
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
import flask_wtf
from flask_sqlalchemy import SQLAlchemy
from wtforms import validators
from argon2 import PasswordHasher
from wtforms.fields.html5 import EmailField
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.sqlite3'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

key=os.urandom(12).hex()

app.secret_key = key

db = SQLAlchemy(app)


class user(db.Model):
	_id = db.Column("id",db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	email= db.Column(db.String(100))
	password = db.Column(db.String(100))

	def __init__(self,name,email,password):
		self.name= name
		self.email=email
		self.password=password

	def __repr__(self):
	        return f"User( {self.name}, {self.email})"
		
#db.create_all()	

class Signup(FlaskForm):
	username = StringField('Username', [validators.DataRequired("Enter some shit here"),validators.Length(min=4, max=25)])
	email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
	password=PasswordField('New Password', [validators.DataRequired(),validators.EqualTo('confirm')])
	confirm = PasswordField('Repeat Password',[validators.DataRequired()])
	submit = SubmitField("Sign up")

	

class Login(FlaskForm):
	email = StringField('Email Address', [validators.Email("This field requires a valid email address")])
	password=PasswordField('Password', [validators.DataRequired()])


@app.route("/")
def home():


    return render_template("index.html", content="Testing")


@app.route("/about")
def about():

    return render_template("about.html", content="AboutTesting")

@app.route("/signup", methods=["POST","GET"])
def signup():
	form= Signup(prefix="a")
	print("hi")
	if request.method=="POST":
		existing_name = user.query.filter_by(name = form.username.data).first()
		existing_email = user.query.filter_by(email = form.email.data).first()
		if existing_name or existing_email:
			print("This is bad news")
			flash("The email or user name are already created")

		else:
			print("hi")
			ph = PasswordHasher()
			name=form.username.data
			email=form.email.data
			hashed_pw = ph.hash(form.password.data)
			
			usr= user(name=name, email=email, password=hashed_pw)
			
			db.session.add(usr)
			print(usr)
			db.session.commit()

			print("Saved")
			flash('Thanks for registering')
			return redirect(url_for("home"))

    


	return render_template("signup.html",form=form)

@app.route("/login", methods=["POST","GET"])
def login():
	form=Login()


	return render_template("login.html",form=form)


if __name__ == "__main__":
	db.create_all()
	app.run(debug=True)
