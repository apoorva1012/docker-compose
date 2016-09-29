from flask import Flask
from flask import request
from flask import json
from model import db
from model import User
from model import CreateDB
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
import os

# initate flask app
app = Flask(__name__)

@app.route('/')
def index():
	return 'This is test webapp for cmpe273-Assignment1\n'

@app.route('/v1')
def welcome():
	return 'Welcome to Assignment 1.\n This basic app is developer as a part of CMPE 273 Assignment. You should be able to run below tests on this application \n # POST should be working on /v1/expenses \n # checking GET on /v1/expenses/{id}\n# checking GET for invalid id\n# checking for put on /v1/expenses/{id}\n# checking if values have changed after PUT\n# checking for delete at /v1/expenses/{id}\n# checking if object still exists \n\n\n Please continue testing this as you wish!!!'

@app.route('/v1/expenses', methods=['GET'])
def show_user():
	#return json.dumps({'name':request.args['name']})
	try:
		user = User.query.filter_by(name=request.args['name']).first_or_404()
		return json.dumps({user.name:{ 'id': user.id, 'email': user.email, 'category': user.category,'description':user.description}})
	except IntegrityError:
		return json.dumps({})

# http://localhost/
@app.route('/insert', methods=['POST'])
def insert_user():
	try:
		user = User(request.json['name'],
				request.json['email'],
				request.json['category'],
				request.json['description'],
				request.json['link'],
				request.json['estimated_costs'],
				request.json['submit_date'])
		db.session.add(user)
		db.session.commit()
		return json.dumps({'status':True})
	except IntegrityError:
		return json.dumps({'status':False})

@app.route('/createtbl')
def createUserTable():
	try:
		db.create_all()
		return json.dumps({'status':True})
	except IntegrityError:
		return json.dumps({'status':False})

@app.route('/users')
def users():
	try:
		users = User.query.all()
		users_dict = {}
		for user in users:
			users_dict[user.name] = {
							'email': user.email,
							'phone': user.phone,
							'fax': user.fax
						    }

		return json.dumps(users_dict)
	except IntegrityError:
		return json.dumps({})

@app.route('/createdb')
def createDatabase():
	HOSTNAME = 'localhost'
	try:
		HOSTNAME = request.args['hostname']
	except:
		pass
	database = CreateDB(hostname = HOSTNAME)
	return json.dumps({'status':True})

@app.route('/info')
def app_status():
	return json.dumps({'server_info':application.config['SQLALCHEMY_DATABASE_URI']})

# run app service
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8082, debug=True)
