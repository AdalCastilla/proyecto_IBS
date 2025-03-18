from . import db
from flask_login import UserMixin  # Para manejar la autenticación de usuarios
from werkzeug.security import generate_password_hash, check_password_hash  # Para hashear contraseñas
from datetime import datetime  # Para manejar fechas

class Usuario(db.Model, UserMixin):
    """
    Modelo de la tabla 'usuarios'.
    Representa a los usuarios del sistema (clientes, técnicos y administradores).
    """
    id = db.Column(db.Integer, primary_key=True)  # ID único del usuario
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)  # Nombre de usuario (único)
    correo = db.Column(db.String(100), unique=True, nullable=False)  # Correo electrónico (único)
    contraseña = db.Column(db.String(100), nullable=False)  # Contraseña (hash)
    tipo_usuario = db.Column(db.String(20), nullable=False)  # Tipo de usuario (cliente, tecnico, admin)
    tickets_creados = db.relationship('Ticket', backref='cliente', lazy=True)  # Relación con los tickets creados

    def __repr__(self):
        return f"Usuario('{self.nombre_usuario}', '{self.correo}', '{self.tipo_usuario}')"

    def set_password(self, contraseña):
        """
        Hashea la contraseña y la guarda en el campo 'contraseña'.
        """
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        """
        return check_password_hash(self.contraseña, contraseña)


class Ticket(db.Model):
    """
    Modelo de la tabla 'tickets'.
    Representa los tickets creados por los clientes.
    """
    id = db.Column(db.Integer, primary_key=True)  # ID único del ticket
    descripcion = db.Column(db.Text, nullable=False)  # Descripción del problema
    estado = db.Column(db.String(20), nullable=False, default='pendiente')  # Estado del ticket (pendiente, resuelto)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Fecha de creación del ticket
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # ID del cliente que creó el ticket
    tecnico_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))  # ID del técnico asignado (opcional)

    def __repr__(self):
        return f"Ticket('{self.id}', '{self.descripcion}', '{self.estado}')"