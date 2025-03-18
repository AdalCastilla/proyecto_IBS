import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

def enviar_correo(destinatario, asunto, mensaje):
    """
    Envía un correo electrónico utilizando SMTP.

    Parámetros:
        destinatario (str): Correo electrónico del destinatario.
        asunto (str): Asunto del correo.
        mensaje (str): Cuerpo del correo.

    Retorna:
        bool: True si el correo se envió correctamente, False en caso contrario.
    """
    try:
        # Configuración del servidor SMTP
        smtp_server = current_app.config.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = current_app.config.get('SMTP_PORT', 587)
        email_address = current_app.config.get('EMAIL_ADDRESS', 'tucorreo@gmail.com')
        email_password = current_app.config.get('EMAIL_PASSWORD', 'tucontraseña')

        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = destinatario
        msg['Subject'] = asunto

        # Agregar el cuerpo del mensaje
        msg.attach(MIMEText(mensaje, 'plain'))

        # Conectar al servidor SMTP y enviar el correo
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Habilitar cifrado TLS
            server.login(email_address, email_password)  # Iniciar sesión en el servidor
            server.sendmail(email_address, destinatario, msg.as_string())  # Enviar el correo

        print(f"Correo enviado a {destinatario}: {asunto}")
        return True
    except Exception as e:
        print(f"Error enviando correo a {destinatario}: {e}")
        return False