import pygame


class Bird:
    def __init__(self):
        self.y = 200
        self.vel = 0
        self.acc = 0.33
        self.angle = 0
        self.angle_vel = 2.5
        self.sprites = [pygame.image.load('assets/bird1.png'),
                    pygame.image.load('assets/bird2.png'),
                    pygame.image.load('assets/bird3.png')]
        self.img_rot = self.sprites[0]
        self.img_count = 0
        self.rect = self.sprites[self.img_count].get_rect()

    def get_rect(self):
        return self.rect

    def jump(self):
        self.vel = -5
        self.angle = 45

    def move(self):
        self.vel += self.acc
        self.y += self.vel

    def rotate(self):
        if self.angle > -80:
            self.angle -= self.angle_vel
        self.img_rot = pygame.transform.rotate(self.sprites[self.img_count], self.angle)
        self.rect = self.img_rot.get_rect(center=(144, self.y))

    def update(self):
        self.x = self.rect.x
        self.move()
        self.rotate()

    def get_mask(self):
        return pygame.mask.from_surface(self.img_rot)

    def draw(self, win):
        win.blit(self.img_rot, self.rect)

