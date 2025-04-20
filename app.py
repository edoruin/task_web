from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secreto"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    completada = db.Column(db.Boolean, default=False)
    fecha_vencimiento = db.Column(db.Date)
    prioridad = db.Column(db.String(20))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tareas = db.relationship('Tarea', backref='usuario', lazy=True)


@app.route("/")
def index():
    return render_template("login.html")

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

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    usuario = Usuario.query.filter_by(username=username).first()
    if usuario and check_password_hash(usuario.password, password):
        session["usuario_id"] = usuario.id
        return redirect("/tareas_p")
    else:
        flash("Usuario o contraseña incorrectos.")
        return redirect("/")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if Usuario.query.filter_by(username=username).first():
            flash("El nombre de usuario ya existe.")
            return redirect("/registro")

        hashed_password = generate_password_hash(password)
        nuevo_usuario = Usuario(username=username, password=hashed_password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Registro exitoso. Por favor inicia sesión.")
        return redirect("/")
    return render_template("registro.html")

@app.route("/logout")
def logout():
    session.pop("usuario_id", None)
    return redirect("/")

@app.route("/tareas_p")
def tareas_p():
    if "usuario_id" not in session:
        return redirect("/")

    usuario_id = session["usuario_id"]
    tareas = Tarea.query.filter_by(usuario_id=usuario_id).all()
    return render_template("tareas.html", tareas=tareas)

@app.route("/crear_tarea", methods=["POST"])
def crear_tarea():
    if "usuario_id" not in session:
        return redirect("/")

    descripcion = request.form["descripcion"]
    fecha_vencimiento = request.form.get("fecha_vencimiento")
    prioridad = request.form.get("prioridad")

    tarea = Tarea(
        descripcion=descripcion,
        completada=False,
        fecha_vencimiento=datetime.strptime(fecha_vencimiento, '%Y-%m-%d') if fecha_vencimiento else None,
        prioridad=prioridad,
        usuario_id=session["usuario_id"]
    )
    db.session.add(tarea)
    db.session.commit()

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
    tarea.fecha_vencimiento = datetime.strptime(request.form["fecha_vencimiento"], '%Y-%m-%d') if request.form["fecha_vencimiento"] else None
    tarea.prioridad = request.form.get("prioridad")
    tarea.completada = "completada" in request.form

    db.session.commit()
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
    return redirect("/tareas_p")

@app.route("/toggle_tarea/<int:id>", methods=["POST"])
def toggle_tarea(id):
    if "usuario_id" not in session:
        return redirect("/")

    tarea = Tarea.query.get_or_404(id)
    if tarea.usuario_id != session["usuario_id"]:
        flash("No tienes permiso para modificar esta tarea.")
        return redirect("/tareas_p")

    tarea.completada = not tarea.completada
    db.session.commit()
    return redirect("/tareas_p")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
