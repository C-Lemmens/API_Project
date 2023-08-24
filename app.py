from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos_with_auth.db'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth2Provider(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(60))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(128))
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# OAuth setup (simplified)
class Client(db.Model):
    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    _redirect_uris = db.Column(db.Text)

@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()

@app.before_request
def before_request():
    # Placeholder logic to set g.user based on OAuth token (implement this)
    g.user = None

@app.route('/todos', methods=['GET'])
def get_todos():
    status = request.args.get('status', None)
    if status is not None:
        status = True if status.lower() == 'true' else False
        todos = Todo.query.filter_by(completed=status).all()
    else:
        todos = Todo.query.all()

    return jsonify({'todos': [{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in todos]})

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'todo': {'id': todo.id, 'task': todo.task, 'completed': todo.completed}})

@app.route('/todos', methods=['POST'])
def add_todo():
    new_todo_data = request.get_json()
    new_todo = Todo(task=new_todo_data['task'], completed=new_todo_data.get('completed', False))
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'todo': {'id': new_todo.id, 'task': new_todo.task, 'completed': new_todo.completed}}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Not found'}), 404
    updated_data = request.get_json()
    todo.task = updated_data.get('task', todo.task)
    todo.completed = updated_data.get('completed', todo.completed)
    db.session.commit()
    return jsonify({'todo': {'id': todo.id, 'task': todo.task, 'completed': todo.completed}})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    plaintext_pw = data.get('password')
    hashed_pw = bcrypt.hashpw(plaintext_pw.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password=hashed_pw.decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password').encode('utf-8')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password, user.password.encode('utf-8')):
        # Generate and return an access token here
        return jsonify({'message': 'Logged in'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)
