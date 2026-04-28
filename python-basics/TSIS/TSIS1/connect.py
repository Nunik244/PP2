import psycopg2
from config import load_config

def execute_query(query, params=None, fetch=False):
    """Универсальный помощник для работы с БД с обработкой ошибок"""
    conn = None
    try:
        # Загружаем конфиг и подключаемся
        params_db = load_config()
        conn = psycopg2.connect(**params_db)
        
        with conn.cursor() as cur:
            cur.execute(query, params)
            
            # Если это SELECT, возвращаем данные
            if fetch:
                return cur.fetchall()
            
            # Если это INSERT/UPDATE/DELETE, фиксируем изменения
            conn.commit()
            return None

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при работе с базой данных: {error}")
        if conn:
            conn.rollback() # Откатываем изменения при ошибке
    finally:
        if conn:
            conn.close() # Закрываем соединение в любом случае