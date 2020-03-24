import pygame
import os
import random

# Display and enviroment init section
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
win_height = 600
win_width = 800
win = pygame.display.set_mode((win_width, win_height))
font = pygame.font.Font(os.path.join("assets", "fonts", 'unifont.ttf'), 16)
pygame.display.set_caption("Space Invaders by Zuvix")

#Load Sound Assets
bullet_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'shoot.wav'))
enemy_death_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'invaderkilled.wav'))
track_sounds = []
for i in range(1, 5):
    track_sounds.append(
        pygame.mixer.Sound(
            os.path.join('assets', 'nSounds',
                         'fastinvader' + str(i) + ".wav")))
#Load Images
img_p = pygame.image.load(os.path.join('assets', 'images', 'Ship.png'))
img_a1 = pygame.image.load(os.path.join('assets', 'images', 'InvaderA1.png'))
img_a2 = pygame.image.load(os.path.join('assets', 'images', 'InvaderA2.png'))
img_b1 = pygame.image.load(os.path.join('assets', 'images', 'InvaderB1.png'))
img_b2 = pygame.image.load(os.path.join('assets', 'images', 'InvaderB2.png'))
img_c1 = pygame.image.load(os.path.join('assets', 'images', 'InvaderC1.png'))
img_c2 = pygame.image.load(os.path.join('assets', 'images', 'InvaderC2.png'))

#Define Colors
ORANGE = pygame.Color(255, 100, 0)
GREEN = pygame.Color(78, 255, 87)
YELLOW = pygame.Color(241, 255, 0)
BLUE = pygame.Color(0, 150, 240)
PURPLE = pygame.Color(203, 0, 255)
RED = pygame.Color(237, 28, 36)
WHITE = pygame.Color(255, 255, 255)


def calculate_velocity(number_of_enemies: int):
    if number_of_enemies > 0:
        return 0.25 + 10 / (1.5 * number_of_enemies)
    else:
        return 0


def set_color(img, color):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color.a = img.get_at((x, y)).a  # Preserve the alpha value.
            img.set_at((x, y), color)  # Set the color of the pixel.


class Projectile(object):
    def __init__(self, x, y, color, vel, is_enemy):
        self.x = x
        self.y = y
        self.color = color
        self.vel = vel
        self.is_enemy = is_enemy
        self.x_min = self.x - 0.2
        self.x_max = self.x + 0.2
        self.horizontal_direction = "right"

    def draw(self):
        pass

    def move(self):
        pass

    def horiznotal_move(self):
        if self.horizontal_direction == "right":
            if self.x < self.x_max:
                self.x += 0.10
            else:
                self.horizontal_direction = "left"
        elif self.horizontal_direction == "left":
            if self.x > self.x_min:
                self.x -= 0.10
            else:
                self.horizontal_direction = "right"


class CircleProjectile(Projectile):
    def __init__(self, radius, *args):
        self.radius = radius
        super().__init__(*args)

    def draw(self, window):
        self.horiznotal_move()
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


class RectProjectile(Projectile):
    def __init__(self, width, height, *args):
        self.width = width
        self.height = height
        super().__init__(*args)

    def draw(self, window):
        self.horiznotal_move()
        pygame.draw.rect(window, self.color,
                         (int(self.x), int(self.y), self.width, self.height))


class Player:
    player_image = img_p
    player_image = pygame.transform.scale(player_image, (42, 21))

    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.can_fire = True

    def draw(self, window):
        window.blit(self.player_image, (self.x, self.y))


class Enemy:
    def __init__(self, x, y, width, height, score, color, image_1, image_2,
                 is_active, depth, row, min_shoot_cd, max_shoot_cd,
                 bullet_speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.score = score
        self.image_id = 1
        self.is_active = is_active
        self.depth = depth
        self.row = row
        self.min_shoot_cd = min_shoot_cd
        self.max_shoot_cd = max_shoot_cd
        self.bullet_speed = bullet_speed
        self.cd = 0
        self.set_cd = 0
        self.color = color

        i1 = image_1
        i1 = pygame.transform.scale(i1, (28, 21))
        set_color(i1, color)
        self.enemy_image1 = i1
        i2 = image_2
        i2 = pygame.transform.scale(i2, (28, 21))
        set_color(i2, color)
        self.enemy_image2 = i2
        self.enemy_image = i1

    def draw(self, window):
        window.blit(self.enemy_image, (int(self.x), int(self.y)))

    def move(self, move_dir, is_by_wall, vel):
        if self.image_id == 1:
            self.image_id = 2
            self.enemy_image = self.enemy_image2
        else:
            self.image_id = 1
            self.enemy_image = self.enemy_image1
        if is_by_wall:
            self.y += self.height + 10
        elif move_dir == "right":
            self.x += vel
        elif move_dir == "left":
            self.x -= vel
        if self.y + self.height + 3 >= win_height:
            pygame.quit()

    def shoot(self, bullets):
        if self.is_active == True:
            #Initial cd value, so enemies dont shoot at the same interal
            if self.set_cd == 0:
                self.set_cd = 60 + random.randrange(self.min_shoot_cd,
                                                    self.max_shoot_cd)
                self.cd = random.randrange(0, 540)
            self.cd += 1
            if self.cd > self.set_cd:
                new_bullet = RectProjectile(4, 20, self.x + self.width // 2,
                                            self.y + self.height, self.color,
                                            self.bullet_speed, True)
                bullets.append(new_bullet)
                self.cd = 0
                self.set_cd = random.randrange(self.min_shoot_cd,
                                               self.max_shoot_cd)

    def destroy(self):
        print("destroyed", self.score)


class Text:
    def __init__(self, font, color, x, y):

        self.font = font
        self.color = color
        self.x = x
        self.y = y

    def draw(self, window, text):
        text_obj = self.font.render(text, 1, self.color)
        window.blit(text_obj, (self.x, self.y))


class Music:
    def __init__(self):
        self.index = 0

    def check_and_play(self):
        track_sounds[self.index].play()
        self.index += 1
        if self.index > 3:
            self.index = 0


def redraw_game_window():
    win.fill((0, 0, 0))
    player.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    if player_bullet != None:
        player_bullet.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    score_text.draw(win, "Score: " + str(score))
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
        bullet_sound.play()
        player_bullet = RectProjectile(4, 16,
                                       round(player.x + player.width // 2 - 1),
                                       round(player.y - 1), (0, 200, 0), 9,
                                       True)


def handle_enemy_movement_direction():
    check_wall = False
    global direction
    for enemy in enemies:
        if direction == "right" and enemy.x + enemy.width >= win_width:
            direction = "left"
            check_wall = True
        elif direction == "left" and enemy.x <= 0:
            direction = "right"
            check_wall = True


def handle_bullets():
    global player_bullet
    global score
    if player_bullet != None:
        if player_bullet.y > -5:
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
        if player_bullet != None:
            if pygame.Rect(int(player_bullet.x), int(player_bullet.y),
                           player_bullet.width,
                           player_bullet.height).colliderect(
                               pygame.Rect(int(enemy.x), int(enemy.y),
                                           enemy.width, enemy.height)):
                player_bullet = None
                player.can_fire = True
                score += enemy.score
                enemy.destroy()
                enemy_death_sound.play()
                activate_next_enemy(enemy, enemies)
                enemies.pop(enemies.index(enemy))
        enemy.shoot(bullets)
    for bullet in bullets:
        if pygame.Rect(int(bullet.x), int(bullet.y), bullet.width,
                       bullet.height).colliderect(
                           pygame.Rect(int(player.x), int(player.y),
                                       player.width, player.height)):
            run = False


def spawn_enemies(iter: int):
    enemies = []
    #OFFSET X,Y
    x = 100
    y = 32 * iter
    for d in range(1):
        for i in range(11):
            enemies.append(
                Enemy(x + i * 44, y + d * 32 + 8, 32, 24, 30, ORANGE, img_c1,
                      img_c2, False, d, i, 280, 420, 4))
    for d in range(1, 3):
        for i in range(11):
            enemies.append(
                Enemy(x + i * 44, y + d * 32 + 8, 32, 24, 20, PURPLE, img_b1,
                      img_b2, False, d, i, 350, 700, 5))
    for d in range(3, 5):
        for i in range(11):
            enemies.append(
                Enemy(x + i * 44, y + d * 32 + 8, 32, 24, 10,
                      pygame.Color(0, 100, 255), img_a1, img_a2, False, d, i,
                      350, 700, 4))
    for enemy in enemies:
        if enemy.depth == 4:
            enemy.is_active = True
    return enemies


def activate_next_enemy(enemy_out: Enemy, enemies):
    if enemy_out.is_active == True:
        new_max_depth = -1
        new_enemy: Enemy = None
        for enemy in enemies:
            if enemy.row == enemy_out.row and enemy.depth < enemy_out.depth:
                if enemy.depth > new_max_depth:
                    new_max_depth = enemy.depth
                    new_enemy = enemy
        if new_enemy != None:
            new_enemy.is_active = True


#Initialize Game variables
player = Player(win_width // 2 - 45, win_height - 24, 45, 24, 3)
run = True
clock = pygame.time.Clock()
bullets = []
player_bullet = None
direction = "right"
score = 0
iteration = 1
score_text = Text(font, WHITE, 10, 10)
music_loop = Music()

# Gameloop
enemies = spawn_enemies(iteration)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    handle_player_input()
    handle_enemy_movement_direction()
    handle_bullets()
    if not enemies:
        iteration += 1
        enemies = spawn_enemies(iteration)

    redraw_game_window()
    clock.tick(60)
pygame.quit()
