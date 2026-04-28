import pygame
import sys
import random
import persistence as db
from ui import *
from racer import Player, Enemy, PowerUp, Hazard, Coin

pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Racer")
CLOCK = pygame.time.Clock()

class Game:
    def __init__(self):
        self.settings = db.get_settings()
        self.state = "MENU"
        self.username = "Player1"
        self.reset_game()

    def reset_game(self):
        """Сброс всех игровых переменных для новой игры"""
        self.score = 0
        self.coins_count = 0
        self.distance = 0
        # Скорость зависит от настроек
        base_speed = {"Easy": 3, "Medium": 5, "Hard": 8}
        self.game_speed = base_speed.get(self.settings.get('difficulty'), 5)
        
        self.player = Player(self.settings['car_color'])
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        self.active_powerup = None
        self.powerup_timer = 0
        self.shield_timer = 0  # Таймер для щита

    def run(self):
        """Главный игровой цикл"""
        while True:
            if self.state == "MENU":
                self.main_menu()
            elif self.state == "GAME":
                self.play_game()
            elif self.state == "LEADERBOARD":
                self.show_leaderboard()
            elif self.state == "GAME_OVER":
                self.game_over_screen()

    def main_menu(self):
        """Главное меню"""
        SCREEN.fill(WHITE)
        draw_text(SCREEN, "STREET RACER", 40, SCREEN_WIDTH//2, 100, RED, True)
        
        btn_play = Button("PLAY", 125, 200, 150, 50, GREEN)
        btn_lead = Button("SCORES", 125, 270, 150, 50, GRAY)
        btn_quit = Button("QUIT", 125, 340, 150, 50, BLACK)
        
        # Поле ввода имени
        draw_text(SCREEN, f"Name: {self.username}", 20, SCREEN_WIDTH//2, 180, BLACK, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    if len(self.username) < 15 and event.unicode.isprintable():
                        self.username += event.unicode
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_play.is_clicked(pos): 
                    self.reset_game()
                    self.state = "GAME"
                if btn_lead.is_clicked(pos): 
                    self.state = "LEADERBOARD"
                if btn_quit.is_clicked(pos): 
                    pygame.quit()
                    sys.exit()

        for b in [btn_play, btn_lead, btn_quit]: 
            b.draw(SCREEN, pygame.font.SysFont("Verdana", 20))
        pygame.display.update()

    def play_game(self):
        """Основной игровой процесс"""
        SCREEN.fill(WHITE)
        
        # Обновление очков: Дистанция + Бонусы за монеты
        self.distance += 0.1
        self.score = int(self.distance) + (self.coins_count * 100)
        self.game_speed += 0.001 
        
        # Обновление таймера щита
        if self.player.shielded:
            current_time = pygame.time.get_ticks()
            if current_time - self.shield_timer > 5000:  # Щит на 5 секунд
                self.player.shielded = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Спавн врагов
        if random.randint(1, 60) == 1 and len(self.enemies) < 4:
            e = Enemy(self.game_speed)
            self.enemies.add(e)
            self.all_sprites.add(e)
        
        # Спавн монет
        if random.randint(1, 120) == 1:
            c = Coin()
            self.coins.add(c)
            self.all_sprites.add(c)

        # Спавн бонусов
        if random.randint(1, 300) == 1:
            p = PowerUp(random.choice(['Nitro', 'Shield']))
            self.powerups.add(p)
            self.all_sprites.add(p)

        # Обновление позиций
        self.player.move()
        self.enemies.update()
        self.coins.update()
        self.powerups.update()

        # Проверка сбора монет
        coins_collected = pygame.sprite.spritecollide(self.player, self.coins, True)
        if coins_collected:
            self.coins_count += len(coins_collected)

        # Проверка сбора бонусов
        powerups_collected = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for p in powerups_collected:
            if p.type == 'Nitro':
                self.game_speed += 3  # Временное ускорение
            elif p.type == 'Shield':
                self.player.shielded = True
                self.shield_timer = pygame.time.get_ticks()

        # Проверка столкновений с врагами
        enemies_hit = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemies_hit:
            if self.player.shielded:
                self.player.shielded = False
                # Уничтожаем всех врагов, с которыми столкнулись
                for e in enemies_hit:
                    e.kill()
            else:
                # Сохраняем результат и завершаем игру
                db.save_score(self.username, self.score, int(self.distance))
                self.state = "GAME_OVER"
                return

        # Отрисовка
        for entity in self.all_sprites:
            SCREEN.blit(entity.image, entity.rect)
        
        # Отображение UI
        draw_text(SCREEN, f"SCORE: {self.score}", 20, 10, 10, BLACK)
        draw_text(SCREEN, f"COINS: {self.coins_count}", 18, 10, 40, (180, 150, 0))
        draw_text(SCREEN, f"SPEED: {int(self.game_speed)}", 18, 10, 70, BLACK)
        
        if self.player.shielded:
            draw_text(SCREEN, "SHIELD ACTIVE!", 18, SCREEN_WIDTH//2, 20, (0, 255, 255), True)
        
        pygame.display.update()
        CLOCK.tick(FPS)

    def game_over_screen(self):
        """Экран окончания игры"""
        SCREEN.fill(RED)
        draw_text(SCREEN, "CRASHED!", 40, SCREEN_WIDTH//2, 150, WHITE, True)
        draw_text(SCREEN, f"Final Score: {self.score}", 25, SCREEN_WIDTH//2, 220, WHITE, True)
        draw_text(SCREEN, f"Coins Collected: {self.coins_count}", 20, SCREEN_WIDTH//2, 260, WHITE, True)
        draw_text(SCREEN, f"Distance: {int(self.distance)}m", 20, SCREEN_WIDTH//2, 300, WHITE, True)
        
        btn_retry = Button("RETRY", 125, 350, 150, 50, BLACK)
        btn_menu = Button("MENU", 125, 420, 150, 50, GRAY)
        
        # Добавляем кнопку для просмотра рекордов
        btn_scores = Button("SCORES", 125, 490, 150, 50, (100, 100, 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_retry.is_clicked(pos): 
                    self.reset_game()
                    self.state = "GAME"
                if btn_menu.is_clicked(pos): 
                    self.state = "MENU"
                if btn_scores.is_clicked(pos):
                    self.state = "LEADERBOARD"

        btn_retry.draw(SCREEN, pygame.font.SysFont("Verdana", 18))
        btn_menu.draw(SCREEN, pygame.font.SysFont("Verdana", 18))
        btn_scores.draw(SCREEN, pygame.font.SysFont("Verdana", 18))
        pygame.display.update()

    def show_leaderboard(self):
        """Таблица лидеров"""
        SCREEN.fill(WHITE)
        draw_text(SCREEN, "TOP SCORES", 30, SCREEN_WIDTH//2, 50, BLACK, True)
        
        scores = db.get_leaderboard()
        
        if not scores:
            draw_text(SCREEN, "No scores yet!", 20, SCREEN_WIDTH//2, 150, GRAY, True)
        else:
            # Заголовки таблицы
            draw_text(SCREEN, "Rank", 18, 50, 100, BLACK)
            draw_text(SCREEN, "Name", 18, 150, 100, BLACK)
            draw_text(SCREEN, "Score", 18, 250, 100, BLACK)
            draw_text(SCREEN, "Distance", 18, 330, 100, BLACK)
            
            for i, entry in enumerate(scores[:8]):  # Показываем топ-8
                y_pos = 150 + i * 35
                draw_text(SCREEN, f"{i+1}", 18, 50, y_pos, BLACK)
                draw_text(SCREEN, entry['name'][:10], 18, 150, y_pos, BLACK)
                draw_text(SCREEN, str(entry['score']), 18, 250, y_pos, BLACK)
                draw_text(SCREEN, str(entry.get('distance', 0)), 18, 330, y_pos, BLACK)
        
        btn_back = Button("BACK", 125, 500, 150, 50, BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.is_clicked(pygame.mouse.get_pos()):
                    self.state = "MENU"
        
        btn_back.draw(SCREEN, pygame.font.SysFont("Verdana", 18))
        pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()