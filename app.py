import os
from flask import Flask, jsonify, request, make_response 
import sqlalchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Contact, Group
  
app = Flask(__name__)
##Setting the place for the db to run
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/change_this_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)
  
@app.route('/')
def allContacts():
    items = Contact.query.all()
    print(items)
    response =[]
    for i in items:
        brochacho = i.to_dict()
        response.append(brochacho)
    print(response)
    #response.to_dict_simple()
    return jsonify({"data": response})
    
    
@app.route('/addcontact', methods=['POST']) 
def add_contact():
    info= request.get_json() or {}
    
    groups = []
    for g in info["groups"]:
        group = Group.query.get(g)
        groups.append(group)
    item= Contact(
        full_name=info["full_name"], 
        email=info["email"], 
        address=info["address"], 
        phone=info["phone"],
        groups=groups
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"response": "ok"})
    
    
@app.route('/contacts/<int:id>', methods=['GET', 'PUT', 'DELETE'])   
def get_contact(id):
    if request.method == "GET":
        ele = Contact.query.get(id)
        my_guy = ele.to_dict()
        if id > 0:
            return jsonify({"status_code": 200, "data": my_guy})
    elif request.method == 'PUT':
        info= request.get_json() or {}
        ele = Contact.query.get(id)
        ele.full_name=info["full_name"]
        ele.email=info["email"]
        ele.address=info["address"]
        ele.phone=info["phone"]
        ele.groups=info["groups"]
        db.session.commit()
        return jsonify({"response": "ok"})
        
    else:
        ele = Contact.query.get(id)
        db.session.delete(ele)
        db.session.commit()
        return jsonify({"response": "ok"})
    
    response = jsonify({"error": 400, "message":"no member found" })
    response.status_code = 400
    return response
    
@app.route('/addgroup', methods=['POST']) 
def add_group():
    info= request.get_json() or {}
    item= Group(name=info["name"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"response": "ok"})
    
@app.route('/groups')
def allGroups():
    items = Group.query.all()
    response =[]
    for i in items:
        brochacho = i.to_dict()
        response.append(brochacho)
    return jsonify({"data": response})
    
@app.route('/groups/<int:id>', methods=['GET', 'PUT', 'DELETE'])   
def get_group(id):
    if request.method == "GET":
        ele = Group.query.get(id)
        my_group = ele.to_dict()
        if id > 0:
            return jsonify({"status_code": 200, "data": my_group})
    elif request.method == 'PUT':
        info= request.get_json() or {}
        ele = Group.query.get(id)
        ele.name=info["full_name"]
        db.session.commit()
        return jsonify({"response": "ok"})
        
    else:
        ele = Group.query.get(id)
        db.session.delete(ele)
        db.session.commit()
        return jsonify({"response": "ok"})
    
    response = jsonify({"error": 400, "message":"no member found" })
    response.status_code = 400
    return response
  
  
  
  
  
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))