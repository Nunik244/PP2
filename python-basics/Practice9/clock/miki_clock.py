import pygame
import datetime

pygame.init()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("Mickey Clock")
done = False
clock = pygame.time.Clock()

image = pygame.image.load('miki.png')
sec_img = pygame.image.load('dir.png')

def rot_center(image, angle):
    rotated_image = pygame.transform.rotate(image, -angle)
    new_rect = rotated_image.get_rect(center=image.get_rect().center)
    return rotated_image, new_rect

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    screen.fill((255, 255, 255))  
    
    now = datetime.datetime.now()
    seconds = now.second
    minutes = now.minute
    
    sec_angle = seconds * 6
    min_angle = minutes * 6 + (seconds / 60.0) * 6
    
    rotated_sec, sec_rect = rot_center(sec_img, sec_angle)
    rotated_min, min_rect = rot_center(sec_img, min_angle)
    
    screen_center = (450, 450)
    sec_rect.center = screen_center
    min_rect.center = screen_center
    
    screen.blit(image, (0, 0))
    screen.blit(rotated_min, min_rect)
    screen.blit(rotated_sec, sec_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()