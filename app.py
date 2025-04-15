from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__,static_url_path='/static')
app.secret_key = "supersecreto"  # Necesario para usar sesiones y mensajes flash

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Usuario - CREACION DE TABLAS
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    contrasena = db.Column(db.String(255)) 

# Modelo Tarea
class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    completada = db.Column(db.Boolean, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    usuario = db.relationship("Usuario", backref="tareas")

# Crear las tablas si no existen
with app.app_context(): 
    db.create_all()

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# Guardar nuevo usuario
@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    contrasena_plana = request.form["contrasena"]
    contrasena_hash = generate_password_hash(contrasena_plana)

    nuevo_usuario = Usuario(nombre=nombre, contrasena=contrasena_hash)
    db.session.add(nuevo_usuario)
    db.session.commit()
    flash("Usuario registrado exitosamente.")
    return redirect("/")

# Iniciar sesión
@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    password = request.form["password"]

    user = Usuario.query.filter_by(nombre=usuario).first()

    if user and check_password_hash(user.contrasena, password):
        session["usuario_id"] = user.id  # Guardamos el usuario_id en la sesión
        flash("Inicio de sesión exitoso.")
        return redirect("/tareas")
    else:
        flash("Credenciales incorrectas.")
        return redirect("/")

# Ruta protegida
@app.route("/tareas")
def tareas():
    if "usuario_id" in session:
        return redirect("/tareas_p")  # Redirige a tareas_p si el usuario está logueado
    else:
        return redirect("/")

# Cerrar sesión
@app.route("/logout")
def logout():
    session.pop("usuario_id", None)  # Elimina usuario_id de la sesión
    flash("Sesión cerrada.")
    return redirect("/")

# Ruta para mostrar tareas
@app.route("/tareas_p")
def tareas_p():
    if "usuario_id" not in session:
        return redirect("/")  # Si no está logueado, redirige al login
    
    usuario_id = session["usuario_id"]
    tareas = Tarea.query.filter_by(usuario_id=usuario_id).all()  # Obtener tareas del usuario
    return render_template("tareas_p.html", tareas=tareas)

@app.route("/crear_tarea", methods=["POST"])
def crear_tarea():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión primero.")
        return redirect("/")  # Si no está logueado, redirige al login
    
    descripcion = request.form["descripcion"]
    usuario_id = session["usuario_id"]
    
    # Crear una nueva tarea
    nueva_tarea = Tarea(descripcion=descripcion, usuario_id=usuario_id)
    db.session.add(nueva_tarea)
    db.session.commit()
    
    flash("Tarea creada exitosamente.")
    return redirect("/tareas_p")  # Redirige a la página de tareas
