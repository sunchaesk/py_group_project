
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
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

key=os.urandom(12).hex()

app.secret_key = key

db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), unique=True)
	email = db.Column(db.String(100), unique=True)
	password=PasswordField(db.String(50))

	def __init__(self,name,email,password):
		self.username=name
		self.username=email
		self.username=password
		
db.create_all()	

class Signup(FlaskForm):
	username = StringField('Username', [validators.DataRequired(message="Fill out this field pls"),validators.Length(min=4, max=25)])
	email = StringField('Email Address', [validators.DataRequired(message="Fill out this field pls"),validators.Length(min=6, max=35)])
	password=PasswordField('New Password', [validators.DataRequired(),validators.EqualTo('confirm')])
	confirm = PasswordField('Repeat Password',[validators.DataRequired()])
	submit = SubmitField("Sign up")

	

class Login(FlaskForm):
	email = StringField('Email Address', [validators.Length(min=6, max=35)])
	password=PasswordField('Password', [validators.DataRequired()])

@app.route("/")
def home():
    return render_template("index.html", content="Testing")

@app.route("/about")
def about():
    return render_template("about.html", content="AboutTesting")

@app.route("/signup", methods=["POST","GET"])
def signup():
	form= Signup()
	print("hi")
	if request.method=="POST":
		existing_user = User.query.filter_by(name = form.username.data , email = form.email.data).first()
		print(existing_user)
		if existing_user:
			print("This is bad news")
			return make_response(f"The name or the gmail you enter is already created")

		else:
			
			user= User(form.username.data,form.email.data,form.password.data)
			print(user)
			db.create_all()
			db.session.add(user)
			db.session.commit()
			
			print("Saved")
			#flash('Thanks for registering')
			return redirect(url_for("home"))

    


	return render_template("signup.html",form=form)

@app.route("/login", methods=["POST","GET"])
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
