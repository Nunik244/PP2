import pygame
import random
import os
import sys
from car import Car,Road,Coin
WIDTH = 800
HEIGHT = 800
FPS = 60
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Игра с машиной и монетами")
    clock = pygame.time.Clock()

    # Создаём объекты
    car = Car()
    road = Road()

    # Группы спрайтов
    all_sprites = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    all_sprites.add(car)

    score = 0
    font = pygame.font.SysFont(None, 55)

    coin_timer = 0

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        car.update()
        coins.update()
        road.update()

        coin_timer += 1
        if coin_timer >= 35:
            new_coin = Coin()
            all_sprites.add(new_coin)
            coins.add(new_coin)
            coin_timer = 0

        collected = pygame.sprite.spritecollide(car, coins, True)
        score += len(collected)

        road.draw(screen)
        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (25, 25))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()