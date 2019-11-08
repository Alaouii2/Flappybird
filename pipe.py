import pygame
import random


class Pipe:
    WIDTH = 100
    START = 100
    START_FLAG = 1

    def __init__(self, x, vel):
        self.pos = self.x, self.y = x, 0
        self.vel = vel
        self.sprite1 = pygame.image.load('assets/pipe.png')
        self.sprite2 = pygame.transform.flip(self.sprite1, 0, 1)
        self.top = 0
        self.bottom = 0
        self.set_height()

    def get_rect(self):
        return [self.sprite1.get_rect(topleft=(self.x, self.bottom)),
                self.sprite2.get_rect(topleft=(self.x, self.top))]

    def set_height(self):
        h = self.sprite1.get_height()
        if Pipe.START_FLAG == 1:
            self.y = 120
            Pipe.START_FLAG = 0
        else:
            self.y = random.randint(50, 250)
        self.top = self.y - h
        self.bottom = self.y + self.WIDTH

    def move(self):
        self.x += self.vel

    def update(self):
        self.move()

    def draw(self, win):
        win.blits(blit_sequence=((self.sprite2, (self.x, self.top)), (self.sprite1, (self.x, self.bottom))))

    def collide(self, bird):
        bird_mask = bird.get_mask()

        mask1 = pygame.mask.from_surface(self.sprite1)
        mask2 = pygame.mask.from_surface(self.sprite2)

        offset1 = (self.x - bird.rect.left, self.bottom - bird.rect.top)
        offset2 = (self.x - bird.rect.left, self.top - bird.rect.top)

        points1 = bird_mask.overlap(mask1, offset1)
        points2 = bird_mask.overlap(mask2, offset2)

        if points1 or points2:
            return True

        return False
