import os

from flask import request
from flask_mail import Message

from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2 import service_account

from core import constants


def get_locale():
    if request.args.get('lang'):
        return request.args.get('lang')
    return request.accept_languages.best_match(['ru', 'sk'])


def create_email(web_request, email):
    data = web_request.get_json()
    name = data.get('name')
    guests = data.get('guests')
    alcohol = data.get('alcohol', [])

    alcohol_preferences = ', '.join(alcohol) if alcohol else 'Нет предпочтений'
    email_body = f"""
        Новый отклик:
        Имя: {name}
        Количество гостей: {guests}
        Предпочтения алкоголя: {alcohol_preferences}
        """

    return Message(
        subject="Новый отклик с формы",
        recipients=[email],
        body=email_body
    )

def get_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        constants.SERVICE_ACCOUNT_FILE,
        scopes=constants.SCOPES
    )
    return build('drive', 'v3', credentials=credentials)

def upload_files_to_drive(drive_service, files) -> bool:
    for file in files:
        if file.content_type not in constants.ALLOWED_MIME_TYPES:
            return False

        file.save(file.filename)
        media = MediaFileUpload(file.filename)
        drive_service.files().create(
            body={'name': file.filename, 'parents': [constants.folder_id]},
            media_body=media,
            fields='id'
        ).execute()
        os.remove(file.filename)

        return True