import os
import subprocess


def run_checker():
    print("=" * 60)
    print("ЗАДАНИЕ: Напишите скрипт, который создаёт переменную b")
    print("со значением 5 и выводит её в консоль.")
    print("=" * 60)

    filename = input(
        "\nВведите название файла с вашим решением (например, solution.py): "
    ).strip()

    if not os.path.exists(filename):
        print(f"Ошибка: Файл '{filename}' не найден в текущей папке!")
        return

    print(f"\n Запускаем и проверяем файл '{filename}'...")

    try:
        result = subprocess.run(
            ["python", filename], capture_output=True, text=True, timeout=5
        )

        user_output = result.stdout.strip()
        user_stderr = result.stderr.strip()

        if result.returncode != 0:
            print("Ошибка: Ваш код не смог запуститься!")
            print(f"Текст ошибки:\n{user_stderr}")
            return

        with open(filename, "r", encoding="utf-8") as file:
            student_code = file.read()

        is_output_correct = user_output == "5"
        has_variable_b = "b" in student_code

        if is_output_correct and has_variable_b:
            print("Проверка пройдена! Задание выполнено идеально.")
            print(f"Полученный вывод в консоли: {user_output}")
        else:
            print("Задание выполнено неверно.")
            print(" Ожидалось, что программа выведет '5'.")
            print(f"Ваша программа вывела: '{user_output}'")

            if not has_variable_b:
                print(" Подсказка: Кажется, вы не создали переменную с именем 'b'.")

    except subprocess.TimeoutExpired:
        print("Ошибка: Скрипт выполнялся слишком долго (возможно, зациклился).")
    except Exception as e:
        print(f"Произошла ошибка при тестировании: {e}")


if __name__ == "__main__":
    run_checker()
