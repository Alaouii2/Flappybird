import pygame

class Pipe:

    def __init__(self, x, y, vel):
        self.pos = self.x, self.y = x, y
        self.width = 100
        self.vel = vel
        self.img = [pygame.image.load('assets/pipe.png'), pygame.transform.flip(pygame.image.load('assets/pipe.png'), 0, 1)]
        self.imgw, self.imgh = self.img[0].get_width(), self.img[0].get_height()

    def get_rect(self):
        return [self.img[0].get_rect(topleft=(self.x, self.y + self.width // 2)),
                self.img[0].get_rect(bottomleft=(self.x, self.y - self.width // 2))]

    def move(self):
        self.x += self.vel

    def update(self):
        self.move()

    def draw(self, win):
        rect = self.get_rect()
        win.blits(blit_sequence=((self.img[0], rect[0]),
                                 (self.img[1], rect[1])))
