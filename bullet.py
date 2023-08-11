import pygame
from const import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, speed = 12) -> None:
        super().__init__()
        self.group = group
        self.image = pygame.image.load(IMAGE_PATH['bullet_red']).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = speed
    
    def reset(self, postion) -> None:
        self.rect.center = postion
        self.add(self.group)
    
    def update(self) -> None:
        if self.alive():
            if self.rect.top < 0:
                self.kill()
            else:
                self.rect.top -= self.speed

class BlueBullet(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, speed = 12) -> None:
        super().__init__()
        self.group = group
        self.image = pygame.image.load(IMAGE_PATH['bullet_blue']).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = speed
    
    def reset(self, postion) -> None:
        self.rect.center = postion
        self.add(self.group)
    
    def update(self) -> None:
        if self.alive():
            if self.rect.top < 0:
                self.kill()
            else:
                self.rect.top -= self.speed