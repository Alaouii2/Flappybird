import pygame
import base
import bird
import pipe

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
FONT = pygame.font.SysFont("Arial Black", 12)


def main():
    clock = pygame.time.Clock()
    framecounter = 0
    run = 1
    state = 0

    f = open("highscore.txt", "r")
    highscore = f.read()
    f.close()
    print(highscore)
    # main loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = 0
                if state == 0:
                    if event.key == pygame.K_SPACE:
                        b = bird.Bird()
                        first_base = base.Base(0, VELOCITY)
                        bases = [first_base]
                        first_pipe = pipe.Pipe(512, VELOCITY)
                        pipes = [first_pipe]
                        score = 0
                        distance = 0
                        flag = 0
                        activate = False
                        state = 1
                elif state == 1:
                    if event.key == pygame.K_SPACE:
                        b.jump()
                    if event.key == pygame.K_d:
                        activate = not activate

        if state == 0:
            SCREEN.blit(BG_IMG, (0, 0))
            f = open("highscore.txt", "r")
            highscore = f.read()
            f.close()
            hs = FONT.render("HIGHSCORE : " + highscore, True, (255, 255, 255))
            SCREEN.blit(hs, (WIDTH // 2 - hs.get_width() // 2, HEIGHT // 2 - hs.get_height() // 2 - 50))
            start = FONT.render('Press JUMP (space) to play (esc to quit)', True, (255, 255, 255))
            if (framecounter // 25) % 2 == 0:
                SCREEN.blit(start, (WIDTH // 2 - start.get_width() // 2, HEIGHT // 2 - start.get_height() // 2))

        elif state == 1:
            # Pipes and bases spawning
            if pipes[-1].x < THRESHOLDS['pipe']:
                pipes.append(pipe.Pipe(288, VELOCITY))
            elif pipes[0].x + pipes[0].sprite1.get_width() < 0:
                flag = 0
                pipes.pop(0)
            if bases[-1].x < 0:
                bases.append(base.Base(bases[-1].x + bases[-1].sprite.get_width(), VELOCITY))
            elif bases[0].x < THRESHOLDS['base']:
                bases.pop(0)

            # Score/distance count
            if flag == 0:
                if pipes[0].x < 144:
                    score += 1
                    flag = 1
            distance -= VELOCITY / 10

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
            scr = FONT.render('Score : ' + str(score), True, (255, 255, 255))
            dist = FONT.render('Distance : ' + str(round(distance)), True, (255, 255, 255))
            SCREEN.blit(scr, (0, 0))
            SCREEN.blit(dist, (0, 15))

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

            # Collision detection
            for p in pipes:
                if p.collide(b):
                    if score > int(highscore):
                        f = open("highscore.txt", "w")
                        f.write(str(score))
                        f.close()
                    state = 0
            if b.rect.bottom > 400 or b.y < -50:
                if score > int(highscore):
                    f = open("highscore.txt", "w")
                    f.write(str(score))
                    f.close()
                state = 0

        # Update display
        framecounter += 1
        pygame.display.flip()

        # Clock tick
        clock.tick(FPS)
        print(highscore)
    pygame.quit()


if __name__ == '__main__':
    main()
