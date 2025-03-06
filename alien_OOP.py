import pygame
import sys
import os
import random

# Constants
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ALIEN_SPEED = 3
SPACEMAN_SPEED = 9
LASER_SPEED = 16
RELOAD_DURATION = 3000  # 3 seconds cooldown

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32)

# Load images
spaceman_img_right = pygame.image.load("spaceman.png")
spaceman_img_right = pygame.transform.scale(spaceman_img_right, (spaceman_img_right.get_width() // 4, spaceman_img_right.get_height() // 4))
spaceman_img_left = pygame.transform.flip(spaceman_img_right, True, False)

alien_img_left = pygame.image.load("alien.png")
alien_img_left = pygame.transform.scale(alien_img_left, (alien_img_left.get_width() // 2.5, alien_img_left.get_height() // 2.5))
alien_img_right = pygame.transform.flip(alien_img_left, True, False)
alien_touched = pygame.image.load("angry_alien.png")
alien_touched = pygame.transform.scale(alien_touched, (alien_touched.get_width() // 2, alien_touched.get_height() // 2))

background_game = pygame.image.load("spaceship2.jpg")
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))
background_game = pygame.image.load("spaceship2.jpg")
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))
background_intro = pygame.image.load("nostromo.jpg")
background_intro = pygame.transform.scale(background_intro, (WIDTH, HEIGHT))
win_screen = pygame.image.load("win.jpg")
win_screen = pygame.transform.scale(win_screen, (WIDTH, HEIGHT))
game_over_screen = pygame.image.load("game_over.png")
game_over_screen = pygame.transform.scale(game_over_screen, (WIDTH, HEIGHT))

def load_best_time():
    if os.path.exists("best_time.txt"):
        try:
            with open("best_time.txt", "r") as file:
                return float(file.read().strip())
        except ValueError:
            return None
    return None

class Spaceman:
    def __init__(self):
        self.image_right = spaceman_img_right
        self.image_left = spaceman_img_left
        self.image = self.image_right
        self.rect = self.image.get_rect(midright=(WIDTH // 2 - 250, HEIGHT // 2))
        self.direction = 1
        self.lifecount = 100
        self.last_shot_time = pygame.time.get_ticks() - RELOAD_DURATION

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= SPACEMAN_SPEED
            self.direction = -1
            self.image = self.image_left
        if keys[pygame.K_RIGHT]:
            self.rect.x += SPACEMAN_SPEED
            self.direction = 1
            self.image = self.image_right
        if keys[pygame.K_UP]:
            self.rect.y -= SPACEMAN_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += SPACEMAN_SPEED
        self.rect.clamp_ip(screen.get_rect())

    def shoot(self, lasers):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= RELOAD_DURATION:
            self.last_shot_time = current_time
            laser_rect = pygame.Rect(self.rect.right if self.direction == 1 else self.rect.left - 20, self.rect.centery, 20, 5)
            lasers.append(Laser(laser_rect, self.direction))

class Alien:
    def __init__(self):
        self.image_left = alien_img_left
        self.image_right = alien_img_right
        self.image_touched = alien_touched
        self.image = self.image_left
        self.rect = self.image.get_rect(midleft=(WIDTH // 2 + 250, HEIGHT // 2))
        self.lifecount = 10
        self.frozen = False
        self.hit_time = None

    def move_towards(self, spaceman):
        if self.frozen:
            if pygame.time.get_ticks() - self.hit_time > 500:
                self.frozen = False
                self.image = self.image_right if self.rect.x < spaceman.rect.x else self.image_left
        else:
            dx = ALIEN_SPEED * 2 if random.random() < 0.3 else ALIEN_SPEED
            if self.rect.x < spaceman.rect.x:
                self.rect.x += dx
                self.image = self.image_right
            elif self.rect.x > spaceman.rect.x:
                self.rect.x -= dx
                self.image = self.image_left
            if self.rect.y < spaceman.rect.y:
                self.rect.y += dx
            elif self.rect.y > spaceman.rect.y:
                self.rect.y -= dx

class Laser:
    def __init__(self, rect, direction):
        self.rect = rect
        self.direction = direction

    def move(self):
        self.rect.x += LASER_SPEED * self.direction
        return 0 < self.rect.x < WIDTH

class Game:
    def __init__(self):
        self.spaceman = Spaceman()
        self.alien = Alien()
        self.lasers = []
        self.running = True

    def run(self):
        while self.running:
            screen.blit(background_game, (0, 0))
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

    def show_end_screen(self, message, screen_image):
        screen.blit(screen_image, (0, 0))
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.spaceman.shoot(self.lasers)

    def update(self):
        keys = pygame.key.get_pressed()
        self.spaceman.move(keys)
        self.alien.move_towards(self.spaceman)
        self.lasers = [laser for laser in self.lasers if laser.move()]
        
        if self.alien.lifecount <= 0:
            self.show_end_screen("SUCCESS! Alien eliminated!", win_screen)
        elif self.spaceman.lifecount <= 0:
            self.show_end_screen("GAME OVER! The alien got you!", game_over_screen)

    def draw(self):
        screen.blit(self.spaceman.image, self.spaceman.rect)
        screen.blit(self.alien.image, self.alien.rect)
        for laser in self.lasers:
            pygame.draw.rect(screen, RED, laser.rect)
        spaceman_life_text = font.render(f"Spaceman: {self.spaceman.lifecount}", True, WHITE)
        alien_life_text = font.render(f"Alien: {self.alien.lifecount}", True, WHITE)
        screen.blit(spaceman_life_text, (10, 10))
        screen.blit(alien_life_text, (WIDTH - 200, 10))

if __name__ == "__main__":
    game = Game()
    game.run()
