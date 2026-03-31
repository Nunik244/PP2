import psycopg2
from config import load_config

def insert_contacts():
    """ Добавление контактов в таблицу """
    # Список кортежей с данными
    contacts = [
        ('Eslan', '+777777777'),
        ('Arman', '+77012223344'),
        ('Olga', '+77055556677')
    ]
    
    # SQL запрос с плейсхолдерами (%s), чтобы избежать SQL-инъекций
    sql = "INSERT INTO phonebook (contact_name, phone_number) VALUES (%s, %s)"
    
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # executemany эффективнее для вставки нескольких строк сразу
                cur.executemany(sql, contacts)
            # В блоке with conn коммит (сохранение) происходит автоматически
            print(f"Успешно добавлено {len(contacts)} контакта(ов).")
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Ошибка при вставке: {error}")

if __name__ == '__main__':
    insert_contacts()