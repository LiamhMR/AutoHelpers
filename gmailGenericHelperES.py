from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.utils import parseaddr
from email.utils import parsedate_to_datetime
import mimetypes
from email import encoders
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError
from apiclient import errors
import os
import traceback
from datetime import datetime, timedelta
"""
Para manejar correos usando la API de GMAIL.
Código no optimizado ni refactorizado | Funciones genéricas adaptadas de la documentación de la API 
By DEVLii
"""

class Correo:
    def __init__(self, id_correo, id_hilo, remitente, asunto, fecha, cuerpo, archivos=[]):
        self.id_correo = id_correo
        self.id_hilo = id_hilo
        self.remitente = remitente
        self.asunto = asunto
        self.fecha = fecha
        self.dia = str(fecha).split(" ")[0].split("-")[2]
        self.mes = str(fecha).split(" ")[0].split("-")[1]
        self.año = str(fecha).split(" ")[0].split("-")[0]
        self.cuerpo = cuerpo
        self.archivos = archivos

class CorreoSimple:
    def __init__(self, id_correo, asunto, fecha):
        self.id_correo = id_correo
        self.asunto = asunto
        self.fecha = fecha
        
def enviar_correo_desde_archivo(ruta_reporte, destinatarios, asunto, cuerpo, token_correo):
    """
    @ruta_reporte    : Ruta donde se encuentra el texto a enviar.
    @destinatarios   : Correos a los que enviar.
    @asunto          : Asunto del correo.
    @cuerpo          : Cuerpo del mensaje inicial.
    @token_correo    : Token de correo configurado.
    """
    try:
        mensaje_reporte = ""
        try:
            with open(ruta_reporte, 'r') as fp:
                mensaje_reporte = fp.read()
        except:
            print("Ruta del reporte vacía")

        SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"
        ]
            
        credenciales = Credentials.from_authorized_user_file(token_correo, SCOPES)

        servicio = build('gmail', 'v1', credentials=credenciales)
        reporte = cuerpo + "\n" + str(mensaje_reporte)
        print(reporte)
        mensaje = MIMEText(reporte)
        mensaje['to'] = destinatarios
        crear_mensaje = {'raw': base64.urlsafe_b64encode(mensaje.as_bytes()).decode()}

        try:
            mensaje = (servicio.users().messages().send(userId="me", body=crear_mensaje).execute())
            print(F'Mensaje enviado a {mensaje} Id de Mensaje: {mensaje["id"]}')
        except HTTPError as error:
            print(F'Ocurrió un error: {error}')
            mensaje = None
    except Exception as e:
        print("ERROR AL ENVIAR CORREO O MAIL NO CONFIGURADO", e)

def configurar_correo(credenciales, ruta_token_json, solo_lectura=True, enviar=False, modificar=False):
    """Abre una pestaña para conectar el correo al bot.
    @credenciales : Credenciales de cliente al proyecto.
    @ruta_token_json : Ruta al archivo token a generar.
    """
    try:
        scopes = []
        if solo_lectura:
            scopes.append("https://www.googleapis.com/auth/gmail.readonly")
        if enviar:
            scopes.append("https://www.googleapis.com/auth/gmail.send")
        if modificar:
            scopes.append("https://www.googleapis.com/auth/gmail.modify")
        
        SCOPES = scopes
        credenciales = None
        
        # Si no hay credenciales (válidas) disponibles, permite que el usuario inicie sesión.
        if credenciales is None or not credenciales.valid:
            print("NO HAY CREDENCIALES")
            if credenciales and credenciales.expired and credenciales.refresh_token:
                credenciales.refresh(Request())
            else:
                flujo = InstalledAppFlow.from_client_secrets_file(
                    credenciales, SCOPES
                )
                credenciales = flujo.run_local_server(port=0)
                # Guardar las credenciales para la próxima ejecución.
                with open(ruta_token_json, "w") as token:
                    token.write(credenciales.to_json())

                servicio = build('gmail', 'v1', credentials=credenciales)
                print("CORREO CONFIGURADO.")
    except:
        print("ERROR AL CONFIGURAR CORREO")

def enviar_correo_prueba(ruta, destinatario, asunto, cuerpo):
    """Envía un correo de ejemplo"""
    enviar_correo_desde_archivo(ruta, destinatario, asunto, cuerpo)

def verificar_configuracion_correo(token_correo):
    try:
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.readonly"
        ]
        credenciales = Credentials.from_authorized_user_file(token_correo, SCOPES)
        if credenciales and credenciales.expired and credenciales.refresh_token:
            credenciales.refresh(Request())
        if credenciales and credenciales.expired and credenciales.refresh_token:
            print("Credenciales vencidas, volver a configurar correo.")
            return False
        return True
    except:
        return False

def contar_lineas_reporte(ruta_reporte):
    """Retorna la cantidad de líneas de un archivo de texto.
    @ruta_reporte : Ruta del archivo.
    """
    try:
        with open(ruta_reporte, 'r') as fp:
            texto = fp.read()
            cantidad_lineas = len(texto.split("\n"))
            return cantidad_lineas
    except:
        return -1
            
# UPDATES
def enviar_correo(destinatarios, asunto, cuerpo, token_correo, adjuntos=[]):
    """
    @destinatarios   : Correos a los que enviar separados por coma.
    @asunto          : Asunto.
    @cuerpo          : Cuerpo del correo.
    @token_correo    : Token de correo configurado.
    @adjuntos        : Lista de archivos a adjuntar *Opcional.
    """
    try:
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"
        ]
            
        credenciales = Credentials.from_authorized_user_file(token_correo, SCOPES)

        servicio = build('gmail', 'v1', credentials=credenciales)
        reporte = cuerpo
        print(reporte)
        mensaje = EmailMessage()
        mensaje.set_content(reporte)
        mensaje['to'] = destinatarios
        mensaje['subject'] = asunto
        if len(adjuntos) != 0:
            for adjunto in adjuntos:
                with open(adjunto, 'rb') as archivo_contenido:
                    contenido = archivo_contenido.read()
                    mensaje.add_attachment(contenido, maintype='application', subtype=(adjunto.split('.')[1]), filename=adjunto.split("/")[-1])
                    print("Adjunto correcto.")
        crear_mensaje = {'raw': base64.urlsafe_b64encode(mensaje.as_bytes()).decode()}

        try:
            mensaje = (servicio.users().messages().send(userId="me", body=crear_mensaje).execute())
            print(F'Mensaje enviado a {mensaje} Id de Mensaje: {mensaje["id"]}')
        except HTTPError as error:
            print(F'Ocurrió un error: {error}')
            mensaje = None
    except Exception as e:
        print("ERROR AL ENVIAR CORREO O MAIL NO CONFIGURADO", e)

def listar_correos_no_leidos(token_correo, asunto=""):
    try:
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.readonly"
        ]
            
        credenciales = Credentials.from_authorized_user_file(token_correo, SCOPES)

        servicio = build('gmail', 'v1', credentials=credenciales)
        mensajes_arr = []
        try:
            consulta = 'is:unread'
            if asunto != "":
                consulta = f'is:unread subject:"{asunto}"'
            resultados = servicio.users().messages().list(userId='me', q=consulta).execute()
            mensajes = resultados.get('messages', [])
            if not mensajes:
                print('No se encontraron correos no leídos.')
            else:
                for mensaje in mensajes:
                    mensajes_arr.append(str(mensaje['id']))
                return mensajes_arr
        except HTTPError as error:
            print(F'Ocurrió un error: {error}')
            mensaje = None
    except Exception as e:
        print("ERROR AL LEER CORREOS O MAIL NO CONFIGURADO", e)

def obtener_cuerpo_correo(mensaje):
    if 'parts' in mensaje['payload']:
        for parte in mensaje['payload']['parts']:
            if parte['mimeType'] == 'text/plain':
                data = parte['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
    elif 'data' in mensaje['payload']['body']:
        data = mensaje['payload']['body']['data']
        return base64.urlsafe_b64decode(data).decode('utf-8')
    else:
        return None
    
def obtener_adjuntos(servicio, id_mensaje, directorio_guardado):
    """Obtener y almacenar adjuntos del Mensaje con el ID dado.
    Args:
    servicio: Instancia de servicio API de Gmail autorizada.
    id_mensaje: ID del Mensaje que contiene el adjunto.
    """
    try:
        usuario_id = "me"
        mensaje = servicio.users().messages().get(userId=usuario_id, id=id_mensaje).execute()
        lista_nombres_adjuntos = []
        for parte in mensaje['payload']['parts']:
            if 'filename' in parte and parte['filename']:
                nombre_adjunto = parte['filename']
                lista_nombres_adjuntos.append(nombre_adjunto)
                ruta_adjunto = os.path.join(directorio_guardado, nombre_adjunto)

                if 'body' in parte and 'attachmentId' in parte['body']:
                    adjunto_id = parte['body']['attachmentId']
                    respuesta_adjunto = servicio.users().messages().attachments().get(
                        userId=usuario_id,
                        messageId=id_mensaje,
                        id=adjunto_id).execute()
                    datos = respuesta_adjunto['data']
                    datos_decodificados = base64.urlsafe_b64decode(datos)

                    with open(ruta_adjunto, 'wb') as f:
                        f.write(datos_decodificados)
                        print(f"Adjunto {nombre_adjunto} guardado en {ruta_adjunto}")

        return lista_nombres_adjuntos

    except Exception as e:
        print(f'Ocurrió un error al obtener adjuntos: {e}')

def listar_correos(token_correo):
    """Lista correos no leídos, retorna una lista de correos de clase Correo.
    Args:
        token_correo
    """
    try:
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.readonly"
        ]

        credenciales = Credentials.from_authorized_user_file(token_correo, SCOPES)

        servicio = build('gmail', 'v1', credentials=credenciales)

        # Obtén mensajes no leídos
        mensajes_no_leidos = listar_correos_no_leidos(token_correo)
        
        lista_correos = []
        for id_mensaje in mensajes_no_leidos:
            try:
                mensaje = servicio.users().messages().get(userId='me', id=id_mensaje).execute()
                cuerpo = obtener_cuerpo_correo(mensaje)
                id_hilo = mensaje['threadId']
                remitente = mensaje['payload']['headers'][0]['value']
                asunto = mensaje['payload']['headers'][1]['value']
                fecha = mensaje['payload']['headers'][2]['value']
                lista_correos.append(Correo(id_mensaje, id_hilo, remitente, asunto, fecha, cuerpo))
            except Exception as e:
                print(f'No se pudo obtener el mensaje con ID: {id_mensaje}. Error: {e}')

        return lista_correos

    except Exception as e:
        print(f'Ocurrió un error al obtener correos: {e}')

    
    