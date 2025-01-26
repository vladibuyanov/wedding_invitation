import os

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail
from flask_babel import Babel

from core.functions import get_locale, create_email

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

if __name__ == "__main__":
    app.run(debug=True)
