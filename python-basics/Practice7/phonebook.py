import psycopg2
from config import load_config

# 1. Объявляем функции СНАРУЖИ, чтобы не пересоздавать их каждый раз
def add_user(cur, conn, user, password):
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cur.execute(sql, (user, password))
    conn.commit()
    print("Добавлено!")

def update_pass(cur, conn, user, newpass):
    sql = "UPDATE users SET password = %s WHERE username = %s"
    cur.execute(sql, (newpass, user))
    conn.commit()
    print("Обновлено!")

def delete_user(cur, conn, username):
    sql = "DELETE FROM users WHERE username = %s"
    cur.execute(sql, (username,))
    conn.commit()
    print("Удалено!")

def main():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                
                while True:
                    print("\n1-INSERT | 2-DELETE | 3-SELECT | 4-UPDATE | 0-STOP")
                    choice = input("Выбери действие: ")

                    if choice == '0':
                        break
                    
                    if choice == '1':
                        name = input("Имя: ")
                        pw = input("Номер: ")
                        add_user(cur, conn, name, pw)
                        
                    elif choice == '2':
                        name = input("Кого удалить?: ")
                        delete_user(cur, conn, name)
                        
                    elif choice == '4':
                        name = input("Кому меняем?: ")
                        pw = input("Новый номер: ")
                        update_pass(cur, conn, name, pw)
                    
                    elif choice == '3':
                        # Маленький спойлер про SELECT
                        cur.execute("SELECT * FROM users")
                        rows = cur.fetchall()
                        for row in rows:
                            print(row)
                    else:
                        print("Нет такой команды")

    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Ошибка: {error}")

if __name__ == '__main__':
    main()