
import sqlite3
# Запрос на замену значений port1 и port2 на f0/0 и f0/1 для всех роутеров
def update_ports_for_routers():
    conn = sqlite3.connect('database1.db')
    cursor = conn.cursor()

    # Обновление значений port1 и port2 на f0/0 и f0/1 для всех записей с component_type 'Router'
    cursor.execute("""
        UPDATE components
        SET port1 = 'f0/1', port2 = 'f0/3'
        WHERE component_id = '2'
    """)

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

# Пример использования
update_ports_for_routers()  # Обновляем порт на f0/0 и f0/1 для всех роутеров
