import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ship War")

# Carregar a imagem de fundo do universo (que já possui o tamanho correto)
background_image = pygame.image.load("universo.jpg")
# Carregar a imagem da nave
image = pygame.image.load("nave1.png")
# Redimensionar a imagem para o tamanho desejado
image = pygame.transform.scale(image, (50, 50))

# Carregar a imagem do míssil
missile_image = pygame.image.load("tiro1.jpg")
# Redimensionar o míssil em 50%
missile_image = pygame.transform.scale(missile_image, (missile_image.get_width() // 2, missile_image.get_height() // 2))

# Carregar a imagem da nave inimiga
enemy_image = pygame.image.load("ship2.png")
# Redimensionar a imagem da nave inimiga para o tamanho desejado
enemy_image = pygame.transform.scale(enemy_image, (50, 50))

# Tamanho e posição inicial da imagem
image_x, image_y = SCREEN_WIDTH // 2, 4 * SCREEN_HEIGHT // 5

# Velocidade de movimento da imagem
speed = 1

# Lista para armazenar os mísseis
missiles = []

# Tempo do último disparo
last_shot_time = 0

# Intervalo mínimo entre os tiros em milissegundos (0,1 segundo = 100 milissegundos)
shot_interval = 100

# Lista para armazenar as naves inimigas
enemies = []

# Intervalo mínimo entre o aparecimento das naves inimigas em milissegundos
enemy_spawn_interval = 200  # 0,5 segundo

# Variável para armazenar o SCORE
score = 0

# Função para verificar colisão entre retângulos
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Loop principal do jogo
while True:
    # Lidar com eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Capturar as teclas pressionadas
    keys = pygame.key.get_pressed()

    # Movimento da imagem
    if keys[pygame.K_LEFT]:
        image_x -= speed
    if keys[pygame.K_RIGHT]:
        image_x += speed
    if keys[pygame.K_UP]:
        image_y -= speed
    if keys[pygame.K_DOWN]:
        image_y += speed

    # Atirar o míssil quando a barra de espaço for pressionada e respeitar o intervalo mínimo
    if keys[pygame.K_SPACE] and pygame.time.get_ticks() - last_shot_time >= shot_interval:
        missile_x, missile_y = image_x + image.get_width() / 2 - missile_image.get_width() / 2, image_y
        missiles.append((missile_x, missile_y))
        last_shot_time = pygame.time.get_ticks()  # Atualiza o tempo do último disparo

    # Movimento de todos os mísseis
    for missile_idx in range(len(missiles)):
        missile_x, missile_y = missiles[missile_idx]
        missile_y -= 2.0
        missiles[missile_idx] = (missile_x, missile_y)

    # Filtrar mísseis que saíram da tela
    missiles = [(x, y) for x, y in missiles if y + missile_image.get_height() >= 0]

    # Adicionar naves inimigas em intervalos de tempo
    if pygame.time.get_ticks() % (2 * enemy_spawn_interval) == 0:
        enemy_x = 0
        enemy_y = random.randint(SCREEN_HEIGHT // 6, SCREEN_HEIGHT // 1.5 - enemy_image.get_height())  # Posição aleatória entre 1/4 e 1/2 da tela
        enemy_speed = random.uniform(1.5, 2)  # Velocidade aleatória para a nave inimiga
        enemies.append((enemy_x, enemy_y, enemy_speed))
    elif pygame.time.get_ticks() % (2 * enemy_spawn_interval) == enemy_spawn_interval:
        enemy_x = SCREEN_WIDTH - enemy_image.get_width()
        enemy_y = random.randint(SCREEN_HEIGHT // 6, SCREEN_HEIGHT // 1.5 - enemy_image.get_height())  # Posição aleatória entre 1/4 e 1/2 da tela
        enemy_speed = -random.uniform(1.5, 2)  # Velocidade aleatória (negativa) para a nave inimiga da direita
        enemies.append((enemy_x, enemy_y, enemy_speed))

    # Movimento das naves inimigas
    for enemy_idx in range(len(enemies)):
        enemy_x, enemy_y, enemy_speed = enemies[enemy_idx]
        enemy_x += enemy_speed
        enemies[enemy_idx] = (enemy_x, enemy_y, enemy_speed)

    # Filtrar naves inimigas que saíram da tela
    enemies = [(x, y, speed) for x, y, speed in enemies if 0 <= x <= SCREEN_WIDTH]

    # Verificar colisão entre mísseis e naves inimigas e excluir ambas em caso de colisão
    for missile_x, missile_y in missiles:
        missile_rect = pygame.Rect(missile_x, missile_y, missile_image.get_width(), missile_image.get_height())
        for enemy_x, enemy_y, _ in enemies:
            enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_image.get_width(), enemy_image.get_height())
            if check_collision(missile_rect, enemy_rect):
                missiles.remove((missile_x, missile_y))
                enemies.remove((enemy_x, enemy_y, _))
                # Incrementar o SCORE quando uma nave2 é destruída
                score += 100
                break

    # Preencher a tela com a imagem de fundo do universo
    screen.blit(background_image, (0, 0))

    # Desenhar o SCORE na tela (canto superior direito)
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("SCORE: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

    # Desenhar todos os mísseis na tela
    for missile_x, missile_y in missiles:
        screen.blit(missile_image, (missile_x, missile_y))

    # Desenhar todas as naves inimigas na tela
    for enemy_x, enemy_y, _ in enemies:
        screen.blit(enemy_image, (enemy_x, enemy_y))

    # Desenhar a imagem da nave na tela
    screen.blit(image, (image_x, image_y))

    # Atualizar a tela 
    pygame.display.flip()
