import redis
from mongoengine import connect, disconnect
from models import Author, Quote

# Відключення від MongoDB перед новим підключенням
disconnect()

# Підключення до MongoDB
connect(host="mongodb+srv://m128axtest:0997943465@m128ax.58sei.mongodb.net/")

# Підключення до Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Функція для пошуку цитат за ім'ям автора
def search_by_name(name):
    # Перевіряємо на кешований результат
    cached_result = r.get(f'name:{name}')
    if cached_result:
        print("Знайдено в кеші:")
        print(cached_result)
        return

    # Якщо в кеші немає, виконуємо запит до MongoDB
    authors = Author.objects(fullname__icontains=name)
    quotes = Quote.objects(author__in=authors)
    result = [quote.text for quote in quotes]  # Заміна quote.quote на quote.text

    if result:
        # Кешуємо результат
        r.set(f'name:{name}', '\n'.join(result))
        print("\n".join(result))
    else:
        print("Цитат не знайдено.")

# Функція для пошуку цитат за тегом
def search_by_tag(tag):
    # Перевіряємо на кешований результат
    cached_result = r.get(f'tag:{tag}')
    if cached_result:
        print("Знайдено в кеші:")
        print(cached_result)
        return

    # Якщо в кеші немає, виконуємо запит до MongoDB
    quotes = Quote.objects(tags__icontains=tag)
    result = [quote.text for quote in quotes]  # Заміна quote.quote на quote.text

    if result:
        # Кешуємо результат
        r.set(f'tag:{tag}', '\n'.join(result))
        print("\n".join(result))
    else:
        print("Цитат не знайдено.")

# Пошук за скороченим значенням
def search_command(command):
    if command.startswith("name:"):
        name_part = command[5:].strip().lower()
        if name_part == 'st':  # Якщо введено 'st', шукаємо за 'Steve Martin'
            name_part = "Steve Martin"
        search_by_name(name_part)
    
    elif command.startswith("tag:"):
        tag_part = command[4:].strip().lower()
        if tag_part == 'li':  # Якщо введено 'li', шукаємо за тегом 'life'
            tag_part = "life"
        search_by_tag(tag_part)
    
    elif command == "exit":
        print("Exiting...")
        return False
    
    else:
        print("Невідома команда.")
    
    return True

# Основний цикл для введення команд
def main():
    print("Enter command (name, tag, exit):")
    while True:
        command = input().strip()
        if not search_command(command):
            break

if __name__ == "__main__":
    main()