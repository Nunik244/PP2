import psycopg2
from psycopg2 import OperationalError, IntegrityError
from datetime import datetime

class Database:
    """
    Класс для управления подключением к PostgreSQL и операциями с БД.
    Хранит игроков и их игровые сессии.
    """
    
    def __init__(self):
        """
        Конструктор: создает подключение к БД и инициализирует таблицы.
        Параметры подключения: имя БД, пользователь, пароль, хост.
        """
        self.conn = None
        self.cursor = None
        self.available = False  # Флаг доступности БД
        try:
            self.conn = psycopg2.connect(
                dbname="snake_db",
                user="postgres",
                password="12345678",
                host="localhost",
                port="5432"
            )
            self.conn.autocommit = False  # Отключаем автокоммит для лучшего контроля
            self.cursor = self.conn.cursor()
            self._create_tables()
            self.available = True
            print("Database connected successfully!")
        except Exception as e:
            print(f"Database connection error: {e}")
            print("Playing in offline mode (scores won't be saved)")

    def _rollback(self):
        """Откатывает текущую транзакцию при ошибке"""
        try:
            if self.conn:
                self.conn.rollback()
        except:
            pass

    def _create_tables(self):
        """
        Создает таблицы в БД, если они не существуют.
        """
        if not self.available:
            return
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                );
            """)
            self.conn.commit()
            print("Tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
            self._rollback()
            self.available = False

    def get_or_create_player(self, username):
        """
        Возвращает ID игрока из БД.
        Если игрока с таким именем нет - создает нового.
        """
        if not self.available:
            return hash(username) % 10000
        
        try:
            # Пытаемся получить существующего игрока
            self.cursor.execute("SELECT id FROM players WHERE username = %s;", (username,))
            result = self.cursor.fetchone()
            
            if result:
                return result[0]
            
            # Если не существует, создаем нового
            self.cursor.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id;",
                (username,)
            )
            player_id = self.cursor.fetchone()[0]
            self.conn.commit()
            return player_id
            
        except IntegrityError:
            # Конфликт уникальности - кто-то создал игрока между запросами
            self._rollback()
            try:
                self.cursor.execute("SELECT id FROM players WHERE username = %s;", (username,))
                return self.cursor.fetchone()[0]
            except:
                return hash(username) % 10000
        except Exception as e:
            print(f"Error getting/creating player: {e}")
            self._rollback()
            return hash(username) % 10000

    def save_session(self, player_id, score, level):
        """
        Сохраняет результаты игровой сессии в БД.
        """
        if not self.available:
            print(f"[Offline] Score saved: {score}, Level: {level}")
            return
            
        if player_id is None:
            return
            
        try:
            self.cursor.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);",
                (player_id, score, level)
            )
            self.conn.commit()
            print(f"Session saved: Score={score}, Level={level}")
        except Exception as e:
            print(f"Error saving session: {e}")
            self._rollback()

    def get_top_10(self):
        """
        Возвращает топ-10 лучших результатов из БД.
        """
        if not self.available:
            return []
            
        try:
            # Сначала откатываем любую зависшую транзакцию
            self._rollback()
            
            query = """
                SELECT p.username, s.score, s.level_reached, 
                       TO_CHAR(s.played_at, 'DD-MM-YY') as play_date
                FROM game_sessions s 
                JOIN players p ON s.player_id = p.id 
                ORDER BY s.score DESC 
                LIMIT 10;
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            self.conn.commit()
            print(f"Retrieved {len(results)} top scores")
            return results
        except Exception as e:
            print(f"Error getting top 10: {e}")
            self._rollback()
            return []

    def get_personal_best(self, player_id):
        """
        Возвращает лучший результат игрока.
        """
        if not self.available:
            return 0
            
        if player_id is None:
            return 0
            
        try:
            # Откатываем зависшую транзакцию
            self._rollback()
            
            self.cursor.execute(
                "SELECT MAX(score) FROM game_sessions WHERE player_id = %s;",
                (player_id,)
            )
            result = self.cursor.fetchone()
            self.conn.commit()
            best = result[0] if result and result[0] is not None else 0
            return best
        except Exception as e:
            print(f"Error getting personal best: {e}")
            self._rollback()
            return 0

    def close(self):
        """Закрывает соединение с БД."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
                print("Database connection closed")
        except Exception as e:
            print(f"Error closing database: {e}")