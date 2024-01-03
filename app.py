from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tareas.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False, default='incomplete')

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        tarea = request.json.get('tarea')
        if tarea:
            nueva_tarea = Tarea(name=tarea)
            db.session.add(nueva_tarea)
            db.session.commit()
            return jsonify({'message': 'Tarea agregada correctamente'})
    return render_template('tareas.html')

@app.route("/tasks")
def tasks():
    lista_tareas = Tarea.query.all()
    tareas = [{'id': tarea.id, 'name': tarea.name} for tarea in lista_tareas]
    return jsonify(tareas)

@app.route("/delete/<int:id>", methods=['DELETE'])
def delete_task(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    return jsonify({'message': 'Tarea eliminada'})

@app.route("/complete/<int:id>", methods=['PATCH'])
def complete_task(id):
    tarea = Tarea.query.get_or_404(id)
    tarea.state = 'complete'
    db.session.commit()
    return jsonify({'message': 'Tarea marcada como completada'})

if __name__ == "__main__":
    app.run(debug=True)
