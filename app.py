from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy #configurar la conexion a mysql

from flask_marshmallow import Marshmallow

app = Flask(__name__)# se crea una variable app que es una instancia de flask donde voy a estar pasandole el name

app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:admin@localhost:3307/flaskmysql'# vamos a decirle donde esta la base de datos a esto se le conoce como recurso o unico. esta en la documentacion de sqlachemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #esto es para que no nos de una dvertencia cuando iniciemos el progrma

db = SQLAlchemy(app)#le decimos al orm que le pasaremos la configuracion que tiene app y me devuelve una instancia la cual sera guardada en db

ma = Marshmallow(app)# me permite definir una especie de esquema con el cual voy a estar interactuando  

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)# desde db importamos un metodo llamdo column el cual nos permitedefinir una columna
    title = db.Column(db.String(70),unique=True)
    description = db.Column(db.String(100))
    
    def __init__(self, title, description):
        self.title = title
        self.description = description


db.create_all()#lee todas nuestras clases y apartir de esas empieza a crear tablas

class TaskSchema(ma.Schema):# desde ma voy a crear un Schema
    class Meta:
        fields = ('id','title','description') #definir los campos que quiero obtener cadavez que interactue con el Squema.

task_schema = TaskSchema()# esto permite interactuar con las tareas eliminarlas etc
tasks_schema = TaskSchema(many=True)#me permite obtener multiples datos que cumplen con los valores

@app.route('/tasks', methods=['POST'])
def crated_task():
    
    print(request.json)

    title = request.json['title']
    description = request.json['description']
    
    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()
    
    return task_schema.jsonify(new_task) #respondemos la tarea al cliente para que vea lo que a guardado 


@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()#esto al final me devuelve todas las tareas y las guardo en una variable
    result = tasks_schema.dump(all_tasks)#    
    return jsonify(result)#lo que vas a retornar es una convercion desde un string a un json
    
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)#desde el modelo de tareas quiero obtener una sola tarea con el id
    return task_schema.jsonify(task)    

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)#llamamos al a tarea
    
    title = request.json['title']
    description = request.json['description']
    
    task.title = title
    task.description = description
    
    db.session.commit()#guardo la tarea
    return task_schema.jsonify(task)
    

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    
    db.session.commit()
    
    return task_schema.jsonify(task)
  
if __name__ == "__main__":
    app.run(debug=True)
