from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__, static_url_path='/static')
app.secret_key = "supersecreto"

# Reemplaza con tu URL real de base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///tareas.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    completada = db.Column(db.Boolean, default=False)
    fecha_vencimiento = db.Column(db.Date, nullable=True)
    prioridad = db.Column(db.String(50), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship("Usuario", backref="tareas")

with app.app_context():
    db.create_all()

# Rutas
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/autenticacion", methods=["POST"])
def autenticacion():
    accion = request.form["accion"]
    usuario = request.form["usuario"]
    contrasena = request.form["password"]

    if accion == "registro":
        if Usuario.query.filter_by(nombre=usuario).first():
            flash("El nombre de usuario ya está registrado.")
            return redirect("/")
        if len(contrasena) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.")
            return redirect("/")
        contrasena_hash = generate_password_hash(contrasena)
        nuevo_usuario = Usuario(nombre=usuario, contrasena=contrasena_hash)
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Usuario registrado exitosamente.")
        return redirect("/")
    
    elif accion == "login":
        user = Usuario.query.filter_by(nombre=usuario).first()
        if user and check_password_hash(user.contrasena, contrasena):
            session["usuario_id"] = user.id
            flash("Inicio de sesión exitoso.")
            return redirect("/tareas")
        else:
            flash("Credenciales incorrectas.")
            return redirect("/")

    else:
        flash("Acción inválida.")
        return redirect("/")

@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    contrasena_plana = request.form["contrasena"]

    if Usuario.query.filter_by(nombre=nombre).first():
        flash("El nombre de usuario ya está registrado.")
        return redirect("/")
    if len(contrasena_plana) < 6:
        flash("La contraseña debe tener al menos 6 caracteres.")
        return redirect("/")

    contrasena_hash = generate_password_hash(contrasena_plana)
    nuevo_usuario = Usuario(nombre=nombre, contrasena=contrasena_hash)
    db.session.add(nuevo_usuario)
    db.session.commit()
    flash("Usuario registrado exitosamente.")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form["usuario"]
    password = request.form["password"]
    user = Usuario.query.filter_by(nombre=usuario).first()

    if user and check_password_hash(user.contrasena, password):
        session["usuario_id"] = user.id
        flash("Inicio de sesión exitoso.")
        return redirect("/tareas")
    else:
        flash("Credenciales incorrectas.")
        return redirect("/")

@app.route("/logout")
def logout():
    session.pop("usuario_id", None)
    flash("Sesión cerrada.")
    return redirect("/")

@app.route("/tareas")
def tareas():
    if "usuario_id" in session:
        return redirect("/tareas_p")
    else:
        return redirect("/")

@app.route("/tareas_p")
def tareas_p():
    if "usuario_id" not in session:
        return redirect("/")
    usuario_id = session["usuario_id"]
    tareas = Tarea.query.filter_by(usuario_id=usuario_id).all()
    return render_template("tareas_p.html", tareas=tareas)

@app.route("/crear_tarea", methods=["POST"])
def crear_tarea():
    if "usuario_id" not in session:
        return redirect("/")
    
    descripcion = request.form["descripcion"]
    fecha_vencimiento = request.form.get("fecha_vencimiento")
    prioridad = request.form.get("prioridad")
    usuario_id = session["usuario_id"]

    fecha_obj = datetime.strptime(fecha_vencimiento, "%Y-%m-%d") if fecha_vencimiento else None

    nueva_tarea = Tarea(
        descripcion=descripcion,
        fecha_vencimiento=fecha_obj,
        prioridad=prioridad,
        usuario_id=usuario_id
    )

    db.session.add(nueva_tarea)
    db.session.commit()
    flash("Tarea creada exitosamente.")
    return redirect("/tareas_p")

@app.route("/editar_tarea/<int:id>", methods=["POST"])
def editar_tarea(id):
    if "usuario_id" not in session:
        return redirect("/")

    tarea = Tarea.query.get_or_404(id)

    if tarea.usuario_id != session["usuario_id"]:
        flash("No tienes permiso para editar esta tarea.")
        return redirect("/tareas_p")

    tarea.descripcion = request.form["descripcion"]
    tarea.fecha_vencimiento = request.form.get("fecha_vencimiento") or None
    tarea.prioridad = request.form.get("prioridad")
    tarea.completada = "completada" in request.form

    if tarea.fecha_vencimiento:
        tarea.fecha_vencimiento = datetime.strptime(tarea.fecha_vencimiento, "%Y-%m-%d")

    db.session.commit()
    flash("Tarea actualizada exitosamente.")
    return redirect("/tareas_p")

@app.route("/eliminar_tarea/<int:id>", methods=["POST"])
def eliminar_tarea(id):
    if "usuario_id" not in session:
        return redirect("/")

    tarea = Tarea.query.get_or_404(id)

    if tarea.usuario_id != session["usuario_id"]:
        flash("No tienes permiso para eliminar esta tarea.")
        return redirect("/tareas_p")

    db.session.delete(tarea)
    db.session.commit()
    flash("Tarea eliminada exitosamente.")
    return redirect("/tareas_p")



if __name__ == "__main__":
    app.run(debug=True)
