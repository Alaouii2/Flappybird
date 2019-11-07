import pygame


class Bird:
    def __init__(self):
        self.y = 200
        self.vel = 0
        self.acc = 0.33
        self.angle = 0
        self.angle_vel = 2.5
        self.img = [pygame.image.load('assets/bird1.png'),
                    pygame.image.load('assets/bird2.png'),
                    pygame.image.load('assets/bird3.png')]
        self.img_rot = self.img
        self.img_count = 0
        self.rect = [self.img[i].get_rect(center=(144, self.y)) for i in range(3)]

    def get_rect(self):
        return self.rect[self.img_count]

    def jump(self):
        self.vel = -5
        self.angle = 45

    def move(self):
        self.vel += self.acc
        self.y += self.vel

    def rotate(self):
        if self.angle > -80:
            self.angle -= self.angle_vel
        new_img = pygame.transform.rotate(self.img[self.img_count], self.angle)
        self.rect = [new_img.get_rect(center=(144, self.y))]*3
        return new_img

    def update(self):
        self.move()
        self.img_rot = self.rotate()

    def draw(self, win):
        win.blit(self.img_rot, self.rect[self.img_count])

