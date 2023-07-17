import pygame
import game
import about_win
import help_win
pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Like")

BG_IMAGE = pygame.transform.scale(pygame.image.load("images\\space.webp"), (WIDTH, HEIGHT))
ARROW_IMAGE = pygame.transform.scale(pygame.image.load("images\\arrow.png"), (50, 50))

TITLE_FONT = pygame.font.SysFont("Courier", 60, "bold")
PLAY_FONT = pygame.font.SysFont("Courier", 36, "bold")
ABOUT_FONT = pygame.font.SysFont("Courier", 36, "bold")
QUIT_FONT = pygame.font.SysFont("Courier", 36, "bold")
HELP_FONT = pygame.font.SysFont("Courier", 36, "bold")

PLAY_EVENT = pygame.USEREVENT + 1
ABOUT_EVENT = pygame.USEREVENT + 2
HELP_EVENT = pygame.USEREVENT + 3
QUIT_EVENT = pygame.USEREVENT + 4


def draw(title, play, about, quit_, help_, arrow):
    win.blit(BG_IMAGE, (0, 0))
    title_text = TITLE_FONT.render(title, 1, "white")
    win.blit(title_text, (WIDTH/2 - title_text.get_width()/2, HEIGHT/2 - title_text.get_height()/2 - 60))
    play_text = PLAY_FONT.render(play, 1, "white")
    win.blit(play_text, (WIDTH/2 - play_text.get_width()/2, HEIGHT/2 - play_text.get_height()/2 + 30))
    about_text = ABOUT_FONT.render(about, 1, "white")
    win.blit(about_text, (WIDTH/2 - about_text.get_width()/2, HEIGHT/2 - about_text.get_height()/2 + 90))
    help_text = HELP_FONT.render(help_, 1, "white")
    win.blit(help_text, (WIDTH/2 - help_text.get_width()/2, HEIGHT/2 - help_text.get_height()/2 + 150))
    quit_text = QUIT_FONT.render(quit_, 1, "white")
    win.blit(quit_text, (WIDTH/2 - quit_text.get_width()/2, HEIGHT/2 - quit_text.get_height()/2 + 210))
    win.blit(ARROW_IMAGE, (arrow.x, arrow.y))

    pygame.display.update()


def arrow_movement_check(keys_pressed, arrow):
    if arrow.y == HEIGHT / 2 and keys_pressed[pygame.K_SPACE]:
        pygame.event.post(pygame.event.Event(PLAY_EVENT))
    if arrow.y == HEIGHT / 2 + 60 and keys_pressed[pygame.K_SPACE]:
        pygame.event.post(pygame.event.Event(ABOUT_EVENT))
    if arrow.y == HEIGHT / 2 + 120 and keys_pressed[pygame.K_SPACE]:
        pygame.event.post(pygame.event.Event(HELP_EVENT))
    if arrow.y == HEIGHT / 2 + 180 and keys_pressed[pygame.K_SPACE]:
        pygame.event.post(pygame.event.Event(QUIT_EVENT))


def main():
    clock = pygame.time.Clock()
    run = True
    title = "SPACE INVADERS LIKE"
    play = "PLAY"
    about = "ABOUT"
    quit_ = "QUIT"
    help_ = "HELP"
    arrow = pygame.Rect(WIDTH / 2 - 150, HEIGHT/2, 20, 20)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if arrow.y == HEIGHT / 2:
                    if event.key == pygame.K_DOWN:
                        arrow.y = HEIGHT / 2 + 60
                    elif event.key == pygame.K_UP:
                        arrow.y = HEIGHT / 2 + 180
                elif arrow.y == HEIGHT / 2 + 60:
                    if event.key == pygame.K_DOWN:
                        arrow.y = HEIGHT / 2 + 120
                    elif event.key == pygame.K_UP:
                        arrow.y = HEIGHT / 2
                elif arrow.y == HEIGHT / 2 + 120:
                    if event.key == pygame.K_DOWN:
                        arrow.y = HEIGHT / 2 + 180
                    elif event.key == pygame.K_UP:
                        arrow.y = HEIGHT / 2 + 60
                elif arrow.y == HEIGHT / 2 + 180:
                    if event.key == pygame.K_DOWN:
                        arrow.y = HEIGHT / 2
                    elif event.key == pygame.K_UP:
                        arrow.y = HEIGHT / 2 + 120
        
            if event.type == PLAY_EVENT:
                with open("highscore.txt") as file:
                    game.HIGHSCORE = file.read()
                game.main()
            elif event.type == ABOUT_EVENT:
                about_win.main()
            elif event.type == HELP_EVENT:
                help_win.main()
            elif event.type == QUIT_EVENT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        arrow_movement_check(keys_pressed, arrow)
        draw(title, play, about, quit_, help_, arrow)
        
    pygame.quit()


if __name__ == "__main__":
    main()