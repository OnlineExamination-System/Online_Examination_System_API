from flask import current_app
from flask_restful import Resource, request
import pymongo
import uuid
from datetime import datetime
import ast
from common.email_service import EmailSend


class Questions(Resource):
    def get(self):
        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection = selectDb["questions"]
            try:
                x = list(selectCollection.find({}, {"_id": 0}))
                connect.close()
                return {"code": 200, "message": "Data served", "data": x}, 200
            except Exception as e:
                return {"code": 211, "message": "Not found or bad request : " + str(e)}, 211
        except Exception as e:
            return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 210


class Submission(Resource):
    def post(self):
        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection1 = selectDb["students"]
            selectCollection2 = selectDb["results"]
            try:
                student_id = "PR" + str(uuid.uuid4().int)
                data = request.get_data()
                dict_str = data.decode("UTF-8")
                mydata = ast.literal_eval(dict_str)
                student = {
                    "student_id": student_id[0:5],
                    "name": mydata["name"],
                    "email": mydata["email"],
                    "roll_no": mydata["roll_no"],
                    "class": mydata["class"]
                }
                result = {
                    "student_id": student_id[0:5],
                    "time": datetime.now(),
                    "marks": mydata["marks"]
                }
                y = selectCollection1.insert_one(student)
                z = selectCollection2.insert_one(result)

                if y.inserted_id and z.inserted_id:
                    try:
                        rec_email = mydata["email"]
                        Subject = "RESULT PUBLISHED - Online Examination System"
                        html1 = """<!DOCTYPE html>
                                    <html>
                                    <head>
                                        <title>Online Examination System Results</title>
                                        <style>
                                            td
                                            {
                                                color:#3E6FCC;
                                            }
                                        </style>
                                    </head>
                                    <body bgcolor="#CDC392">
                                        <center><u><h1 style="font-family: Arial">Online Examination System</h1></center>
                                        </u><center><h2 style="font-family: Arial"><u>Results</u></h2></center>
                                        <table style="font-family: Roboto" align= "center" border="3" cellspacing="5" cellpadding="5" bgcolor="#E8E5DA">
                                            <tr><td>Test taken at</td><td>"""

                        html2 = """</td></tr>
		                            <tr><td>Name</td><td>"""
                        html3 = """</td></tr>
		                            <tr><td>Student Reference ID</td><td>"""
                        html4 = """
                               </td></tr>
		                       <tr><td>E-mail</td><td>
                               """
                        html5 = """</td></tr>
		                            <tr><td>Roll no</td><td>"""
                        html6 = """</td></tr>
                        		            <tr><td>Class</td><td>"""
                        html7 = """ </td></tr>
		                            <tr><td>Total marks scored</td><td>"""
                        html8 = """ </td></tr>
                                        </table>
                                    </body>
                                    </html>"""

                        html_content = html1 + str(datetime.now()) + html2 + mydata["name"] + html3 + student_id[0:5] + html4 + mydata["email"] + html5 + mydata["roll_no"] + html6 +mydata["class"]+html7+ str(mydata["marks"]) + html8

                        response = EmailSend().sendEmailWithHtml(subject=Subject, reciever_email=rec_email,
                                                                 html=html_content)
                        return {"code": 201, "message": "Successfully Submitted your response "}, 201

                    except Exception as e:
                        return {"code": 213, "message": "Submission not Successfull : " + str(e)}, 213

            except Exception as e:
                return {"code": 213, "message": "Submission not Successfull : " + str(e)}, 213
        except Exception as e:
            return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 210
