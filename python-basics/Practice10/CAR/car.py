import pygame
import random
import os

# ====================== КЛАССЫ ======================

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        path = os.path.join(os.path.dirname(__file__), "images", "car.png")
        self.image = pygame.transform.scale(pygame.image.load(path), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 650)
        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 800:
            self.rect.y += self.speed


class Road:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), "images", "road.png")
        self.image = pygame.transform.scale(pygame.image.load(path), (800, 800))
        self.y1 = 0
        self.y2 = -800
        self.speed = 5

    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed
        if self.y1 >= 800:
            self.y1 = -800
        if self.y2 >= 800:
            self.y2 = -800

    def draw(self, surface):
        surface.blit(self.image, (0, self.y1))
        surface.blit(self.image, (0, self.y2))


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        path = os.path.join(os.path.dirname(__file__), "images", "coin.png")
        self.image = pygame.transform.scale(pygame.image.load(path), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(40, 760)
        self.rect.y = -70
        self.speed = random.randint(5, 9)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 800:
            self.kill()