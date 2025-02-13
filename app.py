import os

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail
from flask_babel import Babel

from core import functions


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
babel = Babel(app=app, locale_selector=functions.get_locale)

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        msg = functions.create_email(request, email)
        mail.send(msg)
        return jsonify({"message": "Данные успешно отправлены и письмо отправлено!"}), 200

    except Exception as e:
        print("Ошибка:", e)
        return jsonify({"message": "Ошибка при отправке письма."}), 500

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    drive_service = functions.get_drive_service()
    message = None

    if request.method == 'POST':
        files = request.files.getlist('photos')
        pwd = request.form.get("password")

        if pwd != password:
            return "Пароль неправильный", 403

        result = functions.upload_files_to_drive(drive_service=drive_service, files=files)

        if not result:
            return "Ошибка: Только фото разрешены!", 400

        message = "Файлы успешно загружены!"

    return render_template('upload.html', message=message)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
