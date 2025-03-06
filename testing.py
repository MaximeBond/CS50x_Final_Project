# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 17:42:33 2025

@author: maxime
"""

import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load and scale the image
# win_screen = pygame.image.load("win.png")
win_screen = pygame.image.load("/medianostromo.jpg")
win_screen = pygame.transform.scale(win_screen, (WIDTH, HEIGHT))

spaceman_img = pygame.image.load("/mediaspaceman.png") 
spaceman_img = pygame.transform.scale(spaceman_img, (spaceman_img.get_width() // 4, spaceman_img.get_height() // 4))

spaceman_rect = spaceman_img.get_rect(midright=(WIDTH // 2 - 250, HEIGHT // 2))

font_path = "sup.otf"
font_title = pygame.font.Font(font_path, 40)  # Police par défaut, taille 36
font = pygame.font.SysFont("arial", 32)

# Jump physics variables
jump_velocity = -20  # Jump force (negative goes up)
gravity = 2  # Gravity pulling back down
jumping = False
velocity_y = 0

running = True
while running:
    clock.tick(60)  # Maintain frame rate
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j and not jumping:
                jumping = True
                velocity_y = jump_velocity  # Apply jump force

    # Jump logic
    if jumping:
        spaceman_rect.y += velocity_y  # Move up/down
        velocity_y += gravity  # Apply gravity
        
        if spaceman_rect.y >= HEIGHT // 2:  # Stop when reaching the original position
            spaceman_rect.y = HEIGHT // 2
            jumping = False  # Reset jump

    # Draw background first, then character
    screen.blit(win_screen, (0, 0))  # Background first
    screen.blit(spaceman_img, spaceman_rect)  # Then the spaceman
    title_text = font_title.render("ALIEN GAME", True, (153, 50, 204))  
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 210))
    screen.blit(title_text, title_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()