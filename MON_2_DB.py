import asyncio
import telnetlib3
import re
import sqlite3

# Функция для обновления статуса линии в базе данных
def update_line_status(line, status):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('database1.db')
    cursor = conn.cursor()

    # Обновление статуса линии в таблице components
    cursor.execute("""
        UPDATE components
        SET status = ?
        WHERE line = ?
    """, (status, line))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

# Функция для проверки состояния линий на терминальном сервере
async def check_terminal_server(host, username, password, first_line, last_line):
    try:
        # Подключение к серверу
        reader, writer = await telnetlib3.open_connection(host, 23)

        # Ожидание приглашения для ввода имени пользователя
        while True:
            output = await reader.read(1024)
            if "Username:" in output:
                writer.write(username + "\n")
                break

        # Ожидание приглашения для ввода пароля
        while True:
            output = await reader.read(1024)
            if "Password:" in output:
                writer.write(password + "\n")
                break

        # Ожидание приглашения командной строки
        while True:
            output = await reader.read(1024)
            if ">" in output or "#" in output:
                break

        # Отправка команды для проверки состояния линий
        command = f"show line {first_line} {last_line} summary\n"
        writer.write(command)
        await asyncio.sleep(1)  # Даем время для выполнения команды

        # Чтение вывода команды
        output = await reader.read(1024)

        # Закрытие соединения
        writer.write("exit\n")
        await writer.drain()
        writer.close()

        # Парсим и выводим линии
        parsed_output = parse_line_status(output, first_line, last_line)

        print(f"\n===== PARSED DATA FROM {host} (Lines {first_line}-{last_line}) =====")
        print(parsed_output)
        print("====================================\n")

        # Обновление статуса линий в базе данных
        update_line_status_in_db(parsed_output)

    except Exception as e:
        print(f"\n===== SERVER: {host} =====\nError while connecting: {e}\n====================================\n")

# Функция для парсинга вывода команды с учетом пробелов как разделителей групп
def parse_line_status(output, first_line, last_line):
    lines = output.split("\n")
    parsed_data = []
    current_line = first_line  # Начинаем с первой указанной линии

    for line in lines:
        match = re.match(r"\s*\d+\/\d+\/\d+:\s+(.+)", line.strip())  # Ищем строку со статусами
        if match:
            status_groups = match.group(1).strip().split()  # Разбиваем строку по пробелам (учитываем группы)

            for group in status_groups:
                for char in group:
                    if current_line > last_line:
                        break  # Останавливаемся, если вышли за границу

                    # Переводим статусы на английский
                    if char == "-":
                        status = "available"
                    elif char.lower() == "u":
                        status = "in use"
                    elif char == "?":
                        status = "unverified"
                    else:
                        status = "unknown"

                    parsed_data.append((current_line, status))  # Сохраняем как кортеж (линия, статус)
                    current_line += 1

    # Если мы не дошли до last_line, добавляем оставшиеся линии как "unknown"
    while current_line <= last_line:
        parsed_data.append((current_line, "unknown"))
        current_line += 1

    return parsed_data

# Функция для обновления статуса линий в базе данных
def update_line_status_in_db(parsed_data):
    for line, status in parsed_data:
        update_line_status(line, status)

# Данные для подключения
username = "admin"
password = "@#$-wer-SDF-xcv"

# Список серверов и их диапазонов линий
servers = [
    {"host": "10.40.68.3", "first_line": 3, "last_line": 34},
    {"host": "10.40.83.2", "first_line": 34, "last_line": 49},
]

# Асинхронная функция для проверки всех серверов
async def main():
    tasks = [check_terminal_server(server["host"], username, password, server["first_line"], server["last_line"]) for server in servers]
    await asyncio.gather(*tasks)

# Запуск асинхронного цикла
asyncio.run(main())
