# Plataforma Educativa con Moodle

Este proyecto es una plataforma web de gestión de usuarios y tareas, inspirada en las funcionalidades básicas de plataformas como Moodle. Está construido con **Python**, **Flask** y **SQLite**.

## 🔧 Tecnologías utilizadas

- **Python 3**
- **Flask**
- **Flask-SQLAlchemy**
- **Werkzeug**
- **HTML / CSS (para los templates)**

## ⚙️ Funcionalidades

- Registro de usuarios con contraseña segura.
- Inicio y cierre de sesión.
- Creación, edición y eliminación de tareas personales.
- Gestión de fechas de vencimiento y prioridades.
- Interfaz separada para usuarios autenticados.

## 📁 Estructura del Proyecto
/static/ # Archivos estáticos (CSS, imágenes, JS) ├── style.css # Estilos personalizados

/templates/ # Archivos HTML ├── index.html # Página principal con registro/login ├── tareas_p.html # Panel de tareas del usuario

app.py # Lógica principal del servidor Flask tareas.db # Base de datos SQLite (se crea automáticamente) README.md # Documentación del proyecto


## 🚀 Cómo ejecutar el proyecto

### 1. Clona el repositorio

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

2. Crea un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate   # En Linux o Mac
venv\Scripts\activate      # En Windows

3. Instala las dependencias

pip install flask flask_sqlalchemy werkzeug

4. Ejecuta la app

python app.py

La aplicación estará disponible en http://127.0.0.1:5000.

📝 Notas
La base de datos tareas.db se crea automáticamente al iniciar la app.

Las contraseñas se almacenan de forma segura con hash.

Se recomienda no usar la clave secreta "supersecreto" en producción.

👩‍💻👨‍💻👨‍💻 Autores

Equipo 4- Conformado por: Edwin, José, Jhordalia

Proyecto final de Introducción a los sistemas de computación – ITLA.
