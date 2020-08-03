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


