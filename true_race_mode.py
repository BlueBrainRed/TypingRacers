import pygame
import random
import sys

pygame.init()

# --- CONFIGURATION GÉNÉRALE ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typing Racers - Vrai Jeu de Course")

clock = pygame.time.Clock()

# --- Polices ---
FONT_BIG = pygame.font.SysFont('Consolas', 24, bold=True)
FONT_MED = pygame.font.SysFont('Consolas', 20)
FONT_SMALL = pygame.font.SysFont('Consolas', 18)

# --- Jeu ---
laps_to_win = 3
player_progress = 0
laps_completed = 0
opponents = [0, 0, 0]

words = ["moteur", "accélération", "freinage", "virage", "vitesse", "podium", "circuit", "pneu", "dérapage", "pilotage"]
current_word = random.choice(words)
typed_word = ""

# --- Cockpit ASCII Art ---
COCKPIT_ART = [
"┌─────────────────────────────────────────────────────────────────────────────────────┐",
"│ RPM ██████████░░░░░░░░░░░░░░░░░░░░░░░░░││ VITESSE: 240 km/h │",
"│                                                            │",
"│                 ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄                │",
"│                █                           █               │",
"│               █      ┌─────────────────┐     █              │",
"│              █       │                 │     █              │",
"│               █      │   [  ROUTE ]    │     █              │",
"│                █     └─────────────────┘    █               │",
"│                 █                         █                 │",
"│                  ▀▄                   ▄▀                    │",
"│                    ▀▀▄▄▄         ▄▄▄▀▀                      │",
"│                         ▀▀▀▀▀▀▀▀▀                           │",
"│                                                            │",
"│  LAP: [1/3]                       POSITION: [YOU vs AI]    │",
"└────────────────────────────────────────────────────────────┘"
]

# --- Affichage cockpit ASCII ---
def draw_cockpit(lap, position):
    y_offset = 100
    for idx, line in enumerate(cockpit_lines):
        if "[1/3]" in line:
            line = line.replace("[1/3]", f"[{current_lap}/{laps}]")
        elif "[YOU vs AI]" in line:
            line = line.replace("[YOU vs AI]", f"[Position : {position}/{len(opponents)+1}]")
        else:
            line = line
        text_surface = FONT_BIG.render(line, True, (0, 255, 0))
        screen.blit(text_surface, (50, 50 + y_offset + idx*22))

# --- Fonctions ---
def draw_ui():
    # Barre progression joueur
    pygame.draw.rect(screen, (50,50,50), [150, 750, 900, 20])
    pygame.draw.rect(screen, (0,255,0), [150, 750, 9 * player_progress, 20])

    # Adversaires
    colors = [(255,0,0), (255,255,0), (0,0,255)]
    for idx, opp in enumerate(opponents):
        pygame.draw.rect(screen, (80,80,80), [150, 720 - (idx:=30*i), 900, 15])
        pygame.draw.rect(screen, colors[i], [150, 750 - 40*(i+1), 9 * opp, 15])

    # Affichage mot
    word_surface = FONT_BIG.render(current_word, True, (255,255,255))
    screen.blit(word_surface, (SCREEN_WIDTH//2 - word_surface.get_width()//2, 400))

    typed_surface = FONT_MED.render(typed_word, True, (255,255,255))
    screen.blit(typed_surface, (SCREEN_WIDTH//2 - typed_surface.get_width()//2, 440))

# --- Mise à jour des adversaires ---
def update_opponents():
    global opponents
    opponents = [min(100, opp + random.uniform(0.1, 0.3)) for opp in opponents]

# --- Principale ---
running = True
timer = 0
laps = 3
current_lap = 1
opponents = [0, 0, 0]

while running:
    clock.tick(60)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                typed_word = typed_word[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if typed_word.strip() == current_word:
                    player_progress += 10
                    current_word = random.choice(words)
                typed_word = ""
            else:
                typed_word += event.unicode

    timer += 1
    if timer % 20 == 0:
        update_opponents()

    if player_progress >= 100:
        player_progress = 0
        current_lap += 1
        if current_lap > laps:
            print("🏆 Vous avez gagné la course ! 🏆")
            running = False

    for i in range(len(opponents)):
        if opponents[i] >= 100:
            opponents[i] = 0

    # Tri positions
    all_progress = [player_progress] + opponents
    all_progress.sort(reverse=True)
    position = all_progress.index(player_progress) + 1

    # Dessin
    screen.fill((10,10,10))
    draw_ui()

    cockpit = FONT_BIG.render("\n".join(COCKPIT_ART), True, (0,255,0))
    draw_cockpit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

