import sqlite3

# Подключение к базе данных SQLite (создаст файл, если он не существует)
conn = sqlite3.connect('database1.db')
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
    CREATE TABLE IF NOT EXISTS components (
        component_id INTEGER PRIMARY KEY,
        component_type TEXT,
        location INTEGER,   
        model TEXT,
        status TEXT,
        line INTEGER, 
        port1 TEXT,
        port2 TEXT,
        groups_id INTEGER DEFAULT NULL  
    )
""")
print("Таблица 'components' успешно создана.")

# Вставка данных в таблицу
cursor.execute("""
    UPDATE  components (component_type, location, model, status, line, port1, port2, groups_id)
    VALUES
    ('Switch', 344, 'Cisco', 'inactive', 37, 'GigabitEthernet0/1', 'GigabitEthernet0/2', NULL),
    ('Switch', 344, 'Huawei', 'inactive', 36, 'GigabitEthernet1/1', 'GigabitEthernet1/2', 1),
    ('Router', 224, 'Cisco', 'inactive', 15, 'GigabitEthernet2/1', 'GigabitEthernet2/2', 2),
    ('Router', 224, 'Cisco', 'inactive', 17, 'GigabitEthernet2/1', 'GigabitEthernet2/2', 2)
""")
print("Данные успешно добавлены в таблицу 'components'.")

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
