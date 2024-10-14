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
To handle emails using the GMAIL API.
Unoptimized and unrefactored code | Generic functions adapted from the API documentation 
By DEVLii
"""

class Email:
    def __init__(self, email_id, thread_id, sender, subject, date, body, attachments=[]):
        self.email_id = email_id
        self.thread_id = thread_id
        self.sender = sender
        self.subject = subject
        self.date = date
        self.day = str(date).split(" ")[0].split("-")[2]
        self.month = str(date).split(" ")[0].split("-")[1]
        self.year = str(date).split(" ")[0].split("-")[0]
        self.body = body
        self.attachments = attachments

class SimpleEmail:
    def __init__(self, email_id, subject, date):
        self.email_id = email_id
        self.subject = subject
        self.date = date
        
def send_email_from_file(report_path, recipients, subject, body, email_token):
    """
    @report_path     : Path where the text to send is located.
    @recipients      : Emails to send to.
    @subject         : Email subject.
    @body            : Initial message body.
    @email_token     : Configured email token.
    """
    try:
        report_message = ""
        try:
            with open(report_path, 'r') as fp:
                report_message = fp.read()
        except:
            print("Report path is empty.")

        SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"
        ]
            
        credentials = Credentials.from_authorized_user_file(email_token, SCOPES)

        service = build('gmail', 'v1', credentials=credentials)
        report = body + "\n" + str(report_message)
        print(report)
        message = MIMEText(report)
        message['to'] = recipients
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

        try:
            message = (service.users().messages().send(userId="me", body=create_message).execute())
            print(f'Message sent to {message} Message ID: {message["id"]}')
        except HTTPError as error:
            print(f'An error occurred: {error}')
            message = None
    except Exception as e:
        print("ERROR SENDING EMAIL OR MAIL NOT CONFIGURED", e)

def configure_email(credentials, token_json_path, read_only=True, send=False, modify=False):
    """Opens a tab to connect the email to the bot.
    @credentials     : Client credentials for the project.
    @token_json_path : Path to the token file to be generated.
    """
    try:
        scopes = []
        if read_only:
            scopes.append("https://www.googleapis.com/auth/gmail.readonly")
        if send:
            scopes.append("https://www.googleapis.com/auth/gmail.send")
        if modify:
            scopes.append("https://www.googleapis.com/auth/gmail.modify")
        
        SCOPES = scopes
        credentials = None
        
        # If there are no (valid) credentials available, allow the user to log in.
        if credentials is None or not credentials.valid:
            print("NO CREDENTIALS")
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials, SCOPES
                )
                credentials = flow.run_local_server(port=0)
                # Save the credentials for the next run.
                with open(token_json_path, "w") as token:
                    token.write(credentials.to_json())

                service = build('gmail', 'v1', credentials=credentials)
                print("EMAIL CONFIGURED.")
    except:
        print("ERROR CONFIGURING EMAIL")

def send_test_email(path, recipient, subject, body):
    """Sends a test email"""
    send_email_from_file(path, recipient, subject, body)

def check_email_configuration(email_token):
    try:
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/gmail.readonly"
        ]
        credentials = Credentials.from_authorized_user_file(email_token, SCOPES)
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        if credentials and credentials.expired and credentials.refresh_token:
            print("Credentials expired, reconfigure email.")
            return False
        return True
    except:
        return False

def count_lines_in_report(report_path):
    """Returns the number of lines in a text file.
    @report_path : Path to the file.
    """
    try:
        with open(report_path, 'r') as fp:
            text = fp.read()
            line_count = len(text.split("\n"))
            return line_count
    except:
        return -1
            
# UPDATES
def send_email(recipients, subject, body, email_token, attachments=[]):
    """
    @recipients      : Emails to send to separated by commas.
    @subject         : Subject.
    @body            : Body of the email.
    @email_token     : Configured email token.
    @attachments     : List of files to attach *Optional.
    """
    try:
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"
        ]
            
        credentials = Credentials.from_authorized_user_file(email_token, SCOPES)

        service = build('gmail', 'v1', credentials=credentials)
        report = body
        print(report)
        message = EmailMessage()
        message.set_content(report)
        message['to'] = recipients
        message['subject'] = subject
        if len(attachments) != 0:
            for attachment in attachments:
                with open(attachment, 'rb') as content_file:
                    content = content_file.read()
                    message.add_attachment(content, maintype='application', subtype=(attachment.split('.')[1]), filename=attachment.split("/")[-1])
                    print("Attachment successful.")
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

        try:
            message = (service.users().messages().send(userId="me", body=create_message).execute())
            print(f'Message sent to {message} Message ID: {message["id"]}')
        except HTTPError as error:
            print(f'An error occurred: {error}')
            message = None
    except Exception as e:
        print("ERROR SENDING EMAIL OR MAIL NOT CONFIGURED", e)

def list_unread_emails(email_token, subject=""):
    try:
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.readonly"
        ]
            
        credentials = Credentials.from_authorized_user_file(email_token, SCOPES)

        service = build('gmail', 'v1', credentials=credentials)
        messages_array = []
        try:
            query = 'is:unread'
            if subject != "":
                query = f'is:unread subject:"{subject}"'
            results = service.users().messages().list(userId='me', q=query).execute()
            messages = results.get('messages', [])
            if not messages:
                print('No unread emails found.')
            else:
                for message in messages:
                    messages_array.append(str(message['id']))
                return messages_array
        except HTTPError as error:
            print(f'An error occurred: {error}')
            message = None
    except Exception as e:
        print("ERROR READING EMAILS OR MAIL NOT CONFIGURED", e)

def get_email_body(message):
    if 'parts' in message['payload']:
        for part in message['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
    elif 'data' in message['payload']['body']:
        data = message['payload']['body']['data']
        return base64.urlsafe_b64decode(data).decode('utf-8')
    else:
        return None
    
def get_attachments(service, message_id, save_directory):
    """Retrieve and store attachments from the message with the given ID.
    Args:
    service: Authorized Gmail API service instance.
    message_id: ID of the message containing the attachment.
    """
    try:
        user_id = "me"
        message = service.users().messages().get(userId=user_id, id=message_id).execute()
        attachment_names_list = []
        for part in message['payload']['parts']:
            if 'filename' in part and part['filename']:
                attachment_name = part['filename']
                attachment_names_list.append(attachment_name)
                attachment_path = os.path.join(save_directory, attachment_name)

                if 'body' in part and 'attachmentId' in part['body']:
                    attachment_id = part['body']['attachmentId']
                    attachment_response = service.users().messages().attachments().get(
                        userId=user_id,
                        messageId=message_id,
                        id=attachment_id).execute()
                    data = attachment_response['data']
                    decoded_data = base64.urlsafe_b64decode(data)

                    with open(attachment_path, 'wb') as f:
                        f.write(decoded_data)
                        print(f"Attachment {attachment_name} saved to {attachment_path}")

        return attachment_names_list

    except Exception as e:
        print(f'An error occurred while getting attachments: {e}')

def list_emails(email_token):
    """Lists unread emails, returns a list of emails of class Email.
    Args:
        email_token
    """
    try:
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.readonly"
        ]

        credentials = Credentials.from_authorized_user_file(email_token, SCOPES)

        service = build('gmail', 'v1', credentials=credentials)
        messages_array = []
        try:
            results = service.users().messages().list(userId='me').execute()
            messages = results.get('messages', [])

            if not messages:
                print('No messages found.')
                return []

            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                email_id = msg['id']
                thread_id = msg['threadId']
                sender = msg['payload']['headers'][0]['value']
                subject = msg['payload']['headers'][1]['value']
                date = msg['payload']['headers'][2]['value']
                body = get_email_body(msg)
                messages_array.append(Email(email_id, thread_id, sender, subject, date, body))

            return messages_array
        except HTTPError as error:
            print(f'An error occurred: {error}')
            return []
    except Exception as e:
        print("ERROR LISTING EMAILS OR MAIL NOT CONFIGURED", e)


    
    