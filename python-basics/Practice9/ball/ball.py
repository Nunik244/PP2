import pygame
import random
x = 500
y = 500
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Super ball")
done = False
clock = pygame.time.Clock()
image = pygame.image.load('ball.png')
my_font = pygame.font.SysFont("Arial", 48)
text_surface = my_font.render("No baby you can't get out of this display", True, (255, 255, 255))
def No():
    screen.fill((255,0,0))
    screen.blit(text_surface,(100,400))
    screen.blit(image,(500,500))
    pygame.display.flip()
    pygame.time.wait(2000) 




while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((255, 255, 255))  

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 3
    if pressed[pygame.K_DOWN]: y += 3
    if pressed[pygame.K_LEFT]: x -= 3
    if pressed[pygame.K_RIGHT]: x += 3
    # Creating limits--------------------------
    if x > 960:
        x -= 3 
        No()
        continue
    if x < -15: 
        x += 3
        No()
        continue
    if y < -15: 
        y+=3
        No()
        continue
    elif y > 960: 
        y -=3
        No()
        continue
    #-----------------------------------------------
    screen.blit(image,(x,y))
    pygame.display.flip()
    clock.tick(60)