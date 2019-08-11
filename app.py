from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_jwt import JWT, jwt_required, current_identity

engine = create_engine("mysql://root:12345@localhost/time2study")

db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super-secret'

CORS(app)

#Classe para ser usada pelo jwt
class User:
	def __init__(self, id, name, email):
		self.id = id
		self.name = name
		self.email = email

@app.route("/")
def index():
	data = db.execute("SELECT * FROM User").fetchall()
	print(data)
	return "opa"

@app.route("/api/registrar", methods=["POST"])
def registrar():
	'''
	Recebera os dados enviados via post do front end e tentara inserir ao banco de dados
	'''
	name, email, password = request.form.get("name"), request.form.get("email"), request.form.get("password")
	result = db.execute("SELECT * FROM User WHERE email = :email", {"email" : email}).fetchone()
	if not result:
		a = db.execute("INSERT INTO User(name, email,password) VALUES(:name, :email, :password)", {"name" : name, "email" : email,"password" : password})
		db.commit()
		json = {"success" : True}
	else:
		json  = {"success" : False}

	return jsonify(json)

def logar(email, password):
	'''
	verifica se tem algum registro com o email e senha passados
	'''
	# email, password = request.form.get("email"), request.form.get("password")
	result = db.execute("SELECT * FROM User WHERE email = :email AND password = :password", {"email" : email, "password" : password}).fetchone()
	if result is not None:
		user = User(result[0], result[1], result[2])
		return user
	else:
		return None
	# return jsonify(json)

def identity(payload):
	user_id = payload["identity"]
	result = db.execute("SELECT * FROM User WHERE id_user = :user_id", {"user_id" : user_id}).fetchone()
	print("RESULT", result)
	if result is not None:
		response = {"id" : result[0], "name" : result[1], "email" : result[2]}
		return (dict(response))

jwt = JWT(app, logar, identity)

@app.route("/user")
@jwt_required()
def user():
	print(type(dict(current_identity)))
	return jsonify(dict(current_identity))

'''
	Endpoints referente as atividades
'''

@app.route("/api/addTask", methods=["POST"])
def add_task():
	'''
	adiciona uma nova atividade no banco de dados
	'''
	id_user, title, qtd_pomodoros, description = request.form.get("id_user"), request.form.get("title"), request.form.get("qtd_pomodoros"), request.form.get("description")
	result =  db.execute("INSERT INTO Task(id_user, title, qtd_pomodoros, description, finished) VALUES(:id_user,:title, :qtd_pomodoros, :description, DEFAULT)", {"id_user" : id_user, "title" : title, "qtd_pomodoros" : qtd_pomodoros, "description" : description})
	db.commit()
	
	return jsonify({"success" : True})

@app.route("/api/viewTasks/<id_user>", methods=["GET"])
def view_tasks(id_user):
	'''
	retorna as tasks com finished == false do banco
	retorno um json no formato {tasks: [lista com as tasks]}
	'''
	result = db.execute("SELECT * FROM Task WHERE finished = '0' and id_user = :id_user", {"id_user" : id_user}).fetchall()
	tasks = []
	for i in result:
		tasks.append(list(i))
	return jsonify({"tasks" : tasks})

if __name__ == "__main__":
	app.run(debug=True)

