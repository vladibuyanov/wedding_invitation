import os

from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)

email = os.getenv('EMAIL', False)
password = os.getenv('PASSWORD', False)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] =  password
app.config['MAIL_DEFAULT_SENDER'] = email

mail = Mail(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        # Получение данных из запроса
        data = request.get_json()
        name = data.get('name')
        guests = data.get('guests')
        alcohol = data.get('alcohol', [])

        # Формирование текста письма
        alcohol_preferences = ', '.join(alcohol) if alcohol else 'Нет предпочтений'
        email_body = f"""
            Новый отклик:
            Имя: {name}
            Количество гостей: {guests}
            Предпочтения алкоголя: {alcohol_preferences}
            """

        # Отправка email
        msg = Message(
            subject="Новый отклик с формы",
            recipients=[email],
            body=email_body
        )
        mail.send(msg)

        return jsonify({"message": "Данные успешно отправлены и письмо отправлено!"}), 200
    except Exception as e:
        print("Ошибка:", e)
        return jsonify({"message": "Ошибка при отправке письма."}), 500

if __name__ == "__main__":
    app.run(debug=True)
