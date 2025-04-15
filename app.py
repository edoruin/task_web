from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "supersecreto"  # Necesario para usar sesiones y mensajes flash

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True)
    contrasena = db.Column(db.String(255)) 

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
        session["usuario"] = usuario
        return redirect("/tareas")
    else:
        return redirect("/")


# Ruta protegida (opcional)
@app.route("/tareas")
def tareas():
    if "usuario" in session:
        return render_template("tareas_p.html")
    else:
        return redirect("/")

# Cerrar sesión (opcional)
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Sesión cerrada.")
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
