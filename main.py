# main.py
import pygame
import pygame_menu
from game import start_game

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Função main que inicia o pygame_menu
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ship War")

    my_custom_theme = pygame_menu.themes.Theme(
        title_font_size=50,
        title_font_color=(255, 255, 0),  # Amarelo (R, G, B)
        widget_font_size=30,
        widget_font_color=(255, 255, 255),
        background_color=(0, 0, 0),
        selection_color=(255, 0, 0),
        title_offset=(SCREEN_WIDTH // 2.7, 0)  # Centralizar horizontalmente
    )

    menu = pygame_menu.Menu('SHIP WAR', SCREEN_WIDTH, SCREEN_HEIGHT, theme=my_custom_theme)

    menu.add.button('NOVO JOGO', start_game)
    menu.add.button('SAIR', pygame_menu.events.EXIT)

    menu.mainloop(screen)
