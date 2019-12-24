import pygame

# Init Section
pygame.init()
win_height = 700
win_width = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("First Game")


class Projectile(object):
    def __init__(self, x, y, color, vel, is_enemy):
        self.x = x
        self.y = y
        self.color = color
        self.vel = vel
        self.is_enemy = is_enemy

    def draw(self):
        pass

    def move(self):
        pass


class CircleProjectile(Projectile):
    def __init__(self, radius, *args):
        self.radius = radius
        super().__init__(*args)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class RectProjectile(Projectile):
    def __init__(self, width, height, *args):
        self.width = width
        self.height = height
        super().__init__(*args)

    def draw(self, win):
        pygame.draw.rect(win, self.color,
                         (self.x, self.y, self.width, self.height))


class Player:
    player_image = pygame.image.load('assets\images\Ship.png')

    def __init__(self, x, y, width, height, vel, can_fire):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.can_fire = can_fire

    def draw(self, win):
        win.blit(self.player_image, (self.x, self.y))


class Enemy:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 2
        self.anim_speed = 30
        self.score = 0
        self.counter = 0
        self.image_id = 1

    def draw(self, win):
        if (self.counter >= self.anim_speed):
            self.counter = 0
            if (self.image_id == 1):
                self.image_id = 2
                self.enemy_image = self.enemy_image2
            else:
                self.image_id = 1
                self.enemy_image = self.enemy_image1
        self.counter += 1
        win.blit(self.enemy_image, (self.x, self.y))

    def move(self, win):
        self.y += self.vel

    def shoot(self):
        pass


class AlphaEnemy(Enemy):
    enemy_image1 = pygame.image.load('assets\images\InvaderA1.png')
    enemy_image2 = pygame.image.load('assets\images\InvaderA2.png')

    def __init__(self, *args):
        super().__init__(*args)
        self.score = 10
        self.enemy_image = self.enemy_image1


def redraw_game_window():
    win.fill((0, 0, 0))
    player.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    if player_bullet != None:
        player_bullet.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    pygame.display.update()


def handle_player_input():
    global player_bullet
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.vel
    if keys[pygame.K_RIGHT] and player.x < win_width - player.width:
        player.x += player.vel
    if keys[pygame.K_SPACE] and player.can_fire:
        player.can_fire = False
        player_bullet = RectProjectile(6, 20,
                                       round(player.x + player.width // 2 - 3),
                                       round(player.y), (0, 200, 0), 6, True)


'''        bullets.append(
            CircleProjectile(5, round(player.x + player.width // 2),
                             round(player.y), (0, 200, 0), 6, True))
        player.cooldown = player.max_cooldown
    if player.cooldown > 0:
        player.cooldown -= 1
'''

player = Player(win_width // 2 - 50, win_height - 32, 60, 32, 5, True)
run = True
clock = pygame.time.Clock()
bullets = []
enemies = []
player_bullet = None
# Gameloop
enemies.append(AlphaEnemy(100, 100, 16, 16))
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    handle_player_input()
    if (player_bullet != None):
        if (player_bullet.y > -5):
            player_bullet.y -= player_bullet.vel
        else:
            player_bullet = None
            player.can_fire = True
    for bullet in bullets:
        if bullet.y < win_height:
            bullet.y += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    for enemy in enemies:
        if enemy.y < win_height:
            enemy.move(win)
        else:
            enemies.pop(enemies.index(enemy))
    redraw_game_window()
    clock.tick(60)
pygame.quit()
