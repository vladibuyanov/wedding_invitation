from flask import request
from flask_mail import Message


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
