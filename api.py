# based on https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api

from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
import json

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


##
# Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


#######################################################
#######################################################

# curl http://localhost:5000/model --header "Content-Type: application/json" --request GET --data '{"aaaaa": "xd"}'

class About(Resource):
    # using GET to read about the project:
    # curl http://localhost:5000/about --request GET
    def get(self):
        return "IUM 20L Project. Wojciech Maciejewski, Wiktor Michalski"

api.add_resource(About, '/about')

class Model(Resource):
    # using GET to check the model in use:
    # curl http://localhost:5000/model --request GET
    def get(self):
        # TODO get a way of obtaining modelname
        return "placeholder"

    # using POST to choose the model:
    # curl http://localhost:5000/model --header "Content-Type: application/json" --request POST --data '{"name": "some_model", "path": "some_model.h5"}'
    def post(self):
        json_data = request.json
        # TODO if the file exisits, load it
        print(json_data['name'])
        return "Model successfully loaded.", 201
        # TODO otherwise
        return "Failed to load a model", 400

api.add_resource(Model, '/model')

class Predict(Resource):
    # using GET to get a prediction:
    # curl http://localhost:5000/model/predict --header "Content-Type: application/json" --request GET --data '{"last_browsed_product": "name"}'
    def get(self):
        # TODO get prediction from a model
        # TODO add data to the history [last_browsed_product, prediction, model_used]
        return None

api.add_resource(Predict, '/model/predict')

class History(Resource):
    # using GET to get history:
    # curl http://localhost:5000/model --request GET
    def get(self):
        # TODO get a way of obtaining history
        return None

api.add_resource(History, '/model/history')

if __name__ == '__main__':
    app.run(debug=True)
