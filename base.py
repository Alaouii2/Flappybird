import pygame


class Base:
    def __init__(self, x, vel):
        self.x = x
        self.vel = vel
        self.sprite = pygame.image.load('assets/base.png')

    def get_rect(self):
        return self.sprite.get_rect(topleft=(self.x, 400))

    def move(self):
        self.x += self.vel

    def update(self):
        self.move()

    def draw(self, win):
        win.blit(self.sprite, (self.x, 400))


