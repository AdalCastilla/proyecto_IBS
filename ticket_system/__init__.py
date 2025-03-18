from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager# Para manejo de autenticación de usuarios

# Inicializar la base de datos
db = SQLAlchemy()

# Inicializar el administrador de autenticación
login_manager = LoginManager()

def create_app():
    """
    Función para crear y configurar la aplicación Flask.
    """
    # Crear la aplicación Flask
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'  # Base de datos SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evitar warnings
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Clave secreta para sesiones

    # Inicializar extensiones con la aplicación
    db.init_app(app)
    login_manager.init_app(app)

    # Configurar la función de carga de usuarios para Flask-Login
    from .models import Usuario

    @login_manager.user_loader
    def load_user(usuario_id):
        return Usuario.query.get(int(usuario_id))

    # Registrar blueprints (rutas)
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Crear tablas en la base de datos (si no existen)
    with app.app_context():
        db.create_all()

    return app