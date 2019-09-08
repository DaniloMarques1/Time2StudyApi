from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS


app  = Flask(__name__)
db = SQLAlchemy(app)

from models import *


CORS(app)

app.config["JWT_SECRET_KEY"] = "thisissupersecret"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://danilo:1234@localhost/study"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:1234@localhost/Study"

#PYTHON ANYWHERE DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://daniloMarques:91425377Danilo@daniloMarques.mysql.pythonanywhere-services.com/daniloMarques$Study"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_recycle" : -1}


api = Api(app)



jwt = JWTManager(app)


class Index(Resource):
	def get(self):
            return make_response(jsonify({"message" : "Hello, world!"}), 200)


class Registrar(Resource):
	def post(self):
		name, email = request.json["name"], request.json["email"]
		password = generate_password_hash(request.json.get("password"))

		#caso ja possua um usuario com o e-mail passado, não deixar cadastrar
		if User.query.filter_by(email=email).first() is None:
			user = User(name=name, email=email, password=password)
			db.session.add(user)
			db.session.commit()
			response = jsonify({"message": "sucess"})
			response.status_code = 201
			return response
		else:
			response = jsonify({"message": "error"})
			response.status_code = 400
			return response


class Logar(Resource):
	def post(self):
		email, password = request.json["email"], request.json["password"]
		user = User.query.filter_by(email=email).first()
		if user is not None:
			if check_password_hash(user.password, password):
				user_identity = {"id_user": user.id_user,
                                    "name": user.name, "email": user.email}
				token = create_access_token(identity=user_identity, expires_delta=False)
				response = jsonify({"token": token})
				response.status_code = 200
				return response

		response = jsonify({"message": "email and/or password incorrect"})
		response.status_code = 401
		return response


class getUser(Resource):
	@jwt_required
	def get(self):
		response = jsonify(get_jwt_identity())
		response.status_code = 200
		return response


class add_task(Resource):
	def post(self):
		title, description, pomodoros_total, id_user = request.json["title"], request.json[
			"description"], request.json["pomodoro_total"], request.json["id_user"]

		task = Task(title=title, description=description,
		            id_user=id_user, pomodoros_total=int(pomodoros_total))
		db.session.add(task)
		db.session.commit()
		response = jsonify({"message": "success"})
		response.status_code = 201
		return response


class Tasks(Resource):
	@jwt_required
	def get(self):
		identity = get_jwt_identity()
		user = User.query.filter_by(id_user=identity["id_user"]).first()
		tasks_list = user.tasks
		retorno = []
		for task in tasks_list:
			if task.active == True:
				task_dict = {"id_task": task.id_task, "title": task.title, "description": task.description,
			                                    "current_pomodoros": task.current_pomodoros, "pomodoros_total": task.pomodoros_total, "active": task.active}
				retorno.append(task_dict)
		return make_response(jsonify(retorno), 200) 


class get_task(Resource):
	@jwt_required
	def get(self, id_task):
		user = get_jwt_identity()
		task = Task.query.filter_by(id_task=int(id_task)).first()
		if task is not None and task.id_user == user["id_user"] and task.active == True:
			response = {
				"id_task": task.id_task,
				"title": task.title,
				"description": task.description,
				"current_pomodoros": task.current_pomodoros,
				"pomodoros_total": task.pomodoros_total,
				"active" : task.active
			}
			response = jsonify(response)
			response.status_code = 200
			return response
		response = jsonify({"message": "Task not found"})
		response.status_code = 404
		return response


class update_task(Resource):
	@jwt_required
	def get(self, id_task):
		task = Task.query.filter_by(id_task=int(id_task)).first()
		if task.current_pomodoros < task.pomodoros_total:
			task.current_pomodoros += 1
			
		if task.current_pomodoros == task.pomodoros_total:
			task.active = False


		db.session.commit()
		
		response = {
                    "id_task": task.id_task,
                				"active": task.active,
                				"title": task.title,
                				"description": task.description,
                				"current_pomodoros": task.current_pomodoros,
                				"pomodoros_total": task.pomodoros_total
                }
		return make_response(jsonify(response), 200)


class get_history(Resource):
	@jwt_required
	def get(self):
		identity = get_jwt_identity()
		user = User.query.filter_by(id_user=identity["id_user"]).first()
		tasks_list = user.tasks
		retorno = []
		for task in tasks_list:
			if task.active == False:
				task_dict = {"id_task": task.id_task, "title": task.title, "description": task.description,
                                    "current_pomodoros": task.current_pomodoros, "pomodoros_total": task.pomodoros_total, "active": task.active}
				retorno.append(task_dict)
		response = jsonify({"tasks": retorno})
		response.status_code = 200
		return response


#definição de rotas
api.add_resource(Index, "/")
api.add_resource(Registrar, "/registrar")
api.add_resource(Logar, "/logar")
api.add_resource(getUser, "/user")
api.add_resource(add_task, "/addTask")
api.add_resource(Tasks, "/tasks")
api.add_resource(get_task, "/task/<int:d_task>")
api.add_resource(update_task, "/updateTask/<id_task>")
api.add_resource(get_history, "/history")


if __name__ == "__main__":
	app.run(debug=True)
