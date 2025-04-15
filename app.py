from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # El archivo debe estar en la carpeta "templates"

if __name__ == '__main__':
    app.run(debug=True)
