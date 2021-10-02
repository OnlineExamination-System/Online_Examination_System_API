from flask import current_app
from flask_restful import Resource, request
import pymongo
from common.email_service import EmailSend


class Report(Resource):
    def get(self):
        try:
            connect = pymongo.MongoClient(current_app.config["MONGO_URL"])
            selectDb = connect[current_app.config["DB_NAME"]]
            selectCollection1 = selectDb["students"]
            selectCollection2 = selectDb["results"]
            try:
                student = list(selectCollection1.find({}, {"_id": 0}))
                result = list(selectCollection2.find({}, {"_id": 0}))
                rec_email = request.args.get("email")
                html=""
                Subject = "CONSOLIDATED RESULT GENERATED - Online Examination System"
                html+="""<!DOCTYPE html>
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
                                        <tr><th>Roll no</th><th>Name</th><th>Student_id</th><th>E-mail</th><th>Test taken at</th><th>Total marks scored</th></tr>"""
                for i in student:
                    html+="""<tr><td>"""
                    html+=i["roll_no"]
                    html+="""</td><td>"""
                    html+=i["name"]
                    html+="""</td><td>"""
                    html+=i["student_id"]
                    html+="""</td><td>"""
                    html+=i["email"]
                    html+="""</td><td>"""
                    for j in result:
                        if j["student_id"]==i["student_id"]:
                            break
                    html+=str(j["time"])
                    html+="""</td><td>"""
                    html+=str(j["marks"])
                    html+="""</td></tr>"""
                html+="""</table>
                            </body>
                            </html>"""
                connect.close()
                response = EmailSend().sendEmailWithHtml(subject=Subject, reciever_email=rec_email,
                                                         html=html)
                return {"code": 200, "message": "Data served"}, 200
            except Exception as e:
                return {"code": 211, "message": "Not found or bad request : " + str(e)}, 211
        except Exception as e:
            return {"code": 210, "message": "Failed to connect to Mongo DB : " + str(e)}, 210
