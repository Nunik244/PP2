import pygame
import sys
from clac import Turtle

# Configuration
WIDTH, HEIGHT = 800, 600
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Turtle Controller")
    clock = pygame.time.Clock()

    # Create our turtle instance at the center
    my_turtle = Turtle(WIDTH // 2, HEIGHT // 2)

    while True:
        screen.fill((30, 30, 30))  # Dark background
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Shape Drawing Controls
                if event.key == pygame.K_s:
                    my_turtle.draw_square()
                elif event.key == pygame.K_c:
                    my_turtle.draw_circle()
                elif event.key == pygame.K_t:
                    my_turtle.draw_triangle()
                elif event.key == pygame.K_r:
                    my_turtle.draw_rhombus()
                
                # Movement Controls
                elif event.key == pygame.K_UP:
                    my_turtle.y -= 20
                elif event.key == pygame.K_DOWN:
                    my_turtle.y += 20
                elif event.key == pygame.K_LEFT:
                    my_turtle.x -= 20
                elif event.key == pygame.K_RIGHT:
                    my_turtle.x += 20
                
                # Clear Screen
                elif event.key == pygame.K_SPACE:
                    my_turtle.points = []

        # Rendering
        my_turtle.render(screen)
        
        # Instructions Overlay
        font = pygame.font.SysFont(None, 24)
        img = font.render("S: Square | C: Circle | T: Triangle | R: Rhombus | Arrows: Move | Space: Clear", True, (200, 200, 200))
        screen.blit(img, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()