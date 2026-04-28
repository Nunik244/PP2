import pygame
import random

# Глобальные константы игры
CELL_SIZE = 20      # Размер одной клетки в пикселях
WIDTH, HEIGHT = 800, 600  # Размер игрового окна

class GameObject:
    """
    Базовый класс для всех игровых объектов.
    Содержит координаты x, y на поле.
    """
    def __init__(self, x, y):
        self.x = x  # Координата X в пикселях
        self.y = y  # Координата Y в пикселях

class PowerUp(GameObject):
    """
    Класс бонусов (ускорение, замедление, щит).
    Наследуется от GameObject.
    """
    def __init__(self, p_type, x, y):
        super().__init__(x, y)
        self.type = p_type  # Тип: 'speed', 'slow', 'shield'
        self.spawn_time = pygame.time.get_ticks()  # Время появления в мс
        self.is_active = False  # Активен ли эффект
        self.activation_time = 0  # Время активации эффекта
        
    def is_expired(self, current_time):
        """
        Проверяет, исчез ли бонус с поля (через 8 секунд).
        Возвращает True, если бонус нужно удалить.
        """
        return not self.is_active and (current_time - self.spawn_time > 8000)
    
    def effect_expired(self, current_time):
        """
        Проверяет, закончился ли эффект бонуса (через 5 секунд).
        Для щита эффект бесконечный до использования.
        Возвращает True, если эффект нужно отключить.
        """
        if self.is_active and self.type != 'shield':
            return current_time - self.activation_time > 5000
        return False

class PoisonFood(GameObject):
    """
    Класс ядовитой еды.
    При съедании укорачивает змейку на 2 сегмента.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (139, 0, 0)  # Темно-красный цвет
        self.spawn_time = pygame.time.get_ticks()  # Время появления

class Food(GameObject):
    """
    Класс обычной еды с разными типами.
    Типы: normal (обычная), golden (золотая), timer (исчезающая).
    """
    def __init__(self, x, y, food_type="normal"):
        super().__init__(x, y)
        self.type = food_type  # Тип еды
        self.spawn_time = pygame.time.get_ticks()  # Время появления
        
        # Вес (очки) для каждого типа еды
        self.points = {
            'normal': 10,   # Обычная - 10 очков
            'golden': 30,   # Золотая - 30 очков
            'timer': 5      # Исчезающая - 5 очков
        }
        
    def is_expired(self, current_time):
        """
        Проверяет, исчезла ли еда с поля.
        Только 'timer' еда исчезает через 5 секунд.
        """
        if self.type == 'timer':
            return current_time - self.spawn_time > 5000
        return False
    
    def get_points(self):
        """Возвращает количество очков за этот тип еды."""
        return self.points.get(self.type, 10)

def get_random_position(avoid_positions=[]):
    """
    Генерирует случайную позицию на игровом поле.
    Параметр avoid_positions: список позиций, которые нужно избегать.
    Возвращает: [x, y] координаты в пикселях.
    """
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        if [x, y] not in avoid_positions:
            return [x, y]