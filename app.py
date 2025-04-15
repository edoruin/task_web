from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo actualizado
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    contrasena = db.Column(db.String(255)) 

# Crear las tablas si no existen
with app.app_context(): 
    db.create_all()

# Ruta principal
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para guardar datos del formulario HTML
@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    contrasena_plana = request.form["contrasena"]
    contrasena_hash = generate_password_hash(contrasena_plana)

    nuevo_usuario = Usuario(nombre=nombre, contrasena=contrasena_hash)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
