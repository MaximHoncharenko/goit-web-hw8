import pika
import sys
from models import Contact
from mongoengine import connect

# Підключення до MongoDB
connect('contacts_db', host='localhost', port=27017)

# Підключення до RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Створення черги, якщо її не існує
    channel.queue_declare(queue='email_queue')

    print("Очікування повідомлень. Для виходу натисніть Ctrl+C")

    def send_email(fullname, email):
        """Імітує надсилання email"""
        print(f"Надсилання email до: {fullname} ({email})")

    def callback(ch, method, properties, body):
        contact_id = body.decode('utf-8')
        contact = Contact.objects(id=contact_id).first()
        if contact:
            send_email(contact.fullname, contact.email)
            contact.sent = True
            contact.save()
            print(f"Повідомлення надіслано контакту: {contact.fullname}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='email_queue', on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nЗавершення роботи...")
except Exception as e:
    print(f"Сталася помилка: {e}")
finally:
    if 'connection' in locals() and connection.is_open:
        connection.close()  # Закриваємо з'єднання RabbitMQ
        print("З'єднання RabbitMQ закрито.")
    sys.exit(0)
