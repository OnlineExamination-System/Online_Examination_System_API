from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "staging":
    app.config.from_object("config.StagingConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")



import resources.quiz.attempt as attempt
api.add_resource(attempt.Questions,"/attempt")
api.add_resource(attempt.Submission,"/submit")

import resources.quiz.evaluation as eva
api.add_resource(eva.Report,"/report")


if __name__ == '__main__':
    app.run(debug=True,port=app.config["API_PORT"])
