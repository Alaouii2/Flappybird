import pygame


class Base:
    def __init__(self, x, vel):
        self.x = x
        self.vel = vel
        self.img = pygame.image.load('assets/base.png')
        self.imgw = self.img.get_width()

    def get_rect(self):
        return self.img.get_rect(topleft=(self.x, 400))

    def move(self):
        self.x += self.vel

    def update(self):
        self.move()

    def draw(self, win):
        win.blit(self.img, (self.x, 400))

