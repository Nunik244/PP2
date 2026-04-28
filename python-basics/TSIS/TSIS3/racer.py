import pygame
import random
from ui import SCREEN_WIDTH, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    """Класс игрока (машина)"""
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70)
        self.speed = 5
        self.shielded = False  # Флаг активации щита

    def move(self):
        """Движение игрока влево/вправо"""
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

class Enemy(pygame.sprite.Sprite):
    """Класс врага"""
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((50, 50, 50))  # Темно-серый цвет вместо черного
        # Добавляем красные фары
        pygame.draw.rect(self.image, (255, 0, 0), (5, 5, 10, 10))
        pygame.draw.rect(self.image, (255, 0, 0), (25, 5, 10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)
        self.speed = speed + random.uniform(-1, 2)

    def update(self):
        """Обновление позиции врага"""
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    """Класс монеты"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        # Рисуем золотую монету
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 10)
        pygame.draw.circle(self.image, (255, 165, 0), (10, 10), 7)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH-20), -50)

    def update(self):
        """Обновление позиции монеты"""
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    """Класс бонусов"""
    def __init__(self, type):
        super().__init__()
        self.type = type 
        self.image = pygame.Surface((30, 30))
        colors = {'Nitro': (0, 0, 255), 'Shield': (0, 255, 255)}
        self.image.fill(colors.get(type, (255, 255, 255)))
        # Добавляем символ на бонус
        font = pygame.font.SysFont("Arial", 15)
        symbol = "N" if type == 'Nitro' else "S"
        text = font.render(symbol, True, (255, 255, 255))
        self.image.blit(text, (10, 8))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -50)

    def update(self):
        """Обновление позиции бонуса"""
        self.rect.move_ip(0, 4)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Hazard(pygame.sprite.Sprite):
    """Класс препятствий (масляные пятна)"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (139, 69, 19), (0, 0, 50, 20))
        pygame.draw.ellipse(self.image, (100, 50, 15), (5, 5, 40, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100)

    def update(self):
        """Обновление позиции препятствия"""
        self.rect.move_ip(0, 4)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()