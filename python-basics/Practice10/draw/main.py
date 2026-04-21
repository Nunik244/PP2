import pygame
import sys
from clac import Turtle

WIDTH, HEIGHT = 800, 600
FPS = 60
r = 0
g = 0
b = 0

def main():
    global r, g, b
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Turtle Controller")
    clock = pygame.time.Clock()

    my_turtle = Turtle(WIDTH // 2, HEIGHT // 2)

    while True:
        screen.fill((30, 30, 30)) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    my_turtle.draw_square()
                elif event.key == pygame.K_c:
                    my_turtle.draw_circle()
                elif event.key == pygame.K_t:
                    my_turtle.draw_triangle()
                elif event.key == pygame.K_r: 
                    my_turtle.draw_rhombus()
                
                elif event.key == pygame.K_UP:
                    my_turtle.y -= 20
                elif event.key == pygame.K_DOWN:
                    my_turtle.y += 20
                elif event.key == pygame.K_LEFT:
                    my_turtle.x -= 20
                elif event.key == pygame.K_RIGHT:
                    my_turtle.x += 20
                
                elif event.key == pygame.K_SPACE:
                    my_turtle.points = []
                elif event.key == pygame.K_1:
                    r = (r + 10) % 256
                    my_turtle.color = (r, g, b)
                    my_turtle.drawing_color = (r, g, b) 
                elif event.key == pygame.K_2:
                    g = (g + 10) % 256
                    my_turtle.color = (r, g, b)
                    my_turtle.drawing_color = (r, g, b) 
                elif event.key == pygame.K_3:
                    b = (b + 10) % 256
                    my_turtle.color = (r, g, b)
                    my_turtle.drawing_color = (r, g, b)  
                elif event.key == pygame.K_0:
                    r, g, b = 0, 0, 0
                    my_turtle.color = (r, g, b)
                    my_turtle.drawing_color = (r, g, b)  

        my_turtle.render(screen)
        
        font = pygame.font.SysFont(None, 24)
        instructions = "S/C/T/R: Shapes | Arrows: Move | 1/2/3: R/G/B | 0: Reset Color | Space: Clear"
        img = font.render(instructions, True, (200, 200, 200))
        screen.blit(img, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()