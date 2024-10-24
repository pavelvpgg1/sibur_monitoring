import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "bogodpav@gmail.com"  # константа, емаил с которого идут письма
PASSWORD = "nwyc fhwc wsvi krnm"  # константа, пароль емаила с которого идут письма


class Email:
    def __init__(self, priority, description, message, status, type, author, receiver_email):
        self.priority = priority
        self.description = description
        self.message = message
        self.status = status
        self.type = type
        self.author = author
        self.receiver_email = receiver_email

    def send_new_email(self):
        subject = "ПРОБЛЕМА"  # заголовок письма
        body = f"Здравствуйте! Произошла проблема {self.description}, с приоритетом {self.priority}, где сотрудник {self.author}, сообщил о {self.message}. На данном этапе статус проблемы {self.status}, тип проблемы связан с {self.type}"  # что будет в письме
        msg = MIMEMultipart()  # объект, позволяющий добавлять различные части к сообщению (например, текст, вложения)
        msg['From'] = SENDER_EMAIL  # устанавливаем кто отправитель
        msg['To'] = self.receiver_email  # устанавливаем кому отправляем
        msg['Subject'] = subject  # устанавливаем заголовок письма
        msg.attach(MIMEText(body,
                            'plain'))  # присоединяет текстовое содержимое к сообщению, указывая, что это обычный текст (plain text)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)  # Подключение к SMTP-серверу Gmail
            server.starttls()  # Используем TLS (протокол подлючения для порта 587)
            server.login(SENDER_EMAIL, PASSWORD)  # Аутентификация

            server.sendmail(SENDER_EMAIL, self.receiver_email, msg.as_string())  # Отправка письма
            print("Письмо отправлено успешно!")

        except Exception as e:
            print(f"Произошла ошибка: {e}")

        finally:
            server.quit()  # Закрытие соединения


objectClass = Email(priority="CRIT",
                    description="Миша упал с лестницы",
                    message="Мишаня упал с лестницы на пятом этаже в плавильне, что-то сломал вроде",
                    status="START", type="медики", author="Иванович Иван Иванов",
                    receiver_email="9ipro1@gmail.com"
                    )
objectClass.send_new_email()  # отправить новое письмо
