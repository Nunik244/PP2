import pygame
import math

class Turtle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 255, 0)  
        self.drawing_color = (255, 255, 255)  
        self.points = []  

    def draw_square(self, size=100):
        pts = [(self.x, self.y), (self.x + size, self.y), 
               (self.x + size, self.y + size), (self.x, self.y + size)]
        self.points.append(('polygon', pts))

    def draw_circle(self, radius=50):
        self.points.append(('circle', (int(self.x), int(self.y)), radius))

    def draw_triangle(self, size=100):
        height = int(size * (math.sqrt(3) / 2))
        pts = [(self.x, self.y), (self.x + size, self.y), (self.x + size // 2, self.y - height)]
        self.points.append(('polygon', pts))

    def draw_rhombus(self, size=100):
        pts = [(self.x, self.y), (self.x + size//2, self.y - size//2), 
               (self.x + size, self.y), (self.x + size//2, self.y + size//2)]
        self.points.append(('polygon', pts))

    def render(self, surface):
        for shape in self.points:
            if shape[0] == 'polygon':
                pygame.draw.polygon(surface, self.drawing_color, shape[1], 2)
            elif shape[0] == 'circle':
                pygame.draw.circle(surface, self.drawing_color, shape[1], shape[2], 2)
        
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 10)