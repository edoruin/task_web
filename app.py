from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Usa la variable de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# Modelo de ejemplo
class Usuario(db.Model):a
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(120), unique=True)

#crea las tablas de la base de datos
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
    correo = request.form["correo"]
    nuevo_usuario = Usuario(nombre=nombre, correo=correo)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
