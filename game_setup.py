import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

ALIEN_IMAGE = pygame.image.load("images\\green_alien.png")
ALIEN = pygame.transform.scale(ALIEN_IMAGE, (50, 40))
BG_IMAGE = pygame.transform.scale(pygame.image.load("images\\space.webp"), (WIDTH, HEIGHT))
SPACESHIP_IMAGE = pygame.image.load("images\\spaceship.png")
SPACESHIP = pygame.transform.scale(SPACESHIP_IMAGE, (70, 60))
POWER_UP_IMAGE = pygame.transform.scale(pygame.image.load("images\\pwup.png"), (50, 40))
POWER_UP_BOX_IMAGE = pygame.transform.scale(pygame.image.load("images\\pwup.png"), (30, 30))
LIVES_IMAGE = pygame.transform.scale(pygame.image.load("images\\lives.png"), (50, 40))
LIVES_BOX_IMAGE = pygame.transform.scale(pygame.image.load("images\\lives.png"), (30, 30))
HIGHSCORE_IMAGE = pygame.transform.scale(pygame.image.load("images\\highscore.png"), (30, 30))
SCORE_IMAGE = pygame.transform.scale(pygame.image.load("images\\score.png"), (30, 30))

GAME_LOOP_MUSIC = pygame.mixer.Sound("sounds\\game_music.mp3")
GAME_LOOP_MUSIC.set_volume(0.5)
GAME_LOOP_MUSIC.play(loops=-1)
SHOOT_SOUND = pygame.mixer.Sound("sounds\\shoot.mp3")
ALIEN_HIT_SOUND = pygame.mixer.Sound("sounds\\alien_hit.mp3")
SPACESHIP_HIT_SOUND = pygame.mixer.Sound("sounds\\spaceship_hit.mp3")
GAME_END_SOUND = pygame.mixer.Sound("sounds\\end.mp3")
LASER_BEAM_SOUND = pygame.mixer.Sound("sounds\\laser_beam.mp3")
LIFE_SOUND = pygame.mixer.Sound("sounds\\life.mp3")
POWERUP_SOUND = pygame.mixer.Sound("sounds\\powerup.mp3")

SPACESHIP_VEL = 5
ALIEN_VEL = 2.5
MAX_ALIENS = 15
BULLET_VEL = 5
MAX_BULLETS = 7
MAX_POWER_UP = 1
LASER_BEAM_VEL = 7

SCORE_FONT = pygame.font.SysFont("Courier", 18, "bold")
GAME_OVER_FONT = pygame.font.SysFont("Courier", 60, "bold")
HI_SCORE_FONT = pygame.font.SysFont("Courier", 18, "bold")
POWER_UP_FONT = pygame.font.SysFont("Courier", 18, "bold")
LIVES_FONT = pygame.font.SysFont("Courier", 18, "bold")
HELP_FONT = pygame.font.SysFont("Courier", 18, "bold")
PAUSE_FONT = pygame.font.SysFont("Courier", 60, "bold")

SPACESHIP_HIT = pygame.USEREVENT + 1
ALIEN_HIT = pygame.USEREVENT + 2
POWERUP = pygame.USEREVENT + 3
GOT_LIVE = pygame.USEREVENT + 4

SPACESHIP_FLASH_PERIOD = 100
SPACESHIP_FLASH_DUR = 1000

with open("highscore.txt") as file:
    HIGHSCORE = file.read()