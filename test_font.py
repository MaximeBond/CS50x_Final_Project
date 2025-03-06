# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 15:36:07 2025

@author: maxime
"""

import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Font Viewer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font_list = pygame.font.get_fonts()  # Get all available fonts
font_size = 24
scroll_y = 0  # Scroll position

def draw_fonts(scroll_y):
    """Render and display fonts with scrolling"""
    screen.fill(BLACK)  # Clear screen
    y = 10 - scroll_y  # Apply scrolling
    
    for font_name in font_list:
        try:
            font = pygame.font.SysFont(font_name, font_size)
            text = font.render(font_name, True, WHITE)
            screen.blit(text, (10, y))
            y += font_size + 5  # Space between lines
        except:
            pass  # Skip fonts that can't be rendered

    pygame.display.flip()  # Refresh screen

# Main loop
running = True
while running:
    draw_fonts(scroll_y)  # Draw with the current scroll position
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                scroll_y += 30  # Scroll down
            elif event.key == pygame.K_UP:
                scroll_y = max(0, scroll_y - 30)  # Scroll up, limit at 0

pygame.quit()
