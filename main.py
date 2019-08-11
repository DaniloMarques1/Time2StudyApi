from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app  = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "thisissupersecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:12345@localhost/Study"

api = Api(app)

db = SQLAlchemy(app)

jwt = JWTManager(app)

#Models
class User(db.Model):
	id_user = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	email = db.Column(db.String(40), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	tasks = db.relationship("Task", backref="task", lazy=True)

class Task(db.Model):
	id_task = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text, nullable=True)
	current_pomodoros = db.Column(db.Integer, default=0, nullable=False)
	pomodoros_total = db.Column(db.Integer, nullable=False)
	active = db.Column(db.Boolean, default=True)
	id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"))


class Registrar(Resource):
	def post(self):
		name, email = request.json["name"], request.json["email"]
		password = generate_password_hash(request.json.get("password"))

		#caso ja possua um usuario com o e-mail passado, não deixar cadastrar
		if User.query.filter_by(email=email).first() is None:
			user = User(name=name, email=email, password=password)
			db.session.add(user)
			db.session.commit()
			return make_response({"message" : "success"}, 201)
		else:
			return make_response({"message" : "email has already been used"}, 400)

class Logar(Resource):
	def post(self):
		email, password = request.json["email"], request.json["password"]
		user = User.query.filter_by(email=email).first()
		if user is not None:
			if check_password_hash(user.password, password):
				user_identity = {"id_user" : user.id_user, "name" : user.name, "email" : user.email}
				token = create_access_token(identity=user_identity, expires_delta=False)
				return make_response({"token" : token}, 200)

		return make_response({"message" : "email and/or password incorrect"}, 401)

class getUser(Resource):
	@jwt_required
	def get(self):
		return make_response(get_jwt_identity(), 200)

class add_task(Resource):
	def post(self):
		print("Opa")
		title, description, pomodoros_total, id_user = request.json["title"], request.json["description"], request.json["pomodoro_total"], request.json["id_user"]
		task = Task(title=title, description=description, id_user=id_user, pomodoros_total=pomodoros_total)
		db.session.add(task)
		db.session.commit()
		return make_response({"message" : "success"}, 201)

class Tasks(Resource):
	@jwt_required
	def get(self):
		identity = get_jwt_identity()
		user = User.query.filter_by(id_user=identity["id_user"]).first()
		tasks_list = user.tasks
		retorno = []
		for task in tasks_list:
			if task.active == True:
				task_dict = {"id_task" : task.id_task, "title" : task.title, "description" : task.description, "current_pomodoros" : task.current_pomodoros, "pomodoros_total" : task.pomodoros_total, "active" : task.active}
				retorno.append(task_dict)
		return make_response({"tasks" : retorno}, 200)

class get_task(Resource):
	@jwt_required
	def get(self, id_task):
		user = get_jwt_identity()
		print(user)
		task = Task.query.filter_by(id_task=id_task).first()
		if task is not None and task.id_user == user["id_user"] and task.active == True:
			response = {
				"id_task" : task.id_task,
				"title" : task.title,
				"description" : task.description,
				"current_pomodoros" : task.current_pomodoros,
				"pomodoros_total" : task.pomodoros_total
			}
			return make_response(response, 200)
		return make_response({"message" : "Task not found"}, 404)

class update_task(Resource):
	@jwt_required
	def get(self, id_task):
		task = Task.query.filter_by(id_task=id_task).first()
		if task.current_pomodoros < task.pomodoros_total:
			task.current_pomodoros += 1
		if task.current_pomodoros == task.pomodoros_total:
			task.active = False

		response = {
				"id_task" : task.id_task,
				"active" : task.active,
				"title" : task.title,
				"description" : task.description,
				"current_pomodoros" : task.current_pomodoros,
				"pomodoros_total" : task.pomodoros_total
			}
		db.session.commit()
		return make_response({"task" : response}, 200)

class get_history(Resource):
	@jwt_required
	def get(self):
		identity = get_jwt_identity()
		user = User.query.filter_by(id_user=identity["id_user"]).first()
		tasks_list = user.tasks
		retorno = []
		for task in tasks_list:
			if task.active == False:
				task_dict = {"id_task" : task.id_task, "title" : task.title, "description" : task.description, "current_pomodoros" : task.current_pomodoros, "pomodoros_total" : task.pomodoros_total, "active" : task.active}
				retorno.append(task_dict)
		return make_response({"tasks" : retorno}, 200)

api.add_resource(Registrar, "/registrar")
api.add_resource(Logar, "/logar")
api.add_resource(getUser, "/user")
api.add_resource(add_task, "/addTask")
api.add_resource(Tasks, "/tasks")
api.add_resource(get_task, "/task/<id_task>")
api.add_resource(update_task, "/updateTask/<id_task>")
api.add_resource(get_history, "/history")

if __name__ == "__main__":
	app.run(debug=True, port=5000)
