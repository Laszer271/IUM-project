# based on https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api

from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from models import ModelContainer
import json

app = Flask(__name__)
api = Api(app)

model_container = None

class About(Resource):
    # using GET to read about the project:
    # curl http://localhost:5000/about --request GET
    def get(self):
        return "IUM 20Z Project. Wojciech Maciejewski, Wiktor Michalski"

api.add_resource(About, '/about')

class Model(Resource):
    # using GET to check the model in use:
    # curl http://localhost:5000/model --request GET
    def get(self):
        # TODO get a way of obtaining modelname'
        return jsonify(model_container.selected_model.__name__())

    # using POST to choose the model:
    # curl http://localhost:5000/model --header "Content-Type: application/json" --request POST --data '{"path": "some_model.h5"}'
    def post(self):
        json_data = request.json
        model_container.load_model(json_data["path"])

api.add_resource(Model, '/model')

class Predict(Resource):
    # using GET to get a prediction:
    # curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": id}'
    def get(self):
        json_data = request.json
        predictions = model_container.predict(json_data["last_browsed_product"])
        return jsonify(predictions)

api.add_resource(Predict, '/model/predict')

class History(Resource):
    # using GET to get history:
    # curl http://localhost:5000/model --request GET
    def get(self):
        return jsonify(model_container.history)

api.add_resource(History, '/model/history')

class AB(Resource):
    # using GET to check if AB is used:
    # curl http://localhost:5000/model/ab/status --request GET
    def get(self):
        status = model_container.AB
        return jsonify({"AB_status": status})

    # using POST to activate AB:
    # curl http://localhost:5000/model/ab/status --header "Content-Type: application/json" --request POST --data '{"status": True}'
    def post(self):
        json_data = request.json
        if model_container.complex_model == None:
            return "Failed to change AB status, complex model not loaded.", 400
        if type(json_data["status"]) == type(True):
            model_container.AB = json_data["status"]
            return "AB status successfully set.", 201
        return "Failed to change AB status.", 400

api.add_resource(AB, '/model/ab')

if __name__ == '__main__':
    container = ModelContainer()
    app.run(debug=True)
