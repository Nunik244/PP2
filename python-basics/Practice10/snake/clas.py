import pygame
import random

WIDTH = 800
HEIGHT = 800
GRID_SIZE = 20   
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill((255, 100, 0))   
        self.rect = self.image.get_rect()
        self.respawn()                   
    def respawn(self):
        """Создаёт еду в новом случайном месте (не двигается)"""
        self.rect.x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        self.rect.y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [(400, 400)]        
        self.direction = (GRID_SIZE, 0)   
        self.speed = 10                   
        self.score = 0
        self.grow = False

    def update(self):
        head_x = self.body[0][0] + self.direction[0]
        head_y = self.body[0][1] + self.direction[1]

        new_head = (head_x, head_y)
        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, new_direction):
        if (new_direction[0] == -self.direction[0] and new_direction[1] == 0) or \
           (new_direction[1] == -self.direction[1] and new_direction[0] == 0):
            return
        self.direction = new_direction

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 180, 0), (*segment, GRID_SIZE, GRID_SIZE))

    def check_collision(self):
        head = self.body[0]
        if (head[0] < 0 or head[0] >= WIDTH or 
            head[1] < 0 or head[1] >= HEIGHT):
            return True
        
        if head in self.body[1:]:
            return True
        return False