import pygame

pygame.init()
screen = pygame.display.set_mode((500, 250))
pygame.display.set_caption("Музыкальный плеер")

songs = ["Starboy.mp3", "fakeurface.mp3", "nobodybusiness.mp3", "giveituptome.mp3"]
current_song = 0
is_playing = True
try:
    pygame.mixer.music.load(songs[current_song])
    pygame.mixer.music.play(-1)
except pygame.error:
    print(f"Файл {songs[current_song]} не найден!")

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if is_playing:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                is_playing = not is_playing
            
            # N - Следующий трек
            elif event.key == pygame.K_n:
                current_song = (current_song + 1) % len(songs)
                pygame.mixer.music.load(songs[current_song])
                pygame.mixer.music.play(-1)
                is_playing = True
            
            # Q - Выход
            elif event.key == pygame.K_q:
                running = False

    screen.fill((30, 30, 30)) # Темно-серый фон
    
    text1 = font.render(f"Track: {songs[current_song]}", True, (255, 255, 255))
    screen.blit(text1, (50, 50))
    
    if is_playing:
        status = font.render(">> STATUS: PLAYING", True, (0, 255, 0))
    else:
        status = font.render("|| STATUS: PAUSED", True, (255, 215, 0))
    screen.blit(status, (50, 100))
    
    tips = small_font.render("P: Play/Pause  |  N: Next Track  |  Q: Quit", True, (150, 150, 150))
    screen.blit(tips, (50, 180))
    
    pygame.display.flip()

pygame.quit()