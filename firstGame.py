import pygame

# Init Section
pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")


class Player:
    def __init__(self, x, y, width, height, velocity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity


player = Player(50, 50, 50, 50, 5)
run = True
clock = pygame.time.Clock()

# Gameloop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player.velocity
    if keys[pygame.K_RIGHT]:
        player.x += player.velocity
    if keys[pygame.K_DOWN]:
        player.y += player.velocity
    if keys[pygame.K_UP]:
        player.y -= player.velocity
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), (player.x, player.y, 40, 60))
    pygame.display.update()
    win.fill((0))
    clock.tick(60)

pygame.quit()
