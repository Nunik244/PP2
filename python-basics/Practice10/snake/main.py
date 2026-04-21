import pygame
from clas import Snake,Food
snake = Snake()
food = Food()
WIDTH = 800
HEIGHT = 800
GRID_SIZE = 20 
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
clock = pygame.time.Clock()
move_timer = 0
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snake")
running = True
font = pygame.font.SysFont(None, 55)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake.change_direction((-GRID_SIZE, 0))
    elif keys[pygame.K_RIGHT]:
        snake.change_direction((GRID_SIZE, 0))
    elif keys[pygame.K_UP]:
        snake.change_direction((0, -GRID_SIZE))
    elif keys[pygame.K_DOWN]:
        snake.change_direction((0, GRID_SIZE))

    move_timer += 1
    if move_timer >= snake.speed:
        snake.update()
        move_timer = 0

        if snake.body[0] == (food.rect.x, food.rect.y):
            snake.score += 1
            snake.grow = True
            food.respawn()          

        if snake.check_collision():
            print(f"Game Over! Score: {snake.score}")
            running = False

    screen.fill((0, 0, 0))
    snake.draw(screen)
    screen.blit(food.image, food.rect)
    
    score_text = font.render(f"Score: {snake.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)