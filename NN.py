import os
import pygame
import base
import bird
import pipe
import neat

pygame.init()
WIDTH, HEIGHT = 288, 512
BG_IMG = pygame.image.load('assets/bg.png')
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
VELOCITY = -2
THRESHOLDS = {
    'base': -337,
    'pipe': 72
}
FONT = pygame.font.SysFont("Arial", 12)
gen = 0


def main(genomes, config):
    global WIN, gen
    SCREEN = WIN
    gen += 1

    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(bird.Bird())
        ge.append(genome)

    first_base = base.Base(0, VELOCITY)
    bases = [first_base]
    first_pipe = pipe.Pipe(512, VELOCITY)
    pipes = [first_pipe]
    framecounter = 0
    score = 0
    distance = 0
    flag = 0
    activate = False

    clock = pygame.time.Clock()
    run = 1

    # main loop
    while run:

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and 144 > pipes[0].x + pipes[0].sprite1.get_width():
                pipe_ind = 1
        else:
            run = 0
            break

        for x, b in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            output = nets[birds.index(b)].activate((b.y, abs(b.y - pipes[pipe_ind].y), abs(b.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                b.jump()

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
                for genome in ge:
                    genome.fitness += 5
                score += 1
                flag = 1
        distance -= VELOCITY / 10

        # Updating and drawing
        SCREEN.blit(BG_IMG, (0, 0))
        for b in birds:
            b.update()
            b.draw(SCREEN)
        for p in pipes:
            p.update()
            p.draw(SCREEN)
        for bs in bases:
            bs.update()
            bs.draw(SCREEN)
        scr = FONT.render('Score : ' + str(score), True, (0, 0, 0))
        dist = FONT.render('Distance : ' + str(round(distance)), True, (0, 0, 0))
        SCREEN.blit(scr, (0, 0))
        SCREEN.blit(dist, (0, 15))

        # Animation
        for b in birds:
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

        # controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    activate = not activate
                if event.key == pygame.K_ESCAPE:
                    run = 0
                    pygame.quit()

        # Collision detection
        for p in pipes:
            for b in birds:
                if p.collide(b):
                    ge[birds.index(b)].fitness -= 1
                    nets.pop(birds.index(b))
                    ge.pop(birds.index(b))
                    birds.pop(birds.index(b))
        for b in birds:
            if b.rect.bottom > 400 or b.y < -50:
                ge[birds.index(b)].fitness -= 1
                nets.pop(birds.index(b))
                ge.pop(birds.index(b))
                birds.pop(birds.index(b))

        # Clock tick
        clock.tick(FPS)

def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)


    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)