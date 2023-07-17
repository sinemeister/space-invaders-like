import pygame
import start
pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Like")

BG_IMAGE = pygame.transform.scale(pygame.image.load("images\\space.webp"), (WIDTH, HEIGHT))
ARROW_IMAGE = pygame.transform.scale(pygame.image.load("images\\arrow.png"), (50, 50))

ABOUT_TEXT = "DEVELOPED BY SINEMEISTER"
ABOUT_TEXT_2 = "JULY 2023"
ABOUT_FONT = pygame.font.SysFont("Courier", 48, "bold")
BACK_FONT = pygame.font.SysFont("Courier", 36, "bold")


def draw(back, arrow):
    win.blit(BG_IMAGE, (0,0))
    about_text = ABOUT_FONT.render(ABOUT_TEXT, 1, "white", None, 750)
    win.blit(about_text, (WIDTH / 2 - about_text.get_width() / 2, HEIGHT / 2 - about_text.get_height() / 2 - 120))
    about_text_2 = ABOUT_FONT.render(ABOUT_TEXT_2, 1, "white")
    win.blit(about_text_2, (WIDTH / 2 - about_text_2.get_width() / 2, HEIGHT / 2 - about_text_2.get_height() / 2 - 30))
    win.blit(ARROW_IMAGE, (arrow.x, arrow.y))
    back_text = BACK_FONT.render(back, 1, "white")
    win.blit(back_text, (WIDTH / 2 - back_text.get_width() / 2, HEIGHT / 2 - back_text.get_height() / 2 + 150))

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    back = "BACK"
    arrow = pygame.Rect(WIDTH / 2 - 120, HEIGHT/2 + 125, 20, 20)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and arrow.y == HEIGHT/2 + 125:
                    start.main()

        draw(back, arrow)

    pygame.quit()

if __name__ == "__main__":
    main()