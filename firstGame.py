import pygame

# Init Section
pygame.init()
win_height = 600
win_width = 800
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
    player_image = pygame.transform.scale(player_image, (45, 24))

    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.can_fire = True

    def draw(self, win):
        win.blit(self.player_image, (self.x, self.y))


class Enemy:
    def __init__(self, x, y, width, height, anim_offset):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.score = 0
        self.counter = 0 + anim_offset
        self.image_id = 1

    def draw(self, win, anim_speed):
        if (self.counter >= anim_speed):
            self.counter = 0
            if (self.image_id == 1):
                self.image_id = 2
                self.enemy_image = self.enemy_image2
            else:
                self.image_id = 1
                self.enemy_image = self.enemy_image1
        self.counter += 1
        win.blit(self.enemy_image, (self.x, self.y))

    def move(self, win, direction, is_by_wall, vel):
        if (is_by_wall):
            self.y += self.height + 10
        elif (direction == "right"):
            self.x += vel
        elif (direction == "left"):
            self.x -= vel
        if (self.y + self.height + 3 >= win_height):
            pygame.quit()

    def shoot(self):
        pass


class AlphaEnemy(Enemy):
    enemy_image1 = pygame.image.load('assets\images\InvaderA1.png')
    enemy_image2 = pygame.image.load('assets\images\InvaderA2.png')
    enemy_image1 = pygame.transform.scale(enemy_image1, (32, 24))
    enemy_image2 = pygame.transform.scale(enemy_image2, (32, 24))

    def __init__(self, *args):
        super().__init__(*args)
        self.score = 10
        self.enemy_image = self.enemy_image1


class BetaEnemy(Enemy):
    enemy_image1 = pygame.image.load('assets\images\InvaderB1.png')
    enemy_image2 = pygame.image.load('assets\images\InvaderB2.png')
    enemy_image1 = pygame.transform.scale(enemy_image1, (32, 24))
    enemy_image2 = pygame.transform.scale(enemy_image2, (32, 24))

    def __init__(self, *args):
        super().__init__(*args)
        self.score = 20
        self.enemy_image = self.enemy_image1


class GammaEnemy(Enemy):
    enemy_image1 = pygame.image.load('assets\images\InvaderC1.png')
    enemy_image2 = pygame.image.load('assets\images\InvaderC2.png')
    enemy_image1 = pygame.transform.scale(enemy_image1, (32, 24))
    enemy_image2 = pygame.transform.scale(enemy_image2, (32, 24))

    def __init__(self, *args):
        super().__init__(*args)
        self.score = 30
        self.enemy_image = self.enemy_image1


def redraw_game_window():
    win.fill((0, 0, 0))
    player.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    if player_bullet != None:
        player_bullet.draw(win)
    for enemy in enemies:
        enemy.draw(win, anim_speed + 2 * len(enemies))
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
        player_bullet = RectProjectile(3, 16,
                                       round(player.x + player.width // 2 - 1),
                                       round(player.y - 1), (0, 200, 0), 7,
                                       True)


def spawn_enemies():
    x = 0
    y = 0
    for d in range(1):
        for i in range(11):
            enemies.append(
                GammaEnemy(x + i * 46, y + d * 38 + 8, 32, 24, d * 15))
    for d in range(1, 3):
        for i in range(11):
            enemies.append(
                BetaEnemy(x + i * 46, y + d * 38 + 8, 32, 24, d * 15))
    for d in range(3, 5):
        for i in range(11):
            enemies.append(
                AlphaEnemy(x + i * 46, y + d * 38 + 8, 32, 24, d * 15))


player = Player(win_width // 2 - 45, win_height - 24, 45, 24, 5)
run = True
clock = pygame.time.Clock()
bullets = []
enemies = []
player_bullet = None

direction = "right"
anim_speed = 8
vel = 0.25
# Gameloop
spawn_enemies()
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
    check_wall = False
    for enemy in enemies:
        if (direction == "right" and enemy.x + enemy.width >= win_width):
            direction = "left"
            check_wall = True
        elif (direction == "left" and enemy.x <= 0):
            direction = "right"
            check_wall = True
    for enemy in enemies:
        enemy.move(win, direction, check_wall, vel + 6 / (2 * len(enemies)))
    redraw_game_window()
    clock.tick(60)
pygame.quit()
