import pygame, random
from gym_sorting_puzzle.envs.montesori_env import PuzzleView, LABEL

s = PuzzleView()
done = False
FPS = 60
clock = pygame.time.Clock()
direction = None
player = None
print([type for type in s.puzzle._solution()])
labels = [LABEL[type] for type in s.puzzle._solution()]
for i in range(0, len(labels), 4):
     print(labels[i:i+4])

while not done:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("See you next time!")
            done = True
        elif s.done:
            print("WON! Good job!")
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # choose random tile and random move
                player, direction = s.random_move()
            if event.key == pygame.K_w:
                direction = 'N'
            elif event.key == pygame.K_s:
                direction = 'S'
            elif event.key == pygame.K_a:
                direction = 'W'
            elif event.key == pygame.K_d:
                direction = 'E'
        elif event.type == pygame.KEYUP and player != None:
            player.velocity[1] = 0
            player.velocity[0] = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            player = [s for s in s.puzzle.play_tiles if s.rect.collidepoint(pos)]
            player = player.pop() if len(player) > 0 else None

    if player and direction:
        s.move(player, direction)
        direction = None
    s.update("human")
