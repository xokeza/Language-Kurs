quiz = [
    {
        "question": "Какой вызов print() выведет на экран слово goodbye?",
        "options": ["print('goodbye')", "print goodbye", "'goodbye'"],
        "correct_answer": "print('goodbye')",
    },
    {
        "question": "Что важно для имени команды print в Python?",
        "options": [
            "Важно только число букв, а не их регистр",
            "Регистр важен: print и Print - разные имена",
            "Регистр не важен: print и Print работают одинаково",
        ],
        "correct_answer": "Регистр важен: print и Print - разные имена",
    },
    {
        "question": "Что обязательно нужно сделать, чтобы Python понял, что Hello, World! — это строка?",
        "options": [
            "Написать текст заглавными буквами",
            "Поставить точку с запятой в конце строки",
            "Взять текст в кавычки",
        ],
        "correct_answer": "Взять текст в кавычки",
    },
    {
        "question": "Какой вариант записи строки в print() корректен в Python?",
        "options": ["print('Hello\")", 'print("Hello")', "print(Hello)"],
        "correct_answer": 'print("Hello")',
    },
    {
        "question": "Что выведет этот код?\n   print('Hexlet')",
        "options": ["Ничего не выведет", "Hexlet", "'Hexlet'"],
        "correct_answer": "Hexlet",
    },
]


def run_quiz():
    score = 0

    for num, item in enumerate(quiz, 1):
        print(f"\nВопрос {num}: {item['question']}")

        for index, option in enumerate(item["options"], 1):
            print(f"{index}. {option}")

        try:
            user_choice = int(
                input(f"\nВведите номер вашего ответа (1-{len(item['options'])}): ")
            )

            selected_answer = item["options"][user_choice - 1]

            if selected_answer == item["correct_answer"]:
                print("Правильно!")
                score += 1
            else:
                print(f"Неверно. Правильный ответ: {item['correct_answer']}")

        except (ValueError, IndexError):
            print(
                f"Ошибка ввода! Нужно было ввести число от 1 до {len(item['options'])}."
            )
            print(f"Правильный ответ был: {item['correct_answer']}")

    print(f"\nТест окончен! Вы набрали {score} из {len(quiz)} баллов.")


if __name__ == "__main__":
    run_quiz()
