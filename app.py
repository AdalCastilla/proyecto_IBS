from ticket_system import create_app

app = create_app()

# Configuración del servidor SMTP
app.config['SMTP_SERVER'] = 'smtp.gmail.com'  # Servidor SMTP de Gmail
app.config['SMTP_PORT'] = 587  # Puerto para TLS
app.config['EMAIL_ADDRESS'] = 'tucorreo@gmail.com'  # Tu correo electrónico
app.config['EMAIL_PASSWORD'] = 'tucontraseña'  # Tu contraseña o contraseña de aplicación

if __name__ == '__main__':
    app.run(debug=True)