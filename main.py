import pygame
import bird, pipe, base
import random

pygame.init()

WIDTH, HEIGHT = 288, 512
BG_IMG = pygame.image.load('assets/bg.png')
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
VELOCITY = -2
THRESHOLDS = {
    'base': -337,
    'pipe': 72
}
FONT = pygame.font.SysFont("Arial", 12)

b = bird.Bird()
bird_hitbox = b.get_rect()
first_base = base.Base(0, VELOCITY)
bases = [first_base]
danger = [first_base.get_rect()]
first_pipe = pipe.Pipe(512, 200, VELOCITY)
pipes = [first_pipe]
framecounter = 0
score = 0
flag = 0

clock = pygame.time.Clock()
run = 1

# main loop
while run:

    # controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                b.jump()

    # Pipes and bases spawning
    if pipes[-1].x < THRESHOLDS['pipe']:
        pipes.append(pipe.Pipe(288, random.randint(80, 330), VELOCITY))
    elif pipes[0].x + pipes[0].imgw < 0:
        flag = 0
        pipes.pop(0)
    if bases[-1].x < 0:
        bases.append(base.Base(bases[-1].x + bases[-1].imgw, VELOCITY))
    elif bases[0].x < THRESHOLDS['base']:
        bases.pop(0)

    # Collision detection
    bird_hitbox = b.get_rect()
    base_hitboxes = []
    for bs in bases:
        base_hitboxes.append(bs.get_rect())
    pipe_hitboxes = []
    for p in pipes:
        pipe_hitboxes.extend(p.get_rect())
    danger = base_hitboxes + pipe_hitboxes
    if bird_hitbox.collidelist(danger) != -1:
        print(danger)
        print(bird_hitbox, bird_hitbox.collidelist(danger))
        run = 0

    # Score count
    if flag == 0:
        if pipes[0].x < 144:
            score += 1
            print(score)
            flag = 1

    # Updating and drawing
    SCREEN.blit(BG_IMG, (0, 0))
    b.update()
    b.draw(SCREEN)
    for p in pipes:
        p.update()
        p.draw(SCREEN)
    for bs in bases:
        bs.update()
        bs.draw(SCREEN)
    scr = FONT.render('Score : ' + str(score), True, (0, 0, 0))
    SCREEN.blit(scr, (0, 0))
    # Animation
    if framecounter > 12:
        framecounter = 0
        b.img_count = 0
    if framecounter > 9:
        b.img_count = 1
    elif framecounter > 6:
        b.img_count = 2
    elif framecounter > 3:
        b.img_count = 1
    framecounter += 1

    # Update display
    pygame.display.flip()

    # Clock tick
    clock.tick(FPS)

pygame.quit()
