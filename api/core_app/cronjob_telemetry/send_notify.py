
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from api.core_app.models import User


def send_mail_notify(client, response, txt_type):
    user = User.objects.filter(id=client['user']).first()
    subject = (
        '{} / {} / {}  - Incidencia!').format(client['name_client'], client['title'], txt_type)
    subject = subject.replace('\n', '')
    from_email = '<no-reply@smarthydro.cl>'
    content = render_to_string(
        'notify.html',
        {'client': client, 'response': response,
            'user': user, 'txt_type': txt_type}
    )

    msg = EmailMultiAlternatives(subject, content, from_email, [
                                 "felipe.barraza.vega@gmail.com"])
    msg.attach_alternative(content, "text/html")
    try:
        msg.send()
    except Exception as e:
        print(e)


def send_mail_notified_not_conection(client, variable, e):
    user = User.objects.filter(id=client['user']).first()
    txt = "Tiempo de espera agotado"
    subject = (
        '{} / {} / {}').format(client['name_client'], client['title'], str(txt))
    subject = subject.replace('\n', '')
    from_email = '<no-reply@smarthydro.cl>'
    date_medition = datetime.datetime.now()
    print(variable)
    content = render_to_string(
        'notify_timeout.html',
        {'client': client, 'user': user, 'variable': variable,
            'date_medition': date_medition, 'error': e}
    )

    msg = EmailMultiAlternatives(subject, content, from_email, [
                                 "felipe.barraza.vega@gmail.com"])
    msg.attach_alternative(content, "text/html")
    try:
        msg.send()
    except Exception as e:
        print(e)
