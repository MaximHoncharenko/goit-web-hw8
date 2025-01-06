from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

connect(db="hw8", host="mongodb+srv://hw8:0997943465@m128ax.58sei.mongodb.net/")

# Модель автора
class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

# Модель цитати
class Quote(Document):
    text = StringField(required=True)
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=2)
