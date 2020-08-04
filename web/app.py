"""
Registration of a user
Each user gets 10 tokens
Store a sentence on our database for 1 token 
Retrieve his stored sentence on out database for 1 token
"""
from flask import Flask, jsonify, request
from flask_restful  import Api, Resource 
import os
import bcrypt

from pymongo import MongoClient

app = Flask(__name__) 
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def  post(self):
        #Step 1 is to get posted data  by the user 
        postedData = request.get_json()

        #Get the the data
        username = postedData["username"]
        password = postedData["password"]

        #hash(password + salt) = dljbgnhbrtbgnernj
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens": 10
        })

        retJson = {
            "status" : 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)

def verifyPw(username, password):
    hashed_pw = users.find({
        "Username":username  
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]

    return tokens

class Store(Resource):
    def post(self):
        #Step 1 is to get posted data  by the user 
        postedData = request.get_json()        

        #Step 2 is to read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #Step 3 verify the username pw match
        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retJson = {
                "status" : 302
            }
            return jsonify(retJson)

        #Step 4 verify the tokens
        num_tokens = countTokens(username)

        if num_tokens <= 0:
            retJson = {
                "status" : 301
            }
            return jsonify(retJson)

        #Step 5 store the sentence and return 200 OK
        users.update_one({
            "Username" : username
        }, {
            "$set": {
                "Sentence" : sentence,
                "Tokens": num_tokens - 1
            }
        })

        retJson = { 
            "status" : 200,
            "msg" :  "Sentence saved"
        }

        return jsonify(retJson)

class Get(Resource):
    def post(self):
        postedData = request.get_json()        

        #Step 2 is to read the data
        username = postedData["username"]
        password = postedData["password"]

        #Step 3 verify the username pw match
        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retJson = {
                "status" : 302
            }
            return jsonify(retJson)
        
        num_tokens = countTokens(username)

        if num_tokens <= 0:
            retJson = {
                "status" : 301
            }
            return jsonify(retJson)
        
        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        retJson = {
            "status": 200,
            "sentence": sentence
        }

        return jsonify(retJson)

api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

if __name__=="__main__":
    app.run(host='0.0.0.0')





"""
from flask import Flask, jsonify, request
from flask_restful  import Api, Resource 
import os

from pymongo import MongoClient

app = Flask(__name__) 
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert_one({
    "num_of_users":0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_of_users"]
        new_num  = prev_num + 1
        UserNum.update({}, {"$set":{"num_of_users":new_num}})
        return str("Hello User " + str(new_num))

def checkPostedData(postedData, functionName):
    if (functionName == "add"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else: 
            return 200
    elif(functionName == "subtract"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else: 
            return 200

    elif(functionName == "divide"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif postedData["y"] == 0 :
            return 302
        else: 
            return 200

    elif(functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else: 
            return 200    

class Add(Resource):
    def post(self):
        postedData = request.get_json()
         
        status_code = checkPostedData(postedData, "add")
        if(status_code!=200):
            retJson = {
                "Message" : "An Error Happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        #If I am here, then status code is 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        ret = x + y

        retMap = {
            'Message': 'Successfully Added',
            'Data': ret,
            'Status Code': 200
        }
        return jsonify(retMap)
    pass


class Subtract(Resource):
    def post(self):
        postedData = request.get_json()
         
        status_code = checkPostedData(postedData, "subtract")
        if(status_code!=200):
            retJson = {
                "Message" : "An Error Happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        #If I am here, then status code is 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        ret = x - y

        retMap = {
            'Message': 'Successfully Subtracted',
            'Data': ret,
            'Status Code': 200
        }
        return jsonify(retMap)
    pass

class Divide(Resource):
    def post(self):
        postedData = request.get_json()
         
        status_code = checkPostedData(postedData, "divide")
        if(status_code!=200):
            retJson = {
                "Message" : "An Error Happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        #If I am here, then status code is 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        ret = x/y

        retMap = {
            'Message': 'Successfully Divided',
            'Data': ret,
            'Status Code': 200
        }
        return jsonify(retMap)
    pass

class Multiply(Resource):
    def post(self):
        postedData = request.get_json()
         
        status_code = checkPostedData(postedData, "multiply")
        if(status_code!=200):
            retJson = {
                "Message" : "An Error Happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        #If I am here, then status code is 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        ret = x * y

        retMap = {
            'Message': 'Successfully Multiplied',
            'Data': ret,
            'Status Code': 200
        }
        return jsonify(retMap)
    pass

api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Divide, "/divide")
api.add_resource(Multiply, "/multiply")
api.add_resource(Visit, "/visits")

@app.route('/')
def hello_world(): 
    return "Hello World"

if __name__=="__main__":
    app.run(host='0.0.0.0')
"""

