import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, speed = 12) -> None:
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.active = False
    
    def reset(self, postion) -> None:
        self.rect.center = postion
        self.active = True
    
    def update(self) -> None:
        if self.active:
            if self.rect.top < 0:
                self.active = False
                self.kill()
            else:
                self.rect.top -= self.speed