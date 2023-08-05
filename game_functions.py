# game_functions.py
import pygame
import random
from game_objects import Enemy

MAX_ENEMIES = 7 # Define o maximo de objetos enemies que pode existir na tela

enemy_spawn_interval = 200  # Intervalo de tempo entre cada spawn de inimigo (em milissegundos)
last_enemy_spawn_time = 0    # Tempo do último spawn de inimigo

enemy_shot_interval = 3000  # Intervalo de tempo entre cada tiro inimigo (em milissegundos)
last_enemy_shot_time = 0    # Tempo do último tiro inimigo

def check_collisions(missiles, enemies, score):
    for missile in missiles:
        for enemy in enemies:
            if missile.rect.colliderect(enemy.rect):
                missiles.remove(missile)
                enemies.remove(enemy)
                print(len(enemies))
                score += 100
                break
    return score

def check_player_collisions(enemy_missiles, ship, lives):
    for enemy_missile in enemy_missiles:
        if enemy_missile.rect.colliderect(ship.rect):
            enemy_missiles.remove(enemy_missile)
            lives -= 1
            break
    return lives

def spawn_enemies(enemies, enemy_images, missile_image, screen_width, screen_height):
    global last_enemy_spawn_time

    current_time = pygame.time.get_ticks()
    if len(enemies) < MAX_ENEMIES and current_time - last_enemy_spawn_time >= enemy_spawn_interval:
        enemy_side = random.choice(['left', 'right'])
        if enemy_side == 'left':
            enemy_x = 0
            enemy_speed = random.uniform(0.5, 1)
        else:
            enemy_x = screen_width
            enemy_speed = -random.uniform(0.5, 1)
        
        enemy_y = random.randint(screen_height // 6, screen_height // 1.5)
        enemy_image = random.choice(enemy_images)
        
        # Verifica o índice da imagem selecionada e ajusta a velocidade se for o índice 1 (enemy_image2)
        if enemy_image == enemy_images[1]:
            enemy_speed *= 2.0
        
        # Gere um intervalo de tiro aleatório para cada inimigo
        enemy_shot_interval = random.randint(2000, 4000)

        enemies.add(Enemy(enemy_image, missile_image, enemy_x, enemy_y, enemy_speed, enemy_shot_interval))
        last_enemy_spawn_time = current_time

    # Verifica se algum inimigo saiu da tela e remove
    for enemy in enemies.copy():
        if enemy.rect.x < 0 or enemy.rect.x > screen_width:
            enemies.remove(enemy)


def draw_score(screen, score, screen_width):
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("SCORE: " + str(score), True, (255, 255, 255))
    score_text_width = score_text.get_width()
    screen.blit(score_text, (screen_width - score_text_width - 10, 10))  # Alinhado à direita com um espaço de 10 pixels

def draw_lives(screen, lives, screen_width):
    font = pygame.font.SysFont(None, 30)
    lives_text = font.render("LIVES: " + str(lives), True, (255, 255, 255))
    lives_text_width = lives_text.get_width()
    screen.blit(lives_text, (10, 10))  # Alinhado à esquerda com um espaço de 10 pixels no eixo X e Y

def enemy_fire(enemies, enemy_missiles):
    global last_enemy_shot_time, enemy_shot_interval

    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_shot_time >= enemy_shot_interval:
        for enemy in enemies:
            missile = enemy.fire("down")  # Passando "down" como a direção do míssil do inimigo
            if missile:
                enemy_missiles.add(missile)
        last_enemy_shot_time = current_time
        enemy_shot_interval = random.randint(2000, 4000)
