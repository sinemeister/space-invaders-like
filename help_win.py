import pygame
import start
import game
import sys
pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Like")

BG_IMAGE = pygame.transform.scale(pygame.image.load("images\\space.webp"), (WIDTH, HEIGHT))
ARROW_IMAGE = pygame.transform.scale(pygame.image.load("images\\arrow.png"), (50, 50))
ALIENS_ICON = "images\\green_alien.png"
PWUP_ICON = "images\\pwup.png"
SCORE_ICON = "images\\score.png"
HIGHSCORE_ICON = "images\\highscore.png"
SPACESHIP_ICON = "images\\spaceship.png"
LIVES_ICON = "images\\lives.png"

back = "BACK"
arrow = pygame.Rect(WIDTH / 2 - 120, HEIGHT/2 + 250, 20, 20)

HELP_TEXT = [
    ("In this game, you control a spaceship and shoot the aliens.", None),
    ("The spaceship can move within the window borders using ARROW KEYS.", None),
    ("Lasers are shot when SPACEBAR is pressed.", None),
    ("Turn back to start menu with ENTER when in HELP or ABOUT windows.", None),
    ("You can pause the game with ESC.", None),
    ("Press DEL to turn back to start menu when playing.", None),
    ("Restart the game with R.", None),
    ("Toggle HELP on/off with F1 when playing.", None),
    ("", None),
    ("Additional instructions:", None),
    ("Collect power ups to shoot mega laser beam to kill all the aliens on the screen with LCTRL or RCTRL", PWUP_ICON),
    ("Avoid collisions with aliens to stay alive", ALIENS_ICON),
    ("Collect the hearts in case you are short of lives", LIVES_ICON),
    ("You can track your score,", SCORE_ICON),
    ("and your highscore at the top left corner along your lives and power up", HIGHSCORE_ICON)
]
HELP_FONT = pygame.font.SysFont("Courier", 20, "bold")
BACK_FONT = pygame.font.SysFont("Courier", 36, "bold")

def draw(back, arrow):
    win.blit(BG_IMAGE, (0,0))
    y = 20
    for line, icon_path in HELP_TEXT:
        if icon_path:
            if icon_path != "images\\pwup.png" and icon_path != "images\\highscore.png":
                icon = pygame.transform.scale(pygame.image.load(icon_path), (30, 30))
                win.blit(icon, (20, y+20))
                text = HELP_FONT.render(line, 1, "white", None, 600)
                win.blit(text, (60, y+25))
            elif icon_path == "images\\highscore.png":
                icon = pygame.transform.scale(pygame.image.load(icon_path), (30, 30))
                win.blit(icon, (20, y+35))
                text = HELP_FONT.render(line, 1, "white", None, 600)
                win.blit(text, (60, y+25))         
            else:
                icon = pygame.transform.scale(pygame.image.load(icon_path), (30, 30))
                win.blit(icon, (20, y))
                text = HELP_FONT.render(line, 1, "white", None, 650)
                win.blit(text, (60, y))
            
            y += 40

        else:
            text = HELP_FONT.render(line, 1, "white")
            win.blit(text, (10, y))
            y += 30

    win.blit(ARROW_IMAGE, (arrow.x, arrow.y))
    back_text = BACK_FONT.render(back, 1, "white")
    win.blit(back_text, (WIDTH / 2 - back_text.get_width() / 2, HEIGHT / 2 - back_text.get_height() / 2 + 275))

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and arrow.y == HEIGHT/2 + 250:
                    start.main()

                if event.key == pygame.K_F1:
                    game.show_help = False

        draw(back, arrow)

    pygame.quit()

if __name__ == "__main__":
    main()