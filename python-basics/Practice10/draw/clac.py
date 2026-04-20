import pygame
import math

class Turtle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 255, 0)  # Green turtle
        self.drawing_color = (255, 255, 255)  # White lines
        self.points = []  # To store drawing paths

    def draw_square(self, size=100):
        # Coordinates: (x, y), (x+s, y), (x+s, y+s), (x, y+s)
        pts = [(self.x, self.y), (self.x + size, self.y), 
               (self.x + size, self.y + size), (self.x, self.y + size)]
        self.points.append(('polygon', pts))

    def draw_circle(self, radius=50):
        # Store as type, center, and radius
        self.points.append(('circle', (int(self.x), int(self.y)), radius))

    def draw_triangle(self, size=100):
        # Equilateral-ish triangle
        height = int(size * (math.sqrt(3) / 2))
        pts = [(self.x, self.y), (self.x + size, self.y), (self.x + size // 2, self.y - height)]
        self.points.append(('polygon', pts))

    def draw_rhombus(self, size=100):
        # Diamond shape
        pts = [(self.x, self.y), (self.x + size//2, self.y - size//2), 
               (self.x + size, self.y), (self.x + size//2, self.y + size//2)]
        self.points.append(('polygon', pts))

    def render(self, surface):
        # Draw all stored shapes
        for shape in self.points:
            if shape[0] == 'polygon':
                pygame.draw.polygon(surface, self.drawing_color, shape[1], 2)
            elif shape[0] == 'circle':
                pygame.draw.circle(surface, self.drawing_color, shape[1], shape[2], 2)
        
        # Draw the "Turtle" (a small circle)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 10)