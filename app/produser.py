import pika
from mongoengine import connect
from models import Contact
from faker import Faker
import sys

# Підключення до MongoDB
connect('contacts_db', host='localhost', port=27017)

# Підключення до RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Створення черги, якщо її не існує
    channel.queue_declare(queue='email_queue')

    # Генерація фейкових контактів
    fake = Faker()

    def generate_contacts(n):
        for _ in range(n):
            contact = Contact(
                fullname=fake.name(),
                email=fake.email()
            )
            contact.save()  # Зберігаємо в MongoDB
            channel.basic_publish(
                exchange='',
                routing_key='email_queue',
                body=str(contact.id)  # Відправка ID контакту в чергу
            )
            print(f"Додано контакт: {contact.fullname}, Email: {contact.email}")
        print(f'{n} контактів надіслано в чергу.')

    # Генеруємо 10 фейкових контактів
    generate_contacts(10)
except Exception as e:
    print(f"Сталася помилка: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()  # Закриваємо з'єднання RabbitMQ
        print("З'єднання RabbitMQ закрито.")
    sys.exit(0)
