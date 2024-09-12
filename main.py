import os
import threading_search
import multiprocessing_search
import chardet
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from colorama import init, Fore, Style

# Ініціалізація colorama
init(autoreset=True)


# Функція для вибору файлу
def choose_file():
    try:
        Tk().withdraw()  # Закриває основне вікно Tkinter
        file_path = askopenfilename(
            title="Оберіть текстовий файл для пошуку",
            filetypes=[("Text files", "*.txt")],
        )
        if file_path:
            return file_path
        else:
            print("Файл не обрано!")
            return None
    except Exception as e:
        print(Fore.RED + f"Помилка під час вибору файлу: {e}")
        return None


# Функція для зчитування тексту з файлу .txt
def read_file(file_path):
    try:
        # Визначаємо кодування файлу
        with open(file_path, "rb") as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            encoding = result["encoding"]

        # Читаємо файл з визначеним кодуванням
        with open(file_path, "r", encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        print(Fore.RED + f"Файл {file_path} не знайдено!")
        return None
    except PermissionError:
        print(Fore.RED + f"Немає дозволу на читання файлу {file_path}!")
        return None
    except Exception as e:
        print(Fore.RED + f"Помилка під час читання файлу {file_path}: {e}")
        return None


if __name__ == "__main__":
    # Вибір кількох файлів користувачем
    files = [choose_file() for _ in range(2)]  # Наприклад, обираємо 2 файли для тесту
    files = [
        file for file in files if file is not None
    ]  # Видаляємо None, якщо файл не обрано
    if files:
        # Введення ключових слів або фраз
        keywords_input = input("Введіть слова або фрази для пошуку (через кому): ")
        keywords = [
            kw.strip() for kw in keywords_input.split(",")
        ]  # Формуємо список ключових слів

        # Багатопотоковий пошук
        try:
            thread_results, thread_time = threading_search.multi_thread_search(
                files, keywords
            )
            print(Fore.GREEN + "Threading Results:", thread_results)
            print(Fore.GREEN + "Execution Time (Threads):", thread_time)
        except Exception as e:
            print(Fore.RED + f"Помилка під час багатопотокового пошуку: {e}")

        # Багатопроцесорний пошук
        try:
            process_results, process_time = multiprocessing_search.multi_process_search(
                files, keywords
            )
            print(Fore.GREEN + "Multiprocessing Results:", process_results)
            print(Fore.GREEN + "Execution Time (Processes):", process_time)
        except Exception as e:
            print(Fore.RED + f"Помилка під час багатопроцесорного пошуку: {e}")

        # Аналіз результатів
        if thread_results == process_results:
            print(Fore.GREEN + "Results are identical!")
        else:
            print(Fore.GREEN + "There are differences in the results!")

        print(
            Fore.GREEN
            + f"Threading took {thread_time:.2f} seconds, while multiprocessing took {process_time:.2f} seconds."
        )
    else:
        print(Fore.RED + "Не вдалося вибрати файли для пошуку.")
