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
background_image = pygame.image.load("universo.jpg")
image = pygame.image.load("nave1.png")
missile_image = pygame.image.load("tiro1.jpg")
enemy_image = pygame.image.load("ship2.png")

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

# Variável para armazenar o SCORE
score = 0

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
    gf.spawn_enemies(enemies, enemy_image, missile_image, SCREEN_WIDTH, SCREEN_HEIGHT)   
    print(enemies, enemy_image, missile_image, SCREEN_WIDTH, SCREEN_HEIGHT) 

    # Movimento das naves inimigas
    for enemy in enemies:
        enemy.move()

    # Verificar colisão entre mísseis e naves inimigas e excluir ambas em caso de colisão
    score = gf.check_collisions(missiles, enemies, score)

    # Preencher a tela com a imagem de fundo do universo
    screen.blit(background_image, (0, 0))

    # Desenhar o SCORE na tela (canto superior direito)
    gf.draw_score(screen, score, SCREEN_WIDTH)

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


    # Atualizar a tela
    pygame.display.flip()
