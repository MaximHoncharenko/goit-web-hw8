from mongoengine import connect

def connect_to_db():
    connect(
        db="hw8",  # Назва вашої бази даних у Atlas
        host="mongodb+srv://m128axtest:0997943465@m128ax.58sei.mongodb.net/",  # Ваш URI
        retryWrites=True
    )
if __name__ == "__main__":
    connect_to_db()
    print("Підключення успішне!")