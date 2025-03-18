from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Usuario, Ticket
from . import db
from .utils import enviar_correo

# Crear un Blueprint para las rutas
main_bp = Blueprint('main', __name__)

# Ruta de inicio de sesión
@main_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['username']
        contraseña = request.form['password']
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

        if usuario and usuario.check_password(contraseña):
            login_user(usuario)
            session['tipo_usuario'] = usuario.tipo_usuario

            if usuario.tipo_usuario == 'cliente':
                return redirect(url_for('main.cliente'))
            elif usuario.tipo_usuario == 'tecnico':
                return redirect(url_for('main.tecnico'))
            elif usuario.tipo_usuario == 'admin':
                return redirect(url_for('main.admin'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

# Ruta de cierre de sesión
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('main.login'))

# Ruta del panel del cliente
@main_bp.route('/cliente', methods=['GET', 'POST'])
@login_required
def cliente():
    if current_user.tipo_usuario != 'cliente':
        flash('No tienes permiso para acceder a esta página', 'error')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        descripcion = request.form['ticket-description']
        nuevo_ticket = Ticket(descripcion=descripcion, cliente_id=current_user.id)
        db.session.add(nuevo_ticket)
        db.session.commit()

        # Enviar correo al cliente
        enviar_correo(current_user.correo, 'Ticket Creado', f'Tu ticket ha sido creado: {descripcion}')

        flash('Ticket creado exitosamente', 'success')
        return redirect(url_for('main.cliente'))

    tickets = Ticket.query.filter_by(cliente_id=current_user.id).all()
    return render_template('cliente.html', tickets=tickets)

# Ruta del panel del técnico
@main_bp.route('/tecnico')
@login_required
def tecnico():
    if current_user.tipo_usuario != 'tecnico':
        flash('No tienes permiso para acceder a esta página', 'error')
        return redirect(url_for('main.login'))

    tickets = Ticket.query.filter_by(estado='pendiente').all()
    return render_template('tecnico.html', tickets=tickets)

# Ruta para responder un ticket (técnico)
@main_bp.route('/responder_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def responder_ticket(ticket_id):
    if current_user.tipo_usuario != 'tecnico':
        flash('No tienes permiso para realizar esta acción', 'error')
        return redirect(url_for('main.login'))

    respuesta = request.form['respuesta']
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        ticket.estado = 'resuelto'
        ticket.tecnico_id = current_user.id
        db.session.commit()

        # Enviar correo al cliente y administrador
        cliente = Usuario.query.get(ticket.cliente_id)
        enviar_correo(cliente.correo, 'Ticket Resuelto', f'Tu ticket ha sido resuelto: {respuesta}')
        admin = Usuario.query.filter_by(tipo_usuario='admin').first()
        if admin:
            enviar_correo(admin.correo, 'Ticket Resuelto', f'El ticket #{ticket.id} ha sido resuelto: {respuesta}')

        flash('Ticket marcado como resuelto y notificación enviada', 'success')
    return redirect(url_for('main.tecnico'))

# Ruta del panel del administrador
@main_bp.route('/admin')
@login_required
def admin():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permiso para acceder a esta página', 'error')
        return redirect(url_for('main.login'))

    usuarios = Usuario.query.all()
    return render_template('admin.html', usuarios=usuarios)

# Ruta para crear un usuario (administrador)
@main_bp.route('/crear_usuario', methods=['POST'])
@login_required
def crear_usuario():
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permiso para realizar esta acción', 'error')
        return redirect(url_for('main.login'))

    nombre_usuario = request.form['nombre_usuario']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    tipo_usuario = request.form['tipo_usuario']

    if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
        flash('El nombre de usuario ya existe', 'error')
        return redirect(url_for('main.admin'))

    nuevo_usuario = Usuario(
        nombre_usuario=nombre_usuario,
        correo=correo,
        tipo_usuario=tipo_usuario
    )
    nuevo_usuario.set_password(contraseña)
    db.session.add(nuevo_usuario)
    db.session.commit()

    flash('Usuario creado exitosamente', 'success')
    return redirect(url_for('main.admin'))

# Ruta para eliminar un usuario (administrador)
@main_bp.route('/eliminar_usuario/<int:usuario_id>', methods=['POST'])
@login_required
def eliminar_usuario(usuario_id):
    if current_user.tipo_usuario != 'admin':
        flash('No tienes permiso para realizar esta acción', 'error')
        return redirect(url_for('main.login'))

    usuario = Usuario.query.get(usuario_id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado exitosamente', 'success')
    return redirect(url_for('main.admin'))