import pygame
import random
import start
import help_win
from game_setup import *
pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Like")

class Spaceship:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH / 2 - SPACESHIP.get_width() / 2, HEIGHT - SPACESHIP.get_height() - 10, 
                                SPACESHIP.get_width(), SPACESHIP.get_height())
        self.spaceship_hit = False

    def move(self, keys_pressed, aliens, features, muted):
        if keys_pressed[pygame.K_LEFT] and self.rect.x - SPACESHIP_VEL > 0:
            self.rect.x -= SPACESHIP_VEL
        if keys_pressed[pygame.K_RIGHT] and self.rect.x + SPACESHIP_VEL + self.rect.width < WIDTH:
            self.rect.x += SPACESHIP_VEL
        if keys_pressed[pygame.K_UP] and self.rect.y - SPACESHIP_VEL - self.rect.height > 0:
            self.rect.y -= SPACESHIP_VEL
        if keys_pressed[pygame.K_DOWN] and self.rect.y + SPACESHIP_VEL + self.rect.height < HEIGHT:
            self.rect.y += SPACESHIP_VEL

        for alien in aliens.aliens:
            if self.rect.colliderect(alien) and not self.spaceship_hit:
                aliens.aliens.remove(alien)
                pygame.event.post(pygame.event.Event(SPACESHIP_HIT))
                if not muted:
                    SPACESHIP_HIT_SOUND.play()
    
        for pwup in features.powerups:
            if self.rect.colliderect(pwup):
                pygame.event.post(pygame.event.Event(POWERUP))
                pwup.x = 5000
                pwup.y = 5000
                if not muted:
                    POWERUP_SOUND.play()

        for life in features.lives:
            if self.rect.colliderect(life):
                pygame.event.post(pygame.event.Event(GOT_LIVE))
                features.lives.remove(life)
                if not muted:
                 LIFE_SOUND.play()


class Aliens:
    def __init__(self):
        self.aliens = []

    def generate(self):
        if len(self.aliens) <= 10:
            for _ in range(MAX_ALIENS):
                alien = pygame.Rect(random.randint(0, WIDTH - ALIEN.get_width()), random.randint(-500, -10), 
                                    ALIEN.get_width(), ALIEN.get_height())
                self.aliens.append(alien)

        return self.aliens
    
    def move(self):
        for alien in self.aliens:
            alien.y += ALIEN_VEL
            if alien.y + alien.height >= HEIGHT:
                self.aliens.remove(alien)


class Bullets:
    def __init__(self):
        self.bullets = []
        self.laser_beam = pygame.Rect(1500, 1500, 10, 100)

    def generate(self, spaceship, muted):
        bullet = pygame.Rect(spaceship.rect.x + spaceship.rect.width/2 - 2.5, spaceship.rect.y - 25, 5, 25)
        self.bullets.append(bullet)
        if not muted:
            SHOOT_SOUND.set_volume(0.3)
            SHOOT_SOUND.play()

    def move(self, aliens, muted):
        for bullet in self.bullets:
            bullet.y -= BULLET_VEL
            if bullet.y <= 0:
                self.bullets.remove(bullet)

        for bullet in self.bullets:
            for alien in aliens.aliens:
                if bullet.colliderect(alien) and alien.y > 0:
                    pygame.event.post(pygame.event.Event(ALIEN_HIT))
                    try:
                        self.bullets.remove(bullet)
                        aliens.aliens.remove(alien)
                    except ValueError:
                        pass
                    if not muted:
                        ALIEN_HIT_SOUND.set_volume(0.3)
                        ALIEN_HIT_SOUND.play()

    def move_laser_beam(self):
        if self.laser_beam.y + self.laser_beam.height >= 0:
            self.laser_beam.y -= LASER_BEAM_VEL
        
        return self.laser_beam


class GameFeatures:
    def __init__(self):
        self.lives = []
        self.lives_count = 5
        self.powerups = []
        self.powerup_count = len(self.powerups)
        self.score = 0

    def generate_lives(self):
        if len(self.lives) < 1:
            life = pygame.Rect(random.randint(0, WIDTH - LIVES_IMAGE.get_width()), random.randint(-6500, -6000),
                               LIVES_IMAGE.get_width(), LIVES_IMAGE.get_height())
            self.lives.append(life)

            return self.lives
        
    def move_lives(self):
        for life in self.lives:
            life.y += 7

        if life.y >= 2000:
            self.lives.remove(life)

        return self.lives
    
    def generate_power_up(self):
        if len(self.powerups) < MAX_POWER_UP:
            pwup = pygame.Rect(random.randint(0, WIDTH - POWER_UP_IMAGE.get_width()), random.randint(-5000, -4800),
                               POWER_UP_IMAGE.get_width(), POWER_UP_IMAGE.get_height())
            self.powerups.append(pwup)

        return self.powerups
    
    def move_power_up(self):
        for pwup in self.powerups:
            pwup.y += 5

        if pwup.y >= 2000 and self.powerup_count == 0:
            self.powerups.remove(pwup)

        return self.powerups
    
    def power_up_use(self, keys_pressed, aliens, spaceship, bullets, muted):
        if keys_pressed[pygame.K_LCTRL] and self.powerup_count > 0 or keys_pressed[pygame.K_RCTRL] and self.powerup_count > 0:
            for alien in aliens.aliens[:]:
                aliens.aliens.remove(alien)
                self.score += 1

            for pwup in self.powerups:
                self.powerups.remove(pwup)

            bullets.laser_beam = pygame.Rect(spaceship.rect.x + spaceship.rect.width/2 - 10, 0, 20, spaceship.rect.y)
            bullets.move_laser_beam()

            if not muted:
                LASER_BEAM_SOUND.set_volume(0.5)
                LASER_BEAM_SOUND.play()

            self.powerup_count = 0

        return self.powerups, self.powerup_count, aliens, self.score


def draw_game(spaceship, aliens, bullets, features, HIGHSCORE, hit_start_time, muted):
    win.blit(BG_IMAGE, (0, 0))
    if spaceship.spaceship_hit:
        elapsed_time = pygame.time.get_ticks() - hit_start_time
        if elapsed_time % SPACESHIP_FLASH_PERIOD < SPACESHIP_FLASH_PERIOD / 2:
            win.blit(SPACESHIP, (spaceship.rect.x, spaceship.rect.y))
        if elapsed_time > SPACESHIP_FLASH_DUR:
            spaceship.spaceship_hit = False
    else:
        win.blit(SPACESHIP, (spaceship.rect.x, spaceship.rect.y))
    for alien in aliens.aliens:
            win.blit(ALIEN, (alien.x, alien.y))
    for bullet in bullets.bullets:
        pygame.draw.rect(win, (230, 30, 100), bullet)
    lives_text = LIVES_FONT.render(f"{features.lives_count}", 1, (255, 255, 255))
    win.blit(LIVES_BOX_IMAGE, (10, 20 + POWER_UP_BOX_IMAGE.get_height()))
    win.blit(lives_text, (15 + POWER_UP_BOX_IMAGE.get_width(), 25 + LIVES_BOX_IMAGE.get_height()))
    win.blit(HIGHSCORE_IMAGE, (10, 30 + LIVES_BOX_IMAGE.get_height() + POWER_UP_BOX_IMAGE.get_height()))
    hi_score_text = HI_SCORE_FONT.render(f"{HIGHSCORE}", 1, (255, 255, 255))
    win.blit(hi_score_text, (15 + HIGHSCORE_IMAGE.get_width(), 35 + LIVES_BOX_IMAGE.get_height() + POWER_UP_BOX_IMAGE.get_height()))
    win.blit(SCORE_IMAGE, (10, 40 + LIVES_BOX_IMAGE.get_height() + POWER_UP_BOX_IMAGE.get_height() + HIGHSCORE_IMAGE.get_height()))
    score_text = SCORE_FONT.render(f"{features.score}", 1, (255, 255, 255))
    win.blit(score_text, (15 + SCORE_IMAGE.get_width(), 
                          45 + LIVES_BOX_IMAGE.get_height() + POWER_UP_BOX_IMAGE.get_height() + HIGHSCORE_IMAGE.get_height()))
    help_text = HELP_FONT.render("F1 HELP", 1, (255, 255, 255))
    win.blit(help_text, (WIDTH - help_text.get_width() - 10, 15))
    for pwup in features.powerups:
        win.blit(POWER_UP_IMAGE, (pwup.x, pwup.y))
    powerup_text = POWER_UP_FONT.render(f"{features.powerup_count}", 1, (255, 255, 255))
    win.blit(POWER_UP_BOX_IMAGE, (10, 10))
    win.blit(powerup_text, (15 + POWER_UP_BOX_IMAGE.get_width(), 15))
    pygame.draw.rect(win, (230, 30, 100), bullets.laser_beam)
    for life in features.lives:
        win.blit(LIVES_IMAGE, (life.x, life.y))
    del_text = HELP_FONT.render("DEL MENU", 1, (255, 255, 255))
    win.blit(del_text, (WIDTH - del_text.get_width() - 10, help_text.get_height() + 20))
    if muted:
        mute_text = MUTE_FONT.render("M UNMUTE", 1, (255, 255, 255))
        win.blit(mute_text, (WIDTH - mute_text.get_width() - 10, help_text.get_height() + del_text.get_height() + 30))
        win.blit(MUTE_IMAGE, (WIDTH - mute_text.get_width() - MUTE_IMAGE.get_width(), help_text.get_height() + del_text.get_height() + 10))
    if not muted:
        unmute_text = MUTE_FONT.render("M MUTE", 1, (255, 255, 255))
        win.blit(unmute_text, (WIDTH - unmute_text.get_width() - 10, help_text.get_height() + del_text.get_height() + 30))
        win.blit(UNMUTE_IMAGE, (WIDTH - unmute_text.get_width() - MUTE_IMAGE.get_width(), help_text.get_height() + del_text.get_height() + 10))

    
    pygame.display.update()

    return spaceship.spaceship_hit


def game_over(game_over_text, muted):
    if not muted:
        GAME_LOOP_MUSIC.stop()
        GAME_END_SOUND.play()
    text = GAME_OVER_FONT.render(game_over_text, 1, (255, 255, 255))
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3500)
    if not muted:
        GAME_LOOP_MUSIC.play(loops=-1)


def pause(paused_text):
    text = PAUSE_FONT.render(paused_text, 1, (255, 255, 255))
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    aliens = Aliens()
    bullets = Bullets()
    features = GameFeatures()
    paused = False
    muted = False
    show_help = False
    hit_start_time = 0

    while run:
        clock.tick(60)

        game_over_text = ""
        if features.lives_count == 0:
            game_over_text = "GAME OVER"
            if features.score > int(HIGHSCORE):
                with open("highscore.txt", mode="w") as file:
                    file.write(str(features.score))
            game_over(game_over_text, muted)
            start.main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if features.score > int(HIGHSCORE):
                    with open("highscore.txt", mode="w") as file:
                        file.write(str(features.score))
                run = False 
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    bullets.generate(spaceship, muted) 
                
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
                    if features.score > int(HIGHSCORE):
                        with open("highscore.txt", "w") as file:
                            file.write(str(features.score))
                    start.main()

                if event.key == pygame.K_r:
                    main()

                if event.key == pygame.K_m:
                    if not muted:
                        for sound in SOUNDS:
                            sound.set_volume(0.0)
                            muted = True
                    elif muted:
                        for sound in SOUNDS:
                            if sound != GAME_LOOP_MUSIC:
                                sound.set_volume(0.3)
                            else:
                                sound.set_volume(0.4)
                        muted = False

            if event.type == SPACESHIP_HIT:
                features.lives_count -= 1
                spaceship.spaceship_hit = True
                hit_start_time = pygame.time.get_ticks()
            
            if event.type == ALIEN_HIT:
                features.score += 1

            if event.type == POWERUP:
                features.powerup_count += 1

            if event.type == GOT_LIVE and features.lives_count < 5:
                features.lives_count += 1

        keys_pressed = pygame.key.get_pressed()
        
        if not paused and not show_help:
            spaceship.move(keys_pressed, aliens, features, muted)
            aliens.generate()
            aliens.move()
            bullets.move(aliens, muted)
            bullets.move_laser_beam()
            features.generate_lives()
            features.move_lives()
            features.generate_power_up()
            features.move_power_up()
            features.powerups, features.powerup_count, aliens, features.score = features.power_up_use(keys_pressed, 
            aliens, spaceship, bullets, muted)
            
            spaceship.spaceship_hit = draw_game(spaceship, aliens, bullets, features, HIGHSCORE, hit_start_time, muted)

    pygame.quit()

if __name__ == "__main__":
    main()