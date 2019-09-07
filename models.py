from main import db

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
