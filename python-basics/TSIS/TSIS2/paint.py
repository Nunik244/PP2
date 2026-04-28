import pygame
import datetime
import tools

pygame.init()

WIDTH, HEIGHT = 1200, 700
CANVAS_WIDTH = 1000

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

canvas = pygame.Surface((CANVAS_WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

color = (0, 0, 0)
tool = "pencil"
brush_size = 2

drawing = False
start_pos = None
last_pos = None

# TEXT
font = pygame.font.SysFont(None, 28)
text_active = False
text_input = ""
text_pos = (0, 0)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((200, 200, 200))

    # --- DRAW CANVAS ---
    screen.blit(canvas, (0, 0))

    # --- RIGHT PANEL ---
    panel_rect = pygame.Rect(CANVAS_WIDTH, 0, WIDTH - CANVAS_WIDTH, HEIGHT)
    pygame.draw.rect(screen, (240, 240, 240), panel_rect)

    # --- NOTES TEXT ---
    notes = [
        "TOOLS:",
        "P - Pencil",
        "L - Line",
        "R - Rectangle",
        "C - Circle",
        "F - Fill",
        "T - Text",
        "",
        "BRUSH:",
        "1 - Small",
        "2 - Medium",
        "3 - Large",
        "",
        "SAVE:",
        "Ctrl + S"
    ]

    y_offset = 20
    for line in notes:
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (CANVAS_WIDTH + 10, y_offset))
        y_offset += 28

    # --- CURRENT TOOL ---
    current_tool_text = font.render(f"Current: {tool}", True, (200, 0, 0))
    screen.blit(current_tool_text, (CANVAS_WIDTH + 10, HEIGHT - 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---------------- MOUSE DOWN ----------------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] < CANVAS_WIDTH:  # только в canvas

                if tool == "pencil":
                    drawing = True
                    last_pos = event.pos

                elif tool in ["line", "rect", "circle"]:
                    drawing = True
                    start_pos = event.pos

                elif tool == "fill":
                    tools.flood_fill(canvas, *event.pos, color)

                elif tool == "text":
                    text_active = True
                    text_input = ""
                    text_pos = event.pos

        # ---------------- MOUSE UP ----------------
        elif event.type == pygame.MOUSEBUTTONUP:
            if tool == "pencil":
                drawing = False

            elif tool == "line" and drawing:
                tools.draw_line(canvas, color, start_pos, event.pos, brush_size)
                drawing = False

            elif tool == "rect" and drawing:
                tools.draw_rect(canvas, color, start_pos, event.pos, brush_size)
                drawing = False

            elif tool == "circle" and drawing:
                tools.draw_circle(canvas, color, start_pos, event.pos, brush_size)
                drawing = False

        # ---------------- MOUSE MOVE ----------------
        elif event.type == pygame.MOUSEMOTION:
            if drawing and tool == "pencil":
                tools.draw_pencil(canvas, color, last_pos, event.pos, brush_size)
                last_pos = event.pos

        # ---------------- KEYBOARD ----------------
        elif event.type == pygame.KEYDOWN:

            # TOOL SWITCH
            if event.key == pygame.K_p:
                tool = "pencil"
            elif event.key == pygame.K_l:
                tool = "line"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_f:
                tool = "fill"
            elif event.key == pygame.K_t:
                tool = "text"

            # BRUSH SIZE
            elif event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10

            # SAVE
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)
                print("Saved:", filename)

            # TEXT INPUT
            if text_active:
                if event.key == pygame.K_RETURN:
                    text_surface = font.render(text_input, True, color)
                    canvas.blit(text_surface, text_pos)
                    text_active = False

                elif event.key == pygame.K_ESCAPE:
                    text_active = False

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

    # -------- PREVIEW --------
    if drawing:
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] < CANVAS_WIDTH:

            if tool == "line":
                tools.draw_line(screen, color, start_pos, mouse_pos, brush_size)

            elif tool == "rect":
                tools.draw_rect(screen, color, start_pos, mouse_pos, brush_size)

            elif tool == "circle":
                tools.draw_circle(screen, color, start_pos, mouse_pos, brush_size)

    # -------- TEXT PREVIEW --------
    if text_active:
        text_surface = font.render(text_input, True, color)
        screen.blit(text_surface, text_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()