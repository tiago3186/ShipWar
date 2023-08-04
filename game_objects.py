# game_objects.py
import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, image, missile_image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.missile_image = missile_image        

    def move(self, keys):
        speed = 1
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
        if keys[pygame.K_UP]:
            self.rect.y -= speed
        if keys[pygame.K_DOWN]:
            self.rect.y += speed

    def fire(self):
        missile = Missile(self.missile_image, self.rect.x + self.rect.width // 2, self.rect.y, "up")
        return missile

class Missile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, direction):
        super().__init__()
        self.image = pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x + self.image.get_width() / 2 - self.image.get_width() / 2
        self.rect.y = y
        self.direction = direction  # Armazena a direção do míssil
        
    def move(self):
        if self.direction == "up":
            self.rect.y -= 2.0
        elif self.direction == "down":
            self.rect.y += 2.0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, missile_image, x, y, speed, shot_interval):
        super().__init__()
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.missile_image = missile_image
        self.shot_interval = shot_interval  # Intervalo de tiro específico para cada inimigo
        self.last_shot_time = 0  # Tempo do último tiro do inimigo
    def fire(self, direction):  # Adicionamos o parâmetro 'direction' aqui
        missile = Missile(self.missile_image, self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height, direction)
        return missile
    
    def move(self):
        self.rect.x += self.speed
