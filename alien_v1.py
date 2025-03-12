# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

03/2025
github.com/MaximeBond
"""

import pygame
import sys
import os
import random

def check_files():
    """ Vérifie si tous les fichiers nécessaires existent avant de lancer le jeu. """
    required_files = [
        "media/spaceman.png",
        "media/alien.png",
        "media/angry_alien.png",
        "media/win.png",
        "media/game_over.png",
        "media/nostromo.jpg",
        "media/spaceship.jpg",
        "media/game_on.mp3",
        "media/disco-boogie.mp3",
        "media/game_over.mp3",
        "best_time.txt",
        "sup.otf"
    ]

    missing_files = [file for file in required_files if not os.path.exists(file)]
    
    if missing_files:
        # Initialiser Pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Erreur de Fichier")

        # Fond noir
        screen.fill((0, 0, 0))

        # Charger une police système
        font = pygame.font.SysFont("arial", 30)
        small_font = pygame.font.SysFont("arial", 20)

        # Texte d'erreur
        error_text = font.render("! Fichiers manquants détectés !", True, (255, 0, 0))
        screen.blit(error_text, (150, 50))

        # Lister les fichiers manquants
        y_offset = 120
        for file in missing_files:
            file_text = small_font.render(f"- {file}", True, (255, 255, 255))
            screen.blit(file_text, (50, y_offset))
            y_offset += 30

        # Instructions pour quitter
        quit_text = font.render("Appuyez sur n'importe quelle touche pour quitter...", True, (200, 200, 0))
        screen.blit(quit_text, (100, 500))

        pygame.display.flip()

        # Attente de l'utilisateur
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()
                    sys.exit()
                    
# Vérifier que tous les fichiers sont présents
check_files()
                    
# Initialisation de Pygame
pygame.init()
pygame.mixer.init()

# Constantes
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ALIEN_SPEED = 3
SPACEMAN_SPEED = 9
LASER_SPEED = 16

##### Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Game")
clock = pygame.time.Clock() # Contrôle la fréquence d'images par seconde (FPS) donc la vitesse de la boucle de jeu

##### Police d'affichage
font_path = "sup.otf"
font_title = pygame.font.Font(font_path, 40)  # Police par défaut, taille 36
font = pygame.font.SysFont("arialblack", 32)
font_arial = pygame.font.SysFont("arial", 32)

##### Charger les images et redimensionner
# Astronaute
spaceman_img_right = pygame.image.load("media/spaceman.png") 
spaceman_img_right = pygame.transform.scale(spaceman_img_right, (spaceman_img_right.get_width() // 4, spaceman_img_right.get_height() // 4))
spaceman_img_left = pygame.transform.flip(spaceman_img_right, True, False)
spaceman_img = spaceman_img_right  # Par défaut vers la droite
spaceman_rect = spaceman_img.get_rect(midright=(WIDTH // 2 - 250, HEIGHT // 2))
""" get_rect() crée un rectangle autour de l'image,
midtop positionne le centre du haut de l'image à la position (x, y) """
# Alien
alien_img_left = pygame.image.load("media/alien.png")  
alien_img_left = pygame.transform.scale(alien_img_left, (alien_img_left.get_width() // 2.5, alien_img_left.get_height() // 2.5))
alien_img_right = pygame.transform.flip(alien_img_left, True, False)
alien_img = alien_img_left  # Par défaut vers la gauche
alien_rect = alien_img.get_rect(midleft=(WIDTH // 2 + 250, HEIGHT // 2))
# Alien touché par un laser
alien_touched = pygame.image.load("media/angry_alien.png")  # Alien touché par un laser
alien_touched = pygame.transform.scale(alien_touched, (alien_touched.get_width() // 2, alien_touched.get_height() // 2))

def load_best_time():
    if os.path.exists("best_time.txt"): # Vérifier que le fichier existe
        with open("best_time.txt", "r") as file:
            try:
                return float(file.read().strip()) # strip() enlève les espaces au début et à la fin d'une chaine de caractères
            except ValueError:
                return None
    return None
##### Record de temps pour éliminer l'alien
best_time = load_best_time()

##### Charger les images de fonds
# Fin du jeu
win_screen = pygame.image.load("media/win.png")
win_screen = pygame.transform.scale(win_screen, (WIDTH, HEIGHT)) # Ré-ajuster à la taille de l'écran de jeu
game_over_screen = pygame.image.load("media/game_over.png")
game_over_screen = pygame.transform.scale(game_over_screen, (WIDTH, HEIGHT))
# Intro
background_intro = pygame.image.load("media/nostromo.jpg")
background_intro = pygame.transform.scale(background_intro, (WIDTH, HEIGHT))
# Jeu
background_game = pygame.image.load("media/spaceship.jpg")
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))


def run_game():
    ##### Variables déclérées hors de la fonction et modifiées par la fonction
    global spaceman_img, alien_img, spaceman_rect, alien_rect, best_time
    
    # 🎵 Musique
    pygame.mixer.music.load("media/game_on.mp3")  
    pygame.mixer.music.play(-1)  # En boucle
    
    ##### Variables
    spaceman_direction = 1  # 1 = droite, -1 = gauche
    spaceman_lifecount = 100
    alien_hit_time = None  # Enregistre le moment où l'alien est touché par un laser
    alien_hit_duration = 500  # Durée (en millisecondes) où l'image de l'alien change en "angry_alien.png"
    alien_frozen = False  # Drapeau pour empêcher le mouvement temporairement
    alien_lifecount = 10
    # Liste des lasers
    lasers = []
    
    reload_duration = 3000  # 3 secondes avant de pouvoir retirer un laser
    reload_bar_width = 200  # Largeur de la barre de recharge
    reload_bar_height = 20  # Hauteur de la barre de recharge
    last_shot_time = pygame.time.get_ticks() - reload_duration  # Temps du dernier tir
    
    spaceman_rect = spaceman_img.get_rect(midright=(WIDTH // 2 - 250, HEIGHT // 2))
    alien_rect = alien_img.get_rect(midleft=(WIDTH // 2 + 250, HEIGHT // 2))

    alien_lifecount = 10
    spaceman_lifecount = 100
    last_shot_time = pygame.time.get_ticks() - reload_duration  
    start_time = pygame.time.get_ticks() # Chrono pour enregistrer le meilleur temps 

    ##### Boucle de jeu

    running = True
    while running:
        screen.blit(background_game, (0, 0))
    
        ##### Gestion des événements (QUIT, s)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_shot_time >= reload_duration:
                        last_shot_time = current_time
                        if spaceman_direction == 1:
                            laser_rect = pygame.Rect(spaceman_rect.right, spaceman_rect.centery, 20, 5)
                        else:
                            laser_rect = pygame.Rect(spaceman_rect.left - 20, spaceman_rect.centery, 20, 5)
                        lasers.append((laser_rect, spaceman_direction))
    
        ##### Déplacement de l'astronaute par le joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceman_rect.x -= SPACEMAN_SPEED
            spaceman_direction = -1
            spaceman_img = spaceman_img_left
        if keys[pygame.K_RIGHT]:
            spaceman_rect.x += SPACEMAN_SPEED
            spaceman_direction = 1
            spaceman_img = spaceman_img_right
        if keys[pygame.K_UP]:
            spaceman_rect.y -= SPACEMAN_SPEED
        if keys[pygame.K_DOWN]:
            spaceman_rect.y += SPACEMAN_SPEED
        
        # Empêcher le joueur de sortir de l'écran
        spaceman_rect.clamp_ip(screen.get_rect())
    
        ##### Déplacement des lasers (tir selon la direction du spaceman)
        new_lasers = []
        for laser, direction in lasers: # Les lasers sont de type "tuples" (position et taille, direction) 
            laser.x += LASER_SPEED * direction
            if 0 < laser.x < WIDTH:
                new_lasers.append((laser, direction))
        lasers = new_lasers
    
        ##### Gestion de l'alien
        # L'alien est gelé si touché par un laser
        if alien_frozen:
            if pygame.time.get_ticks() - alien_hit_time > alien_hit_duration:
                alien_frozen = False
                alien_img = alien_img_right if alien_rect.x < spaceman_rect.x else alien_img_left  
        else:
            # Déplacement de l'alien vers le spaceman
            increase = 0
            if random.random() < 0.3:
                increase = ALIEN_SPEED
            if alien_rect.x < spaceman_rect.x:
                alien_rect.x += (ALIEN_SPEED + increase)  # Déplacement vers la droite
                alien_img = alien_img_right
            elif alien_rect.x > spaceman_rect.x:
                alien_rect.x -= (ALIEN_SPEED + increase)  # Déplacement vers la gauche
                alien_img = alien_img_left
            if alien_rect.y < spaceman_rect.y:
                alien_rect.y += (ALIEN_SPEED + increase)  # Déplacement vers le bas
            elif alien_rect.y > spaceman_rect.y:
                alien_rect.y -= (ALIEN_SPEED + increase)  # Déplacement vers le haut

        ##### Vérification des collisions entre les lasers et l'alien
        for laser, _ in lasers:
            if alien_rect.colliderect(laser):
                lasers.remove((laser, _))
                alien_img = alien_touched  # Change l'image de l'alien
                alien_hit_time = pygame.time.get_ticks()
                alien_frozen = True 
                alien_lifecount -= 1
                if alien_lifecount == 0:
                    end_time = pygame.time.get_ticks()  # Arrêt du chrono
                    time_taken = (end_time - start_time) / 1000  # Millisecondes en secondes
                    # Enregistrer le meilleur temps
                    if best_time is None or time_taken < best_time:
                        best_time = time_taken
                        with open("best_time.txt", "w") as file:
                            file.write(str(best_time))
        
        ##### Vérification des collisions entre l'alien et l'astronaute
        if spaceman_rect.colliderect(alien_rect):
            spaceman_lifecount -= 1
            
         
        ##### Fin du jeu si Astronaute ou Alien à 0
        if spaceman_lifecount == 0:
            show_end_screen("GAME OVER! Alien got you!", 1)
            return  # Quitter `run_game()'
        elif alien_lifecount == 0:
            show_end_screen(f"SUCCESS! Alien eliminated in {time_taken:.2f} sec!", 0)
            return
            
        ##### Affichage
        # Affiche l'alien, l'astronaute et les lasers
        screen.blit(spaceman_img, spaceman_rect)
        screen.blit(alien_img, alien_rect)
        for laser, _ in lasers:
            pygame.draw.rect(screen, RED, laser)
        # Affiche les compteurs de vies de l'alien et de l'astronaute
        spaceman_life_text = font.render(f"Spaceman: {spaceman_lifecount}", True, (255, 255, 255))  # Couleur noire
        alien_life_text = font.render(f"Alien: {alien_lifecount}", True, (255, 255, 255))
        screen.blit(spaceman_life_text, (10, 10))  # En haut à gauche de l'écran
        screen.blit(alien_life_text, (WIDTH - 200, 10))  # En haut à droite de l'écran
        
        # Affiche la bar de rechargement du pistolet 
        time_since_last_shot = pygame.time.get_ticks() - last_shot_time
        reload_fill = min(reload_bar_width, (time_since_last_shot / reload_duration) * reload_bar_width)
        """ min() empêche "reload_fill" de dépasser la largeur de la barre de recharge
        pygame.draw.rect(surface, color, rect) / rect → (x, y, width, height) """
        pygame.draw.rect(screen, (200, 200, 200), (WIDTH // 2 - reload_bar_width // 2, HEIGHT - 50, reload_bar_width, reload_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (WIDTH // 2 - reload_bar_width // 2, HEIGHT - 50, reload_fill, reload_bar_height))
        # Affiche "Reloading ..."
        if time_since_last_shot < reload_duration:
            reload_text = font_arial.render("Reloading ...", True, (255, 0, 0))
            screen.blit(reload_text, (WIDTH // 2 - reload_bar_width // 2, HEIGHT - 80))
        # Affiche le temps écoulé et le meilleur temps
        game_timer = (pygame.time.get_ticks() - start_time) / 1000
        game_timer_text = font.render(f"Timer: {game_timer:.3f} sec", True, (255, 255, 0))
        screen.blit(game_timer_text, (10, HEIGHT - 90))
        if best_time is not None:
            best_time_text = font.render(f"Best Time: {best_time:.3f} sec", True, (0, 255, 0))
            screen.blit(best_time_text, (10, HEIGHT - 50))
        
        pygame.display.flip() # Màj de tout l'écran de jeu pour prendre en compte les changements 
        clock.tick(60) # 60 FPS


def show_end_screen(message, integer):
    
    global spaceman_img, spaceman_rect
    
    pygame.mixer.music.stop()
    # 🎵 Musique
    if integer == 0:
        pygame.mixer.music.load("media/disco-boogie.mp3")  
    else:
        pygame.mixer.music.load("media/game_over.mp3")
    pygame.mixer.music.play(-1)
        
    spaceman_rect = spaceman_img.get_rect(midright=(WIDTH // 2 - 350, HEIGHT // 2 + 100))
    
    text_color = (50, 205, 50) if integer == 0 else (255, 0, 0)
    text = font.render(message, True, text_color)        
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50)) 
    
    if integer == 0:
        restart_text = font.render("Press 'SPACE KEY' to Restart, 'q' to Quit, 'j' to Jump!", True, (255, 255, 0))
    else:
        restart_text = font.render("Press 'SPACE KEY' to Restart, 'q' to Quit", True, (255, 255, 0))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
    
    # Variables pour le saut du scpaceman
    jump_velocity = -20  # Negatif va vers le haut
    gravity = 2  # Gravité qui tire vers le bas
    jumping = False
    velocity_y = 0
    # Attendre que le joueur relance ou quitte le jeu
    running = True
    while running:
        
        clock.tick(60)
        # Toujours afficher d'abord l'arrière plan pour effacer les images précédentes
        screen.blit(win_screen if integer == 0 else game_over_screen, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop() # Arrête la musique quand le jeu se relance
                    running = False
                    run_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_j and not jumping:
                            jumping = True
                            velocity_y = jump_velocity
        # Jump logic
        if jumping:
            spaceman_rect.y += velocity_y  
            velocity_y += gravity  
            
            if spaceman_rect.y >= HEIGHT // 2 + 100:  # Arrête quand retour à la position d'origine
                spaceman_rect.y = HEIGHT // 2 + 100
                jumping = False  
                
        screen.blit(text, text_rect)
        screen.blit(restart_text, restart_rect)
        if integer == 0:
            screen.blit(spaceman_img, spaceman_rect)
        
        pygame.display.flip()
    

def show_intro_screen():
    
    # Affiche l'écran d'introduction et attend que le joueur presse la touche 'SPACE'.
    screen.blit(background_intro, (0, 0))
    
    # Titre
    title_text = font_title.render("ALIEN GAME", True, (255, 0, 0))  
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 210))
    
    # Instructions
    instruction_text = font.render("Press 'SPACE KEY' to start", True, (50, 205, 50))  
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 180))
    instruction2_text = font.render("s: Shoot                  \u2190 \u2191 \u2192 \u2193 : Move", True, (255, 0, 0))
    instruction2_rect = instruction2_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
    
    # Affiche le meilleur temps si disponible / Accède à 'best_time' sans la modifier
    if best_time is not None:
        best_time_text = font.render(f"Best Time: {best_time:.3f} sec", True, (50, 205, 50))
        best_time_rect = best_time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 320))
        screen.blit(best_time_text, best_time_rect)
    
    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)
    screen.blit(instruction2_text, instruction2_rect)
    screen.blit(spaceman_img, spaceman_rect)
    screen.blit(alien_img, alien_rect)
    pygame.display.flip()

    # Attendre que le joueur tape 'SPACE' pour commencer le jeu
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # S'assurer que le programme s'arrête complétement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    waiting = False  
                
if __name__ == "__main__":
    while True: 
        show_intro_screen()
        run_game()

pygame.quit()
