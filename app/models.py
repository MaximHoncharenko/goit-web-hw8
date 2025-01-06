from mongoengine import Document, StringField, BooleanField

class Contact(Document):
    fullname = StringField(required=True)  # Повне ім'я контакту
    email = StringField(required=True)    # Email контакту
    message_sent = BooleanField(default=False)  # Логічне поле, чи надіслано повідомлення
