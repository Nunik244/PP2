import pygame
import datetime
x = 0
y = 0
pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Super ball")
done = False
clock = pygame.time.Clock()
image = pygame.image.load('ball.png')

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

    screen.blit(image,(x,y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()