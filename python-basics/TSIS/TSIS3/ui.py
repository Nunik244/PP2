import pygame

# Константы
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (200, 200, 0)

class Button:
    """Класс для создания кнопок"""
    def __init__(self, text, x, y, w, h, color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.action = action
        self.hover_color = tuple(min(c + 50, 255) for c in color)
        self.current_color = color

    def draw(self, screen, font):
        """Отрисовка кнопки с эффектом наведения"""
        # Проверяем наведение мыши
        mouse_pos = pygame.mouse.get_pos()
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)  # Рамка
        
        txt_surf = font.render(self.text, True, WHITE)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, txt_rect)

    def is_clicked(self, pos):
        """Проверяет, нажата ли кнопка"""
        return self.rect.collidepoint(pos)

def draw_text(screen, text, size, x, y, color=BLACK, center=False):
    """Универсальная функция для отрисовки текста"""
    font = pygame.font.SysFont("Verdana", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)