import os

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail
from flask_babel import Babel

from googleapiclient.discovery import build

from google.oauth2 import service_account

from core.functions import get_locale, create_email, upload_files_to_drive


app = Flask(__name__)

email = os.getenv('EMAIL', False)
password = os.getenv('PASSWORD', False)

# Email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] =  password
app.config['MAIL_DEFAULT_SENDER'] = email
# Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'
app.config['BABEL_SUPPORTED_LOCALES'] = ['ru', 'sk']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

mail = Mail(app)
babel = Babel(app=app, locale_selector=get_locale)

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = './secrets/credentials.json'

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)


# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        msg = create_email(request, email)
        mail.send(msg)
        return jsonify({"message": "Данные успешно отправлены и письмо отправлено!"}), 200

    except Exception as e:
        print("Ошибка:", e)
        return jsonify({"message": "Ошибка при отправке письма."}), 500

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    message = None

    if request.method == 'POST':
        files = request.files.getlist('photos')
        result = upload_files_to_drive(drive_service=drive_service, files=files)
        if result:
            message = "Файлы успешно загружены!"
        else:
            return "Ошибка: Только фото разрешены!", 400

    return render_template('upload.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
