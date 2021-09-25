from flask import current_app
from flask_restful import Resource,request
import pymongo
import uuid
from datetime import datetime
import ast

class Questions(Resource):
    def get(self):
            try:
                connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
                selectDb = connect[current_app.config["DB_NAME"]]
                selectCollection = selectDb["questions"]
                try:
                    x = list(selectCollection.find({},{"_id":0}))
                    connect.close()
                    return {"code": 200, "message": "Data served", "data": x},200
                except Exception as e:
                    return {"code": 211, "message": "Not found or bad request : " + str(e)},211
            except Exception as e:
                return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)},210

class Submission(Resource):
    def post(self):
        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection1 = selectDb["students"]
            selectCollection2 = selectDb["results"]
            try:
                student_id = "PR"+str(uuid.uuid4())
                data = request.get_data()
                dict_str = data.decode("UTF-8")
                mydata = ast.literal_eval(dict_str)
                student = {
                    "student_id": student_id,
                    "name": mydata["name"],
                    "email": mydata["email"],
                    "roll_no": mydata["roll_no"],
                    "class": mydata["class"]
                }
                result = {
                    "student_id": student_id,
                    "time" : datetime.now(),
                    "marks": mydata["marks"]
                }
                y = selectCollection1.insert_one(student)
                z = selectCollection2.insert_one(result)

                if y.inserted_id and z.inserted_id:

                    return {"code": 201, "message": "Successfully Submitted your response"},201

            except Exception as e:
                return {"code": 213, "message": "Submission not Successfull : " + str(e)}, 213
        except Exception as e:
            return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 210
