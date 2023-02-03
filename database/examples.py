from database.db import register, login, questions, question_category

if register("Admin", "root"):
    print("Dodano")
else:
    print("Taki użytkownik już istniej")

if login("Admin", "root"):
    print("Zalogowano")
else:
    print("Nie zalogowano")

categories = question_category()
for item in categories:
    print(item.question_category_name)

questions = questions(5, 1)
for item in questions:
    print(item.question_text, " ", item.question_answer)