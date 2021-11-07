import sqlite3
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from email.mime.multipart import MIMEMultipart
from email import encoders

class SendEmail(object):
    def __init__(self, dni, destiny):
        self.connection = ""
        self.email = "proyectoasistencias8@gmail.com"
        self.password = "pskAdm32"
        self.asunto = "Asistencia por código Qr"
        
        self.destiny = destiny
        self.message = "Se envía por este medio el correspondiente código Qr necesario para validar y generar altas de asistencias en el "
        self.dni = dni

    def sendEmail(self):
        try:
            mensaje = MIMEMultipart("alternative")
            mensaje["Subject"] = self.asunto
            mensaje["From"] = self.email
            mensaje["To"] = self.destiny

            html = f"""
            <html>
            <body>
                {self.message} <b>Instituto Privado de Estudios Superiores IPET 1308.</b>
            </body>
            </html>
            """

            generar_html = MIMEText(html, "html")
            mensaje.attach(generar_html)

            qr = f"qr/{self.dni}.PNG"

            with open(qr, "rb") as adjunto:
                contenido_adjunto = MIMEBase("application", "octet-stream")
                contenido_adjunto.set_payload(adjunto.read())

            encoders.encode_base64(contenido_adjunto)

            contenido_adjunto.add_header("Content-Disposition", f"attachment; filename={qr}")

            mensaje.attach(contenido_adjunto)
            mensaje_final = mensaje.as_string()

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, self.destiny, mensaje_final)

            return "Ok"
        except Exception as e:
            print(e)
            return "Error"