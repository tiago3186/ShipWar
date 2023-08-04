# main.py
import pygame
import sys
from game_objects import Ship, Missile, Enemy
import game_functions as gf

pygame.init()

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ship War")

# Carregar as imagens e criar os objetos
background_image = pygame.image.load("resources/img/universo.jpg")
image = pygame.image.load("resources/img/nave1.png")
missile_image = pygame.image.load("resources/img/tiro1.jpg")
enemy_missile_image = pygame.image.load("resources/img/tiro2.jpg")
enemy_image = pygame.image.load("resources/img/ship2.png")

# Criar a nave
ship = Ship(image, missile_image, SCREEN_WIDTH // 2, 4 * SCREEN_HEIGHT // 5)

# Lista para armazenar os mísseis
missiles = pygame.sprite.Group()

# Lista para armazenar as naves inimigas
enemies = pygame.sprite.Group()

# Lista para armazenar os mísseis das naves inimigas
enemy_missiles = pygame.sprite.Group()

# Tempo do último disparo
last_shot_time = 0
shot_interval = 100

# Variável para armazenar o SCORE e LIVES
score = 0
lives = 5

# Armazena o estado do jogo
game_over = False

# Controla o reinicio do jogo
game_restart_requested = False

# Cria um font_large pra ser usado em estados específicos do jogo
font_large = pygame.font.SysFont(None, 60)

# Cria um font_medium pra ser usado em estados específicos do jogo
font_medium = pygame.font.SysFont(None, 35)

# Loop principal do jogo
while True:
    # Lidar com eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Capturar as teclas pressionadas
    keys = pygame.key.get_pressed()

    # Movimento da nave
    ship.move(keys)

    # Atirar o míssil quando a barra de espaço for pressionada e respeitar o intervalo mínimo
    if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_shot_time >= shot_interval:
        missile = ship.fire()
        if missile:
            missiles.add(missile)
            last_shot_time = pygame.time.get_ticks()  # Atualiza o tempo do último disparo

    # Movimento de todos os mísseis
    for missile in missiles:
        missile.move()

    # Adicionar naves inimigas em intervalos de tempo
    gf.spawn_enemies(enemies, enemy_image, enemy_missile_image, SCREEN_WIDTH, SCREEN_HEIGHT)     

    # Movimento das naves inimigas
    for enemy in enemies:
        enemy.move()

    # Verificar colisão entre mísseis e naves inimigas e excluir ambas em caso de colisão
    score = gf.check_collisions(missiles, enemies, score)

    # Verificar colisão entre mísseis inimigos e naves do jogador e diminuir 1 do valor de LIVES
    lives = gf.check_player_collisions(enemy_missiles, ship, lives)

    # Quando o valor de lives chegar a 0 deve dar Game Over

    # Preencher a tela com a imagem de fundo do universo
    screen.blit(background_image, (0, 0))

    # Desenhar o SCORE na tela (canto superior direito)
    gf.draw_score(screen, score, SCREEN_WIDTH)
    gf.draw_lives(screen, lives, SCREEN_WIDTH)

    # Desenhar todos os mísseis na tela
    missiles.draw(screen)
    enemy_missiles.draw(screen)

    # Desenhar todas as naves inimigas na tela
    enemies.draw(screen)    

    # Desenhar a nave na tela
    screen.blit(ship.image, ship.rect)

    # Atualizar o movimento dos mísseis inimigos
    gf.enemy_fire(enemies, enemy_missiles)

    # Atualizar o movimento dos mísseis inimigos
    for missile in enemy_missiles:
        missile.move()

    # Controla o game over caso o número de vidas seja zero
    if lives <= 0:
        game_over = True

    if game_over:
        while game_over:  # Loop para manter o jogo pausado após o game over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Verifica se a tecla ENTER foi pressionada
                        # Reiniciar o jogo
                        game_restart_requested = True
                        game_over = False
                    
            game_over_text = font_large.render("Game Over", True, (255, 0, 0))    
            press_enter_to_restart_text = font_medium.render("Press Enter to Restart", True, (255, 255, 255))       
            screen.blit(press_enter_to_restart_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))

            # Atualizar a tela
            pygame.display.flip()
                
    if game_restart_requested:
            # Reiniciar o jogo aqui
            score = 0
            lives = 5
            ship = Ship(image, missile_image, SCREEN_WIDTH // 2, 4 * SCREEN_HEIGHT // 5)
            missiles.empty()
            enemies.empty()
            enemy_missiles.empty()
            last_shot_time = 0
            game_restart_requested = False  # Reinício do jogo concluído

    else:
            # Atualizar a tela
            pygame.display.flip()