from flask import Flask, jsonify, request
from flask_restful import Api, Resource  
from pymongo import MongoClient
import os
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]

def UserExist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username) :
            retJson = {
                "status" : 301,
                "msg" : "Username Exists"
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6
        })

        retJson = {
            "status": 200,
            "msg": "You've successfully signed up to the API"
        }

        return jsonify(retJson)

api.add_resource(Register, '/register')

if __name__ == "__main__":
    app.run(host='0.0.0.0')

