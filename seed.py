import json
from mongoengine import connect, disconnect
from models import Author, Quote
from mongoengine.errors import DoesNotExist

disconnect()
# Підключення до MongoDB Atlas
connect(host="mongodb+srv://m128axtest:0997943465@m128ax.58sei.mongodb.net/")

# Завантаження авторів
def load_authors():
    with open("authors.json", "r") as file:
        authors_data = json.load(file)

    for author in authors_data:
        try:
            # Спробуйте знайти автора
            existing_author = Author.objects.get(fullname=author["fullname"])
        except DoesNotExist:
            # Якщо автора не існує, створіть нового
            new_author = Author(
                fullname=author["fullname"],
                born_date=author["born_date"],
                born_location=author["born_location"],
                description=author["description"],
            )
            new_author.save()
            print(f"Author {author['fullname']} created.")
        else:
            print(f"Author {author['fullname']} already exists.")

# Завантаження цитат
def load_quotes():
    with open("qoutes.json", "r", encoding="utf-8") as file:
        quotes = json.load(file)
        for quote in quotes:
            author = Author.objects(fullname=quote["author"]).first()
            if author:
                new_quote = Quote(
                    text=quote["quote"],
                    tags=quote.get("tags", []),
                    author=author
                )
                new_quote.save()
                print(f"Quote added: {new_quote.text}")

if __name__ == "__main__":
    load_authors()
    load_quotes()
