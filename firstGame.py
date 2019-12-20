import pygame

# Init Section
pygame.init()
win_height = 700
win_width = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("First Game")
player_image = pygame.image.load('assets\images\Ship.png')


class circle_projectile(object):
    def __init__(self, x, y, color, vel, radius, is_enemy):
        self.x = x
        self.y = y
        self.color= color
        self.vel = vel
        self.radius = radius
        self.is_enemy = is_enemy

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Player:
    def __init__(self, x, y, width, height, velocity, max_cooldown):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.max_cooldown = max_cooldown
        self.cooldown = 0

    def draw(self, win):
        win.blit(player_image, (player.x, player.y))


player = Player(win_width // 2 - 50, win_height - 32, 60, 32, 5, 30)
run = True
clock = pygame.time.Clock()


def redrawGameWindow():
    win.fill((0, 0, 0))
    player.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


def handlePlayerInput():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.velocity
    if keys[pygame.K_RIGHT] and player.x < win_width - player.width:
        player.x += player.velocity
    if keys[pygame.K_SPACE] and player.cooldown == 0:
        bullets.append(circle_projectile(round(player.x + player.width // 2),
            round(player.y), (0, 200, 0), 5, 6, True))
        player.cooldown = player.max_cooldown
    if player.cooldown > 0:
        player.cooldown -= 1


bullets = []
# Gameloop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    handlePlayerInput()
    for bullet in bullets:
        if bullet.y > -5:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    redrawGameWindow()
    clock.tick(60)
pygame.quit()
