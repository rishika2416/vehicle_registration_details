# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Before running the api on host create the db by using cmd:
#>>>from temp import db
#>>>db.create_all()

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    rtoID = db.Column(db.String(10), unique=True, primary_key=True)
    ownerName = db.Column(db.String(10), nullable=False)
    vehicleName = db.Column(db.String(10), nullable=False)
    vehicleAge = db.Column(db.Integer, nullable=False)
    regNo = db.Column(db.String(10), nullable=False)
    regAuth = db.Column(db.String(10), nullable=False)
    regDate = db.Column(db.String(10), nullable=False)
    vehicleClass = db.Column(db.String(10), nullable=False)
    fuelType = db.Column(db.String(10), nullable=False)
    chasisNo = db.Column(db.String(10), nullable=False)
    engineNo = db.Column(db.String(10), nullable=False)
    vehicleCapacity = db.Column(db.Integer, nullable=False)

    def __init__(self, rtoID, ownerName, vehicleName, vehicleAge, regNo, regAuth, regDate, vehicleClass, fuelType, chasisNo, engineNo, vehicleCapacity):
        self.rtoID = rtoID
        self.ownerName = ownerName
        self.vehicleName = vehicleName
        self.vehicleAge = vehicleAge
        self.regNo = regNo
        self.regAuth = regAuth
        self.regDate = regDate
        self.vehicleClass = vehicleClass
        self.fuelType = fuelType
        self.chasisNo = chasisNo
        self.engineNo = engineNo
        self.vehicleCapacity = vehicleCapacity


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('rtoID', 'ownerName', 'vehicleName', 'vehicleAge', 'regNo', 'regAuth', 'regDate', 'vehicleClass', 'fuelType', 'chasisNo', 'engineNo', 'vehicleCapacity')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/',methods=['GET'])


@app.route("/user", methods=["POST"])
def add_user():
    rtoID = request.json['rtoID']
    ownerName = request.json['ownerName']
    vehicleName = request.json['vehicleName']
    vehicleAge = request.json['vehicleAge']
    regNo = request.json['regNo']
    regAuth = request.json['regAuth']
    regDate = request.json['regDate']
    vehicleClass = request.json['vehicleClass']
    fuelType = request.json['fuelType']
    chasisNo = request.json['chasisNo']
    engineNo = request.json['engineNo']
    vehicleCapacity = request.json['vehicleCapacity']

    new_user = User(rtoID, ownerName, vehicleName, vehicleAge, regNo, regAuth, regDate, vehicleClass, fuelType, chasisNo, engineNo, vehicleCapacity)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route("/user/<rtoNo>", methods=["GET"])
def user_detail(rtoNo):
    user = User.query.filter_by(rtoID=rtoNo).first()
    return user_schema.jsonify(user)


@app.route("/user/<rtoNo>", methods=["PUT"])
def user_update(rtoNo):
    user = User.query.filter_by(rtoID=rtoNo).first()
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


@app.route("/user/<rtoNo>", methods=["DELETE"])
def user_delete(rtoNo):
    user = User.query.filter_by(rtoID=rtoNo).first()
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

if __name__ == '__main__':
    app.run(debug=True,port=8080)
