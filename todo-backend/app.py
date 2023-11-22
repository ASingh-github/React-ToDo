# app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import the CORS extension

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Create the SQLAlchemy instance

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    dueDate = db.Column(db.String)
    completed = db.Column(db.Integer, default=0)

# API endpoints
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_data = [{'id': task.id, 'title': task.title, 'dueDate': task.dueDate, 'completed': bool(task.completed)} for task in tasks]
    return jsonify(tasks_data)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    new_task = Task(title=title, dueDate=data.get('dueDate'))
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'id': new_task.id})

# Add similar routes for updating and deleting tasks

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
