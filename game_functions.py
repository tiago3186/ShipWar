# game_functions.py
import pygame
import random
from game_objects import Enemy

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
                score += 100
                break
    return score

def spawn_enemies(enemies, enemy_image, missile_image, screen_width, screen_height):
    global last_enemy_spawn_time

    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time >= enemy_spawn_interval:
        enemy_side = random.choice(['left', 'right'])
        if enemy_side == 'left':
            enemy_x = 0
            enemy_speed = random.uniform(0.5, 1)
        else:
            enemy_x = screen_width
            enemy_speed = -random.uniform(0.5, 1)
        enemy_y = random.randint(screen_height // 6, screen_height // 1.5)        
        enemies.add(Enemy(enemy_image, missile_image, enemy_x, enemy_y, enemy_speed))
        last_enemy_spawn_time = current_time


def draw_score(screen, score, screen_width):
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("SCORE: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

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
