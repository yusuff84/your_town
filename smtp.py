import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendemail(lst, data):
    print(data)
    print(lst)
    msg = MIMEMultipart()
    msg['From'] = 'yusuff84@yandex.ru'
    recipients = lst
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = 'Новое событие в вашем городе !'
    message = data['content']
    msg.attach(MIMEText(message))
    try:
        mailserver = smtplib.SMTP('smtp.yandex.ru', 587)
        mailserver.set_debuglevel(True)
        # Определяем, поддерживает ли сервер TLS
        mailserver.ehlo()
        # Защищаем соединение с помощью шифрования tls
        mailserver.starttls()
        # Повторно идентифицируем себя как зашифрованное соединение перед аутентификацией.
        mailserver.ehlo()
        mailserver.login('yusuff84@yandex.ru', 'xmia195x')

        mailserver.sendmail('yusuff84@yandex.ru', lst, msg.as_string())

        mailserver.quit()
        print("Письмо успешно отправлено")
    except smtplib.SMTPException:
        print("Ошибка: Невозможно отправить сообщение")
