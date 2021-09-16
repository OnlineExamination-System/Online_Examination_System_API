from flask import current_app
from flask_restful import Resource
import pymongo

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

