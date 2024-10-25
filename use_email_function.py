import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "bogodpav@gmail.com"  # константа, емаил с которого идут письма
PASSWORD = "nwyc fhwc wsvi krnm"  # константа, пароль емаила с которого идут письма


class Email:
    def __init__(self, priority, receiver_email, description=None, message=None, status=None, type=None, author=None,
                 time="data_from_DB"):
        self.priority = priority  # приоритет
        self.description = description  # название
        self.message = message  # описание
        self.status = status  # статус
        self.type = type  # тип
        self.author = author  # автор
        self.receiver_email = receiver_email  # кому отправляем
        self.time = time  # время

    def send_new_email(self):
        subject = self.description if self.description else "ПРОБЛЕМА"  # заголовок письма

        # HTML-содержимое письма
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="color: #E03C31;">{subject}</h1>
                <p>Здравствуйте! В <strong>{self.time}</strong> произошла проблема.</p>
        """
        if self.priority:
            body += f"<p><strong>Приоритет:</strong> {self.priority}</p>"
        if self.author:
            body += f"<p><strong>Сообщение от:</strong> {self.author}</p>"
        if self.message:
            body += f"<p><strong>Подробности:</strong> {self.message}</p>"
        if self.status:
            body += f"<p><strong>Статус проблемы:</strong> {self.status}</p>"
        if self.type:
            body += f"<p><strong>Тип проблемы:</strong> {self.type}</p>"

        body += """
                <p style="color: #999;">С уважением,<br>Команда СИБУР</p>
            </body>
        </html>
        """

        msg = MIMEMultipart()  # объект, позволяющий добавлять различные части к сообщению (например, текст, вложения)
        msg['From'] = SENDER_EMAIL  # устанавливаем кто отправитель
        msg['To'] = self.receiver_email  # устанавливаем кому отправляем
        msg['Subject'] = subject  # устанавливаем заголовок письма
        msg.attach(MIMEText(body, 'html'))  # присоединяет HTML-содержимое к сообщению

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)  # Подключение к SMTP-серверу Gmail
            server.starttls()  # Используем TLS (протокол подключения для порта 587)
            server.login(SENDER_EMAIL, PASSWORD)  # Аутентификация

            server.sendmail(SENDER_EMAIL, self.receiver_email, msg.as_string())  # Отправка письма
            print("Письмо отправлено успешно!")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

        finally:
            server.quit()  # Закрытие соединения


objectClass = Email(
    priority="CRIT",
    description="Миша упал",
    message="Мишаня упал с лестницы на пятом этаже в плавильне, что-то сломал вроде",
    status="START",
    type="сварщик",
    author="Иванович Иван Иванов",
    receiver_email="9ipro1@gmail.com"
)
objectClass.send_new_email()  # отправить новое письмо
