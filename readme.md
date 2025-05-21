# nota informativa
El proyecto se mantendra inutilizado hasta que encuentre la oportunidad de agregar un servidor de base de datos sin tiempo limite como el que el plan gratuito de render ofrece, mil disculpas
y gracias por su apoyo!! de todas formas no duden en utilizar y analizar el codigo, es funcional.

# Plataforma de administración de tareas

Este proyecto es una plataforma web de gestión de usuarios y tareas (Task-web) desarrollada como proyecto final para la asignatura Introducción a los Sistemas de Computación en el Instituto Tecnológico de las Américas (ITLA). Está construido con **Python**, **Flask** y **SQLite**.

## 🔧 Tecnologías utilizadas

- **Python 3**
- **Flask**
- **Flask-SQLAlchemy**
- **Werkzeug**
- **HTML / CSS (para los templates)**
- **PostgreSQL (en producción)**
- **SQLite (en desarrollo)**
- **Render (para despliegue)**

---

## ⚙️ Funcionalidades

- Registro de usuarios con contraseña segura.
- Inicio y cierre de sesión.
- Creación, edición y eliminación de tareas personales.
- Gestión de fechas de vencimiento y prioridades.
- Interfaz separada para usuarios autenticados.

## 📁 Estructura del Proyecto
/static/
├── style.css # Estilos personalizados ├── img/ # Imágenes del sitio (si las hubiera) /templates/
├── index.html # Página de inicio con formulario de registro/login ├── tareas_p.html # Panel de tareas del usuario logueado

app.py # Código principal de la aplicación Flask requirements.txt # Lista de dependencias para instalar README.md # Documentación del proyecto .env (opcional) # Variables de entorno (para desarrollo)

## 🚀 Cómo ejecutar el proyecto

1. Uso del link de render
   
    https://task-web-g5zv.onrender.com
 

2. Crea un entorno virtual (opcional pero recomendado)

   python -m venv venv
   source venv/bin/activate   # En Linux o Mac
   venv\Scripts\activate      # En Windows

3. Instala las dependencias

   pip install -r requirements.txt

4. Ejecuta la app

   python app.py

La aplicación estará disponible en http://127.0.0.1:5000.

      

## ☁️ Despliegue en Render con PostgreSQL  

Crear cuenta en Render.

Conectar tu repositorio desde GitHub.

Crear un nuevo servicio web ("Web Service").

Configurar variables de entorno:

DATABASE_URL = (url de PostgreSQL que te da Render)
SECRET_KEY = tu_clave_secreta

Seleccionar el entorno Python y usar como comando de inicio:

gunicorn app:app

Render instalará automáticamente las dependencias desde requirements.txt.


## 📝 Notas

En desarrollo local se usa SQLite, pero en producción usamos PostgreSQL.

Usa siempre contraseñas largas y seguras.

Puedes personalizar los estilos desde /static/style.css.

La base de datos tareas.db se crea automáticamente al iniciar la app.

Las contraseñas se almacenan de forma segura con hash.

Se recomienda no usar la clave secreta "supersecreto" en producción.

## Autores  

Equipo 2- Conformado por:

👨‍💻 Edwin Jeremías Agustín Yack 
👨‍💻 Jose Antonio Mateo Matos
👩‍💻 Jhordalia María Peña Santana

Proyecto final de Introducción a los sistemas de computación – ITLA.


Soporte y Feedbacks a:
edwinjeremiasagustinyack@gmail.com
