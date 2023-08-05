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

    menu = pygame_menu.Menu('SHIP WAR', SCREEN_WIDTH, SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DEFAULT)
    menu.add.label('MENU', font_size=60)
    menu.add.button('NOVO JOGO', start_game)  # Chamada para a função start_game
    menu.add.button('SAIR', pygame_menu.events.EXIT)

    menu.mainloop(screen)
