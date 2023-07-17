import pygame
import random
import start
import help_win
pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Like")

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

def draw_game(spaceship, aliens, bullets, score, lives_count, HIGHSCORE, powerups, powerup_count, laser_beam, lives,
              spaceship_hit, hit_start_time):
    win.blit(BG_IMAGE, (0, 0))
    if spaceship_hit:
        elapsed_time = pygame.time.get_ticks() - hit_start_time
        if elapsed_time % SPACESHIP_FLASH_PERIOD < SPACESHIP_FLASH_PERIOD / 2:
            win.blit(SPACESHIP, (spaceship.x, spaceship.y))
        if elapsed_time > SPACESHIP_FLASH_DUR:
            spaceship_hit = False
    else:
        win.blit(SPACESHIP, (spaceship.x, spaceship.y))
    for alien in aliens:
            win.blit(ALIEN, (alien.x, alien.y))
    for bullet in bullets:
        pygame.draw.rect(win, (230, 30, 100), bullet)
    lives_text = LIVES_FONT.render(f"{lives_count}", 1, (255, 255, 255))
    win.blit(LIVES_BOX_IMAGE, (10, 20 + POWER_UP_BOX_IMAGE.get_height()))
    win.blit(lives_text, (15 + POWER_UP_BOX_IMAGE.get_width(), 25 + LIVES_BOX_IMAGE.get_height()))
    win.blit(HIGHSCORE_IMAGE, (10, 30 + LIVES_BOX_IMAGE.get_height() + POWER_UP_BOX_IMAGE.get_height()))
    hi_score_text = HI_SCORE_FONT.render(f"{HIGHSCORE}", 1, (255, 255, 255))
    win.blit(hi_score_text, (15 + HIGHSCORE_IMAGE.get_width(), 35 + LIVES_BOX_IMAGE.get_height() + POWER_UP_BOX_IMAGE.get_height()))
    win.blit(SCORE_IMAGE, (10, 40 + LIVES_BOX_IMAGE.get_height() + POWER_UP_BOX_IMAGE.get_height() + HIGHSCORE_IMAGE.get_height()))
    score_text = SCORE_FONT.render(f"{score}", 1, (255, 255, 255))
    win.blit(score_text, (15 + SCORE_IMAGE.get_width(), 
                          45 + LIVES_BOX_IMAGE.get_height() + POWER_UP_BOX_IMAGE.get_height() + HIGHSCORE_IMAGE.get_height()))
    help_text = HELP_FONT.render("F1 HELP", 1, (255, 255, 255))
    win.blit(help_text, (WIDTH - help_text.get_width() - 10, 15))
    for pwup in powerups:
        win.blit(POWER_UP_IMAGE, (pwup.x, pwup.y))
    powerup_text = POWER_UP_FONT.render(f"{powerup_count}", 1, (255, 255, 255))
    win.blit(POWER_UP_BOX_IMAGE, (10, 10))
    win.blit(powerup_text, (15 + POWER_UP_BOX_IMAGE.get_width(), 15))
    pygame.draw.rect(win, (230, 30, 100), laser_beam)
    for life in lives:
        win.blit(LIVES_IMAGE, (life.x, life.y))
    del_text = HELP_FONT.render("DEL MENU", 1, (255, 255, 255))
    win.blit(del_text, (WIDTH - del_text.get_width() - 10, help_text.get_height() + 20))
    
    pygame.display.update()

    return spaceship_hit

def spaceship_handle_movement(keys_pressed, spaceship, aliens, powerups, lives, spaceship_hit):
    if keys_pressed[pygame.K_LEFT] and spaceship.x - SPACESHIP_VEL > 0:
        spaceship.x -= SPACESHIP_VEL
    if keys_pressed[pygame.K_RIGHT] and spaceship.x + SPACESHIP_VEL + spaceship.width < WIDTH:
        spaceship.x += SPACESHIP_VEL
    if keys_pressed[pygame.K_UP] and spaceship.y - SPACESHIP_VEL - spaceship.height > 0:
        spaceship.y -= SPACESHIP_VEL
    if keys_pressed[pygame.K_DOWN] and spaceship.y + SPACESHIP_VEL + spaceship.height < HEIGHT:
        spaceship.y += SPACESHIP_VEL

    for alien in aliens:
        if spaceship.colliderect(alien) and not spaceship_hit:
            aliens.remove(alien)
            pygame.event.post(pygame.event.Event(SPACESHIP_HIT))
            SPACESHIP_HIT_SOUND.play()
    
    for pwup in powerups:
        if spaceship.colliderect(pwup):
            pygame.event.post(pygame.event.Event(POWERUP))
            pwup.x = 5000
            pwup.y = 5000
            POWERUP_SOUND.play()

    for life in lives:
        if spaceship.colliderect(life):
            pygame.event.post(pygame.event.Event(GOT_LIVE))
            lives.remove(life)
            LIFE_SOUND.play()


def bullets_handle_movement(bullets, aliens):
    for bullet in bullets:
        bullet.y -= BULLET_VEL
        if bullet.y <= 0:
            bullets.remove(bullet)
    
    for bullet in bullets:
        for alien in aliens:
            if bullet.colliderect(alien) and alien.y > 0:
                pygame.event.post(pygame.event.Event(ALIEN_HIT))
                try:
                    bullets.remove(bullet)
                    aliens.remove(alien)
                except ValueError:
                    pass
                ALIEN_HIT_SOUND.set_volume(0.3)
                ALIEN_HIT_SOUND.play()


def aliens_movement(aliens):
    for alien in aliens:
        alien.y += ALIEN_VEL
        if alien.y + alien.height >= HEIGHT:
            aliens.remove(alien)


def generate_lives(lives):
    if len(lives) < 1:
        life = pygame.Rect(random.randint(0, WIDTH - LIVES_IMAGE.get_width()), random.randint(-6500, -6000),
                           LIVES_IMAGE.get_width(), LIVES_IMAGE.get_height())
        lives.append(life)

        return lives
    

def lives_movement(lives):
    for life in lives:
        life.y += 7

    if life.y >= 2000:
        lives.remove(life)

    return lives


def generate_power_up(powerups):
    if len(powerups) < MAX_POWER_UP:
        pwup = pygame.Rect(random.randint(0, WIDTH - POWER_UP_IMAGE.get_width()), random.randint(-5000, -4800),
                           POWER_UP_IMAGE.get_width(), POWER_UP_IMAGE.get_height())
        powerups.append(pwup)
        
    return powerups


def power_up_movement(powerups, powerup_count):
    for pwup in powerups:
        pwup.y += 5
    
    if pwup.y >= 2000 and powerup_count == 0:
        powerups.remove(pwup)

    return powerups


def power_up_use(keys_pressed, powerups, powerup_count, aliens, score, spaceship, laser_beam):
    if keys_pressed[pygame.K_LCTRL] and powerup_count > 0 or keys_pressed[pygame.K_RCTRL] and powerup_count > 0:
        for alien in aliens[:]:
            aliens.remove(alien)
            score += 1
        
        for pwup in powerups:
            powerups.remove(pwup)

        LASER_BEAM_SOUND.set_volume(0.5)
        LASER_BEAM_SOUND.play()

        laser_beam = pygame.Rect(spaceship.x + spaceship.width/2 - 10, 0, 20, spaceship.y)
        powerup_count = 0

    return powerups, powerup_count, aliens, score, laser_beam


def generate_aliens(aliens):
    if len(aliens) <= 10:
        for _ in range(MAX_ALIENS):
            alien = pygame.Rect(random.randint(0, WIDTH - ALIEN.get_width()), random.randint(-500, -10), 
                                ALIEN.get_width(), ALIEN.get_height())
            aliens.append(alien)

    return aliens


def game_over(game_over_text):
    start.GAME_LOOP_MUSIC.stop()
    GAME_END_SOUND.play()
    text = GAME_OVER_FONT.render(game_over_text, 1, (255, 255, 255))
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3500)


def pause(paused_text):
    text = PAUSE_FONT.render(paused_text, 1, (255, 255, 255))
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    spaceship = pygame.Rect(WIDTH / 2 - SPACESHIP.get_width() / 2, HEIGHT - SPACESHIP.get_height() - 10, 
                            SPACESHIP.get_width(), SPACESHIP.get_height())
    aliens = []
    bullets = []
    powerups = []
    powerup_count = len(powerups)
    score = 0
    lives = []
    lives_count = 5
    laser_beam = pygame.Rect(1500, 1500, 10, 100)
    paused = False
    show_help = False
    spaceship_hit = False
    hit_start_time = 0

    while run:
        clock.tick(60)

        game_over_text = ""
        if lives_count == 0:
            game_over_text = "GAME OVER"
            if score > int(HIGHSCORE):
                with open("highscore.txt", mode="w") as file:
                    file.write(str(score))
            game_over(game_over_text)
            start.main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score > int(HIGHSCORE):
                    with open("highscore.txt", mode="w") as file:
                        file.write(str(score))
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(spaceship.x + spaceship.width/2 - 2.5, spaceship.y + 10, 5, 25)
                    bullets.append(bullet)
                    SHOOT_SOUND.set_volume(0.3)
                    SHOOT_SOUND.play()      

                paused_text = ""
                if event.key == pygame.K_ESCAPE:
                    if not paused:
                        paused = True
                        paused_text = "PAUSED"
                        SHOOT_SOUND.stop()
                        pause(paused_text)
                    elif paused:
                        paused = False
                
                if event.key == pygame.K_F1 and not show_help:
                    show_help = True
                    if show_help:
                        help_win.draw(back="", arrow=pygame.Rect(1000, 1000, 1, 1))
                elif event.key == pygame.K_F1 and show_help:
                    show_help = False

                if event.key == pygame.K_DELETE:
                    if score > int(HIGHSCORE):
                        with open("highscore.txt", "w") as file:
                            file.write(str(score))
                    start.main()

                if event.key == pygame.K_r:
                    main()

            if event.type == SPACESHIP_HIT:
                lives_count -= 1
                spaceship_hit = True
                hit_start_time = pygame.time.get_ticks()
            
            if event.type == ALIEN_HIT:
                score += 1

            if event.type == POWERUP:
                powerup_count += 1

            if event.type == GOT_LIVE and lives_count < 5:
                lives_count += 1

        keys_pressed = pygame.key.get_pressed()
        
        if not paused and not show_help:
            generate_aliens(aliens)
            generate_lives(lives)
            lives_movement(lives)
            generate_power_up(powerups)
            power_up_movement(powerups, powerup_count)
            powerups, powerup_count, aliens, score, laser_beam = power_up_use(keys_pressed, powerups, powerup_count, aliens, 
                                                                              score, spaceship, laser_beam)
            bullets_handle_movement(bullets, aliens)
            aliens_movement(aliens)
            spaceship_handle_movement(keys_pressed, spaceship, aliens, powerups, lives, spaceship_hit)

            if laser_beam.y + laser_beam.height >= 0:
                laser_beam.y -= LASER_BEAM_VEL

            spaceship_hit = draw_game(spaceship, aliens, bullets, score, lives_count, HIGHSCORE, powerups, powerup_count, 
                            laser_beam, lives, spaceship_hit, hit_start_time)

    pygame.quit()

if __name__ == "__main__":
    main()