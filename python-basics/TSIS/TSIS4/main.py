import pygame
import sys
import random
from db import Database
from config import load_settings, save_settings
from game import PowerUp, PoisonFood, Food, get_random_position, CELL_SIZE, WIDTH, HEIGHT

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        
    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.db = Database()
        self.settings = load_settings()
        
        self.state = "MENU"
        self.username = ""
        self.player_id = None
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 48)
        self.small_font = pygame.font.SysFont("Arial", 16)
        
        self.selected_color_index = 0
        self.colors = [[0, 255, 0], [255, 0, 0], [0, 0, 255], [255, 255, 0], [255, 0, 255]]
        
        self.init_buttons()
        self.reset_game()

    def init_buttons(self):
        button_width, button_height = 200, 50
        center_x = WIDTH // 2 - button_width // 2
        
        self.play_btn = Button(center_x, 200, button_width, button_height, "PLAY", GREEN, (0, 100, 0))
        self.leaderboard_btn = Button(center_x, 270, button_width, button_height, "LEADERBOARD", BLUE, (0, 0, 100))
        self.settings_btn = Button(center_x, 340, button_width, button_height, "SETTINGS", GRAY, (100, 100, 100))
        self.quit_btn = Button(center_x, 410, button_width, button_height, "QUIT", RED, (100, 0, 0))
        
        self.retry_btn = Button(center_x - 110, 400, 200, 50, "RETRY", GREEN, (0, 100, 0))
        self.main_menu_btn = Button(center_x + 110, 400, 200, 50, "MAIN MENU", BLUE, (0, 0, 100))
        
        self.back_btn = Button(WIDTH - 120, HEIGHT - 60, 100, 40, "BACK", GRAY, (100, 100, 100))
        
        self.grid_btn = Button(center_x, 250, 300, 50, "", GRAY, (100, 100, 100))
        self.sound_btn = Button(center_x, 320, 300, 50, "", GRAY, (100, 100, 100))
        self.color_btn = Button(center_x, 390, 300, 50, "", GRAY, (100, 100, 100))
        self.save_btn = Button(center_x, 460, 200, 50, "SAVE & BACK", GREEN, (0, 100, 0))
        
    def reset_game(self):
        self.snake = [[WIDTH//2, HEIGHT//2], 
                      [WIDTH//2 - CELL_SIZE, HEIGHT//2], 
                      [WIDTH//2 - 2*CELL_SIZE, HEIGHT//2]]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        self.score = 0
        self.level = 1
        self.obstacles = []
        self.food = None
        self.poison = None
        self.powerup = None
        self.active_powerup = None
        self.shield_active = False
        self.base_speed = 10
        self.current_speed = 10
        self.speed_boost_end_time = 0
        self.speed_slow_end_time = 0
        self.food_eaten = 0
        
        self.spawn_food()
        self.spawn_obstacles()
        
    def spawn_food(self):
        avoid_positions = self.snake + self.obstacles
        if self.poison:
            avoid_positions.append([self.poison.x, self.poison.y])
        if self.powerup:
            avoid_positions.append([self.powerup.x, self.powerup.y])
            
        pos = get_random_position(avoid_positions)
        
        rand = random.random()
        if rand < 0.7:
            food_type = "normal"
        elif rand < 0.9:
            food_type = "golden"
        else:
            food_type = "timer"
            
        self.food = Food(pos[0], pos[1], food_type)
        
    def spawn_obstacles(self):
        self.obstacles = []
        if self.level >= 3:
            num_obstacles = min(self.level, 15)
            for _ in range(num_obstacles):
                pos = get_random_position(self.snake + [[self.food.x, self.food.y] if self.food else []])
                self.obstacles.append(pos)
                
    def spawn_powerup(self):
        if not self.powerup and random.random() < 0.002:
            p_type = random.choice(['speed', 'slow', 'shield'])
            avoid = self.snake + self.obstacles
            if self.food:
                avoid.append([self.food.x, self.food.y])
            if self.poison:
                avoid.append([self.poison.x, self.poison.y])
            pos = get_random_position(avoid)
            self.powerup = PowerUp(p_type, pos[0], pos[1])
            
    def spawn_poison(self):
        if not self.poison and random.random() < 0.003:
            avoid = self.snake + self.obstacles
            if self.food:
                avoid.append([self.food.x, self.food.y])
            if self.powerup:
                avoid.append([self.powerup.x, self.powerup.y])
            pos = get_random_position(avoid)
            self.poison = PoisonFood(pos[0], pos[1])
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.db.close()
                pygame.quit()
                sys.exit()
                
            if self.state == "MENU":
                if self.play_btn.is_clicked(event):
                    if self.username:
                        self.player_id = self.db.get_or_create_player(self.username)
                        self.state = "PLAYING"
                        self.reset_game()
                elif self.leaderboard_btn.is_clicked(event):
                    self.state = "LEADERBOARD"
                elif self.settings_btn.is_clicked(event):
                    self.state = "SETTINGS"
                elif self.quit_btn.is_clicked(event):
                    self.db.close()
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN and self.username:
                        self.player_id = self.db.get_or_create_player(self.username)
                        self.state = "PLAYING"
                        self.reset_game()
                    else:
                        if len(self.username) < 15 and event.unicode.isprintable():
                            self.username += event.unicode
                            
            elif self.state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.next_direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.next_direction = "DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.next_direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.next_direction = "RIGHT"
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                        
            elif self.state == "GAME_OVER":
                if self.retry_btn.is_clicked(event):
                    self.reset_game()
                    self.state = "PLAYING"
                elif self.main_menu_btn.is_clicked(event):
                    self.state = "MENU"
                    
            elif self.state == "LEADERBOARD":
                if self.back_btn.is_clicked(event):
                    self.state = "MENU"
                    
            elif self.state == "SETTINGS":
                if self.grid_btn.is_clicked(event):
                    self.settings["grid_overlay"] = not self.settings["grid_overlay"]
                elif self.sound_btn.is_clicked(event):
                    self.settings["sound"] = not self.settings["sound"]
                elif self.color_btn.is_clicked(event):
                    self.selected_color_index = (self.selected_color_index + 1) % len(self.colors)
                    self.settings["snake_color"] = self.colors[self.selected_color_index]
                elif self.save_btn.is_clicked(event):
                    save_settings(self.settings)
                    self.state = "MENU"
                    
    def update_speed_effects(self):
        current_time = pygame.time.get_ticks()
        
        if self.active_powerup:
            if self.active_powerup.type == 'speed' and current_time > self.speed_boost_end_time:
                self.current_speed = self.base_speed
                self.active_powerup = None
            elif self.active_powerup.type == 'slow' and current_time > self.speed_slow_end_time:
                self.current_speed = self.base_speed
                self.active_powerup = None
                
    def update(self):
        if self.state != "PLAYING":
            return
            
        self.update_speed_effects()
        self.spawn_powerup()
        self.spawn_poison()
        
        current_time = pygame.time.get_ticks()
        
        if self.powerup and self.powerup.is_expired(current_time):
            self.powerup = None
        if self.food and self.food.is_expired(current_time):
            self.spawn_food()
        if self.poison and current_time - self.poison.spawn_time > 8000:
            self.poison = None
            
        self.direction = self.next_direction
        head = list(self.snake[0])
        
        if self.direction == "UP":
            head[1] -= CELL_SIZE
        elif self.direction == "DOWN":
            head[1] += CELL_SIZE
        elif self.direction == "LEFT":
            head[0] -= CELL_SIZE
        elif self.direction == "RIGHT":
            head[0] += CELL_SIZE
            
        if head in self.snake[1:]:
            if self.shield_active:
                self.shield_active = False
            else:
                self.game_over()
                return
                
        if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or 
            head in self.obstacles):
            if self.shield_active:
                self.shield_active = False
                return
            else:
                self.game_over()
                return
                
        if self.powerup and head == [self.powerup.x, self.powerup.y]:
            self.active_powerup = self.powerup
            self.active_powerup.is_active = True
            self.active_powerup.activation_time = current_time
            
            if self.powerup.type == 'speed':
                self.current_speed = min(25, self.base_speed + 8)
                self.speed_boost_end_time = current_time + 5000
            elif self.powerup.type == 'slow':
                self.current_speed = max(3, self.base_speed - 5)
                self.speed_slow_end_time = current_time + 5000
            elif self.powerup.type == 'shield':
                self.shield_active = True
                
            self.powerup = None
            
        if head == [self.food.x, self.food.y]:
            points = self.food.get_points()
            self.score += points
            self.food_eaten += 1
            self.snake.insert(0, head)
            
            if self.food_eaten % 5 == 0:
                self.level += 1
                self.base_speed += 1
                self.current_speed = self.base_speed
                self.spawn_obstacles()
                
            self.spawn_food()
        else:
            self.snake.insert(0, head)
            self.snake.pop()
            
        if self.poison and head == [self.poison.x, self.poison.y]:
            if len(self.snake) > 2:
                self.snake.pop()
                self.snake.pop()
                self.score = max(0, self.score - 20)
            else:
                self.game_over()
                return
            self.poison = None
            
    def game_over(self):
        if self.player_id:
            self.db.save_session(self.player_id, self.score, self.level)
        self.state = "GAME_OVER"
        
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        title = self.title_font.render("SNAKE GAME", True, GREEN)
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        name_text = self.font.render(f"Enter Name: {self.username}", True, WHITE)
        name_rect = name_text.get_rect(center=(WIDTH//2, 160))
        self.screen.blit(name_text, name_rect)
        
        self.play_btn.draw(self.screen, self.font)
        self.leaderboard_btn.draw(self.screen, self.font)
        self.settings_btn.draw(self.screen, self.font)
        self.quit_btn.draw(self.screen, self.font)
        
        inst = self.font.render("Press ENTER to start with current name", True, GRAY)
        inst_rect = inst.get_rect(center=(WIDTH//2, HEIGHT - 50))
        self.screen.blit(inst, inst_rect)
        
        # Показываем статус БД
        if not self.db.available:
            offline_text = self.small_font.render("Database offline - scores won't be saved", True, RED)
            offline_rect = offline_text.get_rect(center=(WIDTH//2, HEIGHT - 20))
            self.screen.blit(offline_text, offline_rect)
        
    def draw_game(self):
        self.screen.fill(BLACK)
        
        if self.settings.get("grid_overlay", True):
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(self.screen, DARK_GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(self.screen, DARK_GRAY, (0, y), (WIDTH, y))
                
        snake_color = tuple(self.settings.get("snake_color", [0, 255, 0]))
        for i, segment in enumerate(self.snake):
            color = CYAN if self.shield_active and i == 0 else snake_color
            pygame.draw.rect(self.screen, color, (segment[0], segment[1], CELL_SIZE-2, CELL_SIZE-2))
            
        food_colors = {'normal': GREEN, 'golden': YELLOW, 'timer': (255, 165, 0)}
        food_color = food_colors.get(self.food.type, GREEN)
        pygame.draw.rect(self.screen, food_color, (self.food.x, self.food.y, CELL_SIZE, CELL_SIZE))
        
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (obs[0], obs[1], CELL_SIZE, CELL_SIZE))
            
        if self.poison:
            pygame.draw.rect(self.screen, (139, 0, 0), (self.poison.x, self.poison.y, CELL_SIZE, CELL_SIZE))
            
        if self.powerup:
            power_colors = {'speed': CYAN, 'slow': YELLOW, 'shield': BLUE}
            color = power_colors.get(self.powerup.type, WHITE)
            pygame.draw.rect(self.screen, color, (self.powerup.x, self.powerup.y, CELL_SIZE, CELL_SIZE))
            center = (self.powerup.x + CELL_SIZE//2, self.powerup.y + CELL_SIZE//2)
            if self.powerup.type == 'speed':
                pygame.draw.polygon(self.screen, WHITE, [(center[0], center[1]-5), (center[0]+5, center[1]), (center[0], center[1]+5)])
            elif self.powerup.type == 'slow':
                pygame.draw.rect(self.screen, WHITE, (center[0]-4, center[1]-2, 8, 4))
                
        personal_best = self.db.get_personal_best(self.player_id) if self.player_id else 0
        stats = self.font.render(f"Score: {self.score}  Level: {self.level}  Best: {personal_best}", True, WHITE)
        self.screen.blit(stats, (10, 10))
        
        if self.shield_active:
            shield_text = self.font.render("SHIELD ACTIVE!", True, CYAN)
            self.screen.blit(shield_text, (WIDTH - 150, 10))
            
        food_type_text = self.font.render(f"Food: {self.food.type.upper()} (+{self.food.get_points()})", True, food_color)
        self.screen.blit(food_type_text, (10, 40))
        
        esc_text = self.font.render("ESC - Menu", True, GRAY)
        self.screen.blit(esc_text, (WIDTH - 100, HEIGHT - 30))
        
    def draw_game_over(self):
        self.screen.fill(BLACK)
        
        game_over = self.title_font.render("GAME OVER", True, RED)
        game_over_rect = game_over.get_rect(center=(WIDTH//2, 150))
        self.screen.blit(game_over, game_over_rect)
        
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH//2, 250))
        self.screen.blit(score_text, score_rect)
        
        level_text = self.font.render(f"Level Reached: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(WIDTH//2, 300))
        self.screen.blit(level_text, level_rect)
        
        personal_best = self.db.get_personal_best(self.player_id) if self.player_id else 0
        best_text = self.font.render(f"Personal Best: {personal_best}", True, YELLOW)
        best_rect = best_text.get_rect(center=(WIDTH//2, 350))
        self.screen.blit(best_text, best_rect)
        
        self.retry_btn.draw(self.screen, self.font)
        self.main_menu_btn.draw(self.screen, self.font)
        
    def draw_leaderboard(self):
        self.screen.fill(BLACK)
        
        title = self.title_font.render("TOP 10 SCORES", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        if not self.db.available:
            offline_text = self.font.render("DATABASE NOT AVAILABLE", True, RED)
            offline_rect = offline_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            self.screen.blit(offline_text, offline_rect)
            offline_text2 = self.small_font.render("Check PostgreSQL connection", True, GRAY)
            offline_rect2 = offline_text2.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.screen.blit(offline_text2, offline_rect2)
        else:
            top_scores = self.db.get_top_10()
            
            if not top_scores:
                no_data = self.font.render("No scores yet. Play the game!", True, WHITE)
                no_data_rect = no_data.get_rect(center=(WIDTH//2, HEIGHT//2))
                self.screen.blit(no_data, no_data_rect)
            else:
                headers = ["Rank", "Username", "Score", "Level", "Date"]
                for i, header in enumerate(headers):
                    text = self.font.render(header, True, YELLOW)
                    self.screen.blit(text, (100 + i*150, 100))
                    
                for idx, (username, score, level, date) in enumerate(top_scores):
                    y_pos = 150 + idx * 40
                    rank_text = self.font.render(f"#{idx + 1}", True, WHITE)
                    name_text = self.font.render(username[:15], True, WHITE)
                    score_text = self.font.render(str(score), True, GREEN)
                    level_text = self.font.render(str(level), True, CYAN)
                    date_text = self.font.render(date, True, GRAY)
                    
                    self.screen.blit(rank_text, (100, y_pos))
                    self.screen.blit(name_text, (250, y_pos))
                    self.screen.blit(score_text, (400, y_pos))
                    self.screen.blit(level_text, (550, y_pos))
                    self.screen.blit(date_text, (700, y_pos))
                
        self.back_btn.draw(self.screen, self.font)
        
    def draw_settings(self):
        self.screen.fill(BLACK)
        
        title = self.title_font.render("SETTINGS", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        grid_text = f"Grid Overlay: {'ON' if self.settings['grid_overlay'] else 'OFF'}"
        self.grid_btn.text = grid_text
        self.grid_btn.draw(self.screen, self.font)
        
        sound_text = f"Sound: {'ON' if self.settings['sound'] else 'OFF'}"
        self.sound_btn.text = sound_text
        self.sound_btn.draw(self.screen, self.font)
        
        color_names = ["Green", "Red", "Blue", "Yellow", "Purple"]
        color_text = f"Snake Color: {color_names[self.selected_color_index]}"
        self.color_btn.text = color_text
        self.color_btn.draw(self.screen, self.font)
        
        preview_rect = pygame.Rect(WIDTH//2 + 160, 405, 30, 30)
        pygame.draw.rect(self.screen, tuple(self.settings["snake_color"]), preview_rect)
        
        self.save_btn.draw(self.screen, self.font)
        
    def draw(self):
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "PLAYING":
            self.draw_game()
        elif self.state == "GAME_OVER":
            self.draw_game_over()
        elif self.state == "LEADERBOARD":
            self.draw_leaderboard()
        elif self.state == "SETTINGS":
            self.draw_settings()
            
        pygame.display.flip()
        
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            speed = self.current_speed if self.state == "PLAYING" else 60
            self.clock.tick(speed)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()