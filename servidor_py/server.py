import logging
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia esto a una clave segura
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Configurar logger específico para la aplicación
app_logger = logging.getLogger("app_logger")
app_logger.setLevel(logging.INFO)

# Formato para los logs
formatter = logging.Formatter('%(asctime)s - %(message)s')

# Handler para guardar en archivo
file_handler = logging.FileHandler('logs.txt', encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
app_logger.addHandler(file_handler)

# Handler para la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
app_logger.addHandler(console_handler)

# Redirigir los logs de Werkzeug al logger de la aplicación con el mismo formato
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)

# Sobrescribir el formateo de Werkzeug
for handler in werkzeug_logger.handlers[:]:
    werkzeug_logger.removeHandler(handler)

werkzeug_file_handler = logging.FileHandler('logs.txt', encoding='utf-8')
werkzeug_file_handler.setLevel(logging.INFO)
werkzeug_file_handler.setFormatter(formatter)

werkzeug_console_handler = logging.StreamHandler()
werkzeug_console_handler.setLevel(logging.INFO)
werkzeug_console_handler.setFormatter(formatter)

werkzeug_logger.addHandler(werkzeug_file_handler)
werkzeug_logger.addHandler(werkzeug_console_handler)

# Middleware para obtener IPs correctas si hay proxy
app.wsgi_app = ProxyFix(app.wsgi_app)

# Define la tabla de usuarios
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Ruta para la página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('El usuario ya existe')
            app_logger.info(f'{request.remote_addr} - INFO - Intento de registro fallido para el usuario {username}')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Usuario registrado con éxito')
        app_logger.info(f'{request.remote_addr} - INFO - Nuevo usuario registrado: {username}')
        return redirect(url_for('login'))
    return render_template('register.html')

# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            flash('Inicio de sesión exitoso')
            app_logger.info(f'{request.remote_addr} - INFO - Usuario {username} inició sesión exitosamente')
            return redirect(url_for('welcome'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
            app_logger.warning(f'{request.remote_addr} - WARNING - Intento de inicio de sesión fallido para el usuario {username}')
            return redirect(url_for('login'))

    return render_template('login.html')

# Ruta de bienvenida tras inicio de sesión exitoso
@app.route('/welcome')
def welcome():
    return "Bienvenido a la aplicación"

if __name__ == '__main__':
    # Crear las tablas en la base de datos
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
