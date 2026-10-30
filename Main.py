
import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 900, 560
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighting Game Timing Trainer")
clock = pygame.time.Clock()
FPS = 60

# ---------- colors ----------
BG = (24, 24, 32)
PANEL = (40, 40, 56)
WHITE = (240, 240, 240)
GREY = (140, 140, 160)
GREEN = (60, 220, 90)
GREEN_DIM = (25, 70, 35)
RED = (235, 60, 60)
RED_DIM = (80, 25, 25)
YELLOW = (250, 210, 70)

# ---------- fonts ----------
font_big = pygame.font.SysFont("arial", 40, bold=True)
font_med = pygame.font.SysFont("arial", 26)
font_small = pygame.font.SysFont("arial", 18)

PRESETS = [
    "Street Fighter 6",
    "Tekken 8",
    "Guilty Gear Strive",
    "Mortal Kombat 1",
    "Skullgirls",
    "Under Night In-Birth",
]

# ---------- state ----------
preset_index = 0
game_name = PRESETS[preset_index]
typing = False

window_frames = 6      # total width of the "correct" zone, in frames
cycle_frames = 90      # frames for the marker to sweep across the bar
frame_counter = 0      # current marker position (in frames)

result = None          # None, True (green) or False (red)
offset_text = ""
hits = 0
misses = 0
streak = 0
best_streak = 0

# ---------- layout ----------
name_box = pygame.Rect(150, 80, 600, 50)
bar = pygame.Rect(100, 300, 700, 40)


def draw_text(text, font, color, center=None, topleft=None):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = center
    if topleft:
        rect.topleft = topleft
    screen.blit(surf, rect)


def draw_ball(center, color, dim_color, lit):
    if lit:
        pygame.draw.circle(screen, color, center, 62)          # glow ring
        pygame.draw.circle(screen, WHITE, center, 54)
        pygame.draw.circle(screen, color, center, 50)
    else:
        pygame.draw.circle(screen, dim_color, center, 50)
        pygame.draw.circle(screen, GREY, center, 50, 2)


def attempt_input():
    """Called when SPACE is pressed. Judge timing against the center of the bar."""
    global result, offset_text, hits, misses, streak, best_streak
    center_frame = cycle_frames / 2
    offset = frame_counter - center_frame        # negative = early, positive = late
    good = abs(offset) <= window_frames / 2

    result = good
    if offset == 0:
        offset_text = "Perfect! (0 frames)"
    elif offset < 0:
        offset_text = f"{abs(int(offset))} frames EARLY"
    else:
        offset_text = f"{int(offset)} frames LATE"

    if good:
        hits += 1
        streak += 1
        best_streak = max(best_streak, streak)
    else:
        misses += 1
        streak = 0


def reset_score():
    global hits, misses, streak, best_streak, result, offset_text
    hits = misses = streak = best_streak = 0
    result = None
    offset_text = ""


def set_preset(new_index):
    global preset_index, game_name
    preset_index = new_index % len(PRESETS)
    game_name = PRESETS[preset_index]


# ---------- main loop ----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            typing = name_box.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN:
            if typing:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    game_name = game_name[:-1]
                elif event.unicode and event.unicode.isprintable() and len(game_name) < 32:
                    game_name += event.unicode
            else:
                if event.key == pygame.K_SPACE:
                    attempt_input()
                elif event.key == pygame.K_LEFT:
                    set_preset(preset_index - 1)
                elif event.key == pygame.K_RIGHT:
                    set_preset(preset_index + 1)
                elif event.key == pygame.K_UP:
                    window_frames = min(30, window_frames + 1)
                elif event.key == pygame.K_DOWN:
                    window_frames = max(1, window_frames - 1)
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    cycle_frames = min(240, cycle_frames + 10)
                    frame_counter = 0
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    cycle_frames = max(30, cycle_frames - 10)
                    frame_counter = 0
                elif event.key == pygame.K_r:
                    reset_score()
                elif event.key == pygame.K_ESCAPE:
                    running = False

    # advance the marker one frame per tick
    frame_counter += 1
    if frame_counter >= cycle_frames:
        frame_counter = 0

    # ---------- draw ----------
    screen.fill(BG)

    draw_text("TIMING TRAINER", font_big, WHITE, center=(WIDTH // 2, 35))

    # game name box
    draw_text("Inputs for which fighting game?", font_small, GREY, topleft=(name_box.x, name_box.y - 24))
    pygame.draw.rect(screen, PANEL, name_box, border_radius=8)
    pygame.draw.rect(screen, YELLOW if typing else GREY, name_box, 2, border_radius=8)
    cursor = "|" if typing and (pygame.time.get_ticks() // 500) % 2 == 0 else ""
    draw_text(game_name + cursor, font_med, WHITE, topleft=(name_box.x + 15, name_box.y + 11))
    draw_text("(click to type, or use LEFT/RIGHT for presets)", font_small, GREY,
              center=(WIDTH // 2, name_box.bottom + 18))

    # balls
    draw_ball((330, 200), GREEN, GREEN_DIM, result is True)
    draw_ball((570, 200), RED, RED_DIM, result is False)
    draw_text("RIGHT", font_small, GREEN, center=(330, 275))
    draw_text("WRONG", font_small, RED, center=(570, 275))

    # timing bar
    pygame.draw.rect(screen, PANEL, bar, border_radius=6)
    zone_w = bar.w * window_frames / cycle_frames
    zone = pygame.Rect(0, bar.y, zone_w, bar.h)
    zone.centerx = bar.centerx
    pygame.draw.rect(screen, GREEN_DIM, zone)
    pygame.draw.rect(screen, GREEN, zone, 2)
    marker_x = bar.x + bar.w * frame_counter / cycle_frames
    pygame.draw.line(screen, WHITE, (marker_x, bar.y - 10), (marker_x, bar.bottom + 10), 4)
    pygame.draw.rect(screen, GREY, bar, 2, border_radius=6)

    # feedback text
    if offset_text:
        color = GREEN if result else RED
        draw_text(offset_text, font_med, color, center=(WIDTH // 2, 380))

    # stats
    total = hits + misses
    accuracy = (hits / total * 100) if total else 0
    draw_text(f"Hits: {hits}    Misses: {misses}    Accuracy: {accuracy:.0f}%",
              font_med, WHITE, center=(WIDTH // 2, 430))
    draw_text(f"Streak: {streak}    Best streak: {best_streak}",
              font_med, YELLOW, center=(WIDTH // 2, 465))

    # settings / help
    ms = window_frames * 1000 / 60
    draw_text(f"Window: {window_frames} frames (~{ms:.0f} ms)   |   Sweep: {cycle_frames} frames",
              font_small, GREY, center=(WIDTH // 2, 510))
    draw_text("SPACE = input   UP/DOWN = window   +/- = speed   R = reset",
              font_small, GREY, center=(WIDTH // 2, 535))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
