import pandas as pd
import sqlite3


def get_active_devices(db_filename):
    try:
        conn = sqlite3.connect(db_filename)
        query = "SELECT * FROM components WHERE status = 'Active'"
        devices = pd.read_sql_query(query, conn)
        print(devices)
        conn.close()
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def update_status_to_using(db_filename):
    try:
        with sqlite3.connect(db_filename) as conn:
            cursor = conn.cursor()

            query_update = """
                UPDATE components
                SET status = 'Using'
                WHERE status = 'Active'
            """
            cursor.execute(query_update)
            conn.commit()
            print("Статусы обновлены: Active -> Using")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    data = 'mydatabase.db'
    print("Активные устройства до обновления статуса:")
    get_active_devices(data)
    update_status_to_using(data)
    print("Активные устройства после обновления статуса:")
    get_active_devices(data)
