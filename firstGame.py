import pygame
import os
import random

# Display and enviroment init section
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mixer.pre_init(44100, -16, 300, 2048)
pygame.init()
win_height = 600
win_width = 800
win = pygame.display.set_mode((win_width, win_height))
font = pygame.font.Font(os.path.join("assets", "fonts", 'unifont.ttf'), 16)
pygame.display.set_caption("Space Invaders by Zuvix")
icon = pygame.image.load(os.path.join('assets', 'images', 'icon.png'))
pygame.display.set_icon(icon)

#Load Sound Assets
bullet_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'shoot.wav'))
enemy_death_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'invaderkilled.wav'))
spawn_sound = pygame.mixer.Sound(os.path.join('assets', 'nSounds',
                                              'spawn.wav'))
ufo_sound = pygame.mixer.Sound(os.path.join('assets', 'nSounds', 'ufo.wav'))
ufo_kill_sounds = []
for i in range(1, 4):
    ufo_kill_sounds.append(
        pygame.mixer.Sound(
            os.path.join('assets', 'nSounds', 'ufo_kill' + str(i) + '.wav')))
track_sounds = []
for i in range(1, 5):
    track_sounds.append(
        pygame.mixer.Sound(
            os.path.join('assets', 'nSounds',
                         'fastinvader' + str(i) + '.wav')))
    track_sounds[i - 1].set_volume(0.5)

#Set volume for sounds
bullet_sound.set_volume(0.6)
enemy_death_sound.set_volume(0.2)
spawn_sound.set_volume(0.5)
ufo_sound.set_volume(0.3)

#Load Images
img_p = pygame.image.load(os.path.join('assets', 'images', 'Ship.png'))
img_a1 = pygame.image.load(os.path.join('assets', 'images', 'InvaderA1.png'))
img_a2 = pygame.image.load(os.path.join('assets', 'images', 'InvaderA2.png'))
img_b1 = pygame.image.load(os.path.join('assets', 'images', 'InvaderB1.png'))
img_b2 = pygame.image.load(os.path.join('assets', 'images', 'InvaderB2.png'))
img_c1 = pygame.image.load(os.path.join('assets', 'images', 'InvaderC1.png'))
img_c2 = pygame.image.load(os.path.join('assets', 'images', 'InvaderC2.png'))
img_ufo = pygame.image.load(os.path.join('assets', 'images', 'ufo.png'))

#Define Colors
ORANGE = pygame.Color(255, 100, 0)
GREEN = pygame.Color(78, 255, 87)
YELLOW = pygame.Color(241, 255, 0)
BLUE = pygame.Color(0, 150, 240)
PURPLE = pygame.Color(203, 0, 255)
RED = pygame.Color(237, 28, 36)
WHITE = pygame.Color(255, 255, 255)


#function used to set color of surface
def set_color(img, color):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color.a = img.get_at((x, y)).a  # Preserve the alpha value.
            img.set_at((x, y), color)  # Set the color of the pixel.


#class for all bullets
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

    #function used to make bullets look less static
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


#Maybe used sometime for a boss type event
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
        if is_by_wall:
            self.y += self.height + 12
        elif move_dir == "right":
            self.x += vel
        elif move_dir == "left":
            self.x -= vel
        if self.y + self.height + 3 >= win_height:
            pygame.quit()

    def change_anim(self):
        if self.image_id == 1:
            self.image_id = 2
            self.enemy_image = self.enemy_image2
        else:
            self.image_id = 1
            self.enemy_image = self.enemy_image1

    def shoot(self, bullets):
        if self.is_active == True:
            #Initial cd value, so enemies dont shoot at the same interal
            if self.set_cd == 0:
                self.set_cd = 60 + random.randrange(self.min_shoot_cd,
                                                    self.max_shoot_cd)
                self.cd = random.randrange(0, self.set_cd - 30)
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


class Ufo:
    def __init__(self, x, y, width, height, vel, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.img = pygame.transform.scale(img, (50, 22))

    def move(self):
        self.x += self.vel

    def draw(self, window):
        window.blit(self.img, (int(self.x), int(self.y)))


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
        pygame.mixer.find_channel().play(track_sounds[self.index])
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
    if ufo:
        ufo.draw(win)
    score_text.draw(win, "Score: " + str(score))
    level_text.draw(win, "Wave: " + str(iteration))
    pygame.display.update()


def handle_player_input():
    global player_bullet
    global player_shot_count
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.vel
    if keys[pygame.K_RIGHT] and player.x < win_width - player.width:
        player.x += player.vel
    if keys[pygame.K_SPACE] and player.can_fire:
        player.can_fire = False
        player_shot_count += 1
        pygame.mixer.find_channel().play(bullet_sound)
        player_bullet = RectProjectile(4, 16,
                                       round(player.x + player.width // 2 - 1),
                                       round(player.y - 1), (0, 200, 0), 9,
                                       True)


def handle_enemy_movement_direction():
    check_wall = False
    global direction
    for enemy in enemies:
        if direction == "right" and enemy.x + 2 * enemy.width >= win_width:
            direction = "left"
            check_wall = True
        elif direction == "left" and enemy.x - enemy.width <= 0:
            direction = "right"
            check_wall = True
    return check_wall


def handle_bullets():
    global player_bullet
    global score
    global game_speed
    global run
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
                pygame.mixer.find_channel().play(enemy_death_sound)
                game_speed -= 2
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
    global enemies
    #OFFSET X,Y
    spawn_sound.play(-1)
    x = 150
    y = 34 + 36 * iter
    for d in range(1):
        for i in range(11):
            enemies.append(
                Enemy(x + i * 44, y + d * 32 + 8, 32, 24, 30, ORANGE, img_c1,
                      img_c2, False, d, i, 250, 420, 4))
            clock.tick(20)
            redraw_game_window()
    for d in range(1, 3):
        for i in range(11):
            enemies.append(
                Enemy(x + i * 44, y + d * 32 + 8, 32, 24, 20, PURPLE, img_b1,
                      img_b2, False, d, i, 350, 700, 6))
            clock.tick(20)
            redraw_game_window()
    for d in range(3, 5):
        for i in range(11):
            enemies.append(
                Enemy(x + i * 44, y + d * 32 + 8, 32, 24, 10,
                      pygame.Color(0, 100, 255), img_a1, img_a2, False, d, i,
                      350, 700, 4))
            clock.tick(20)
            redraw_game_window()
    for enemy in enemies:
        if enemy.depth == 4:
            enemy.is_active = True
    spawn_sound.stop()


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


def move_enemies():
    global current_time
    global enemy_move_cycle
    global game_speed
    current_time += 2
    vel = 8
    if len(enemies) == 1:
        game_speed = 16
        if current_time == 4 or current_time == 12:
            by_wall = handle_enemy_movement_direction()
            for enemy in enemies:
                enemy.move(direction, by_wall, vel)
    if current_time >= game_speed:
        current_time = 0
        if not music_muted:
            music_loop.check_and_play()
        by_wall = handle_enemy_movement_direction()
        for enemy in enemies:
            enemy.move(direction, by_wall, vel)
            enemy.change_anim()
            enemy_move_cycle = 0
    if current_time >= game_speed / 2 and enemy_move_cycle == 0:
        enemy_move_cycle = 1
        by_wall = handle_enemy_movement_direction()
        for enemy in enemies:
            enemy.move(direction, by_wall, vel)


def spawn_ufo():
    global ufo
    global win
    global music_muted
    music_muted = True
    pygame.mixer.find_channel().play(ufo_sound, loops=100)
    ufo = Ufo(0, 40, 50, 22, 1.75, img_ufo)


def handle_ufo():
    global ufo
    global player_bullet
    global player
    global score
    global music_muted
    global player_shot_count
    if ufo == None:
        if ufo_milestone == player_shot_count:
            spawn_ufo()
            player_shot_count = 0
            ufo_milestione = random.randrange(12, 25)
    else:
        ufo.move()
        if ufo.x > win_width:
            destroy_ufo()

        elif not player_bullet == None:
            if pygame.Rect(int(player_bullet.x), int(player_bullet.y),
                           player_bullet.width,
                           player_bullet.height).colliderect(
                               pygame.Rect(int(ufo.x), int(ufo.y), ufo.width,
                                           ufo.height)):
                destroy_ufo()
                player_bullet = None
                player.can_fire = True
                possible_scores = (50, 100, 150)
                random_num = random.randrange(0, 3)
                score += possible_scores[random_num]
                pygame.mixer.find_channel().play(ufo_kill_sounds[random_num])


def destroy_ufo():
    global ufo
    global music_muted
    ufo = None
    ufo_sound.stop()
    music_muted = False


#Initialize Game variables
player = Player(win_width // 2 - 45, win_height - 24, 45, 24, 3)
run = True
clock = pygame.time.Clock()
bullets = []
player_bullet = None
direction = "right"
score = 0
current_time = 80
enemy_move_cycle = 0
game_speed = 130
iteration = 0
score_text = Text(font, WHITE, 12, 12)
level_text = Text(font, WHITE, 360, 12)
music_loop = Music()
music_muted = False
ufo = None
player_shot_count = 0
ufo_milestone = 0
# Gameloop
enemies = []
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if not enemies:
        iteration += 1
        spawn_enemies(iteration)
        current_time = 80
        enemy_move_cycle = 1
        game_speed = 130
        direction = "right"
        random_shot_count = 0
        ufo_milestone = random.randrange(20, 30)
    if (enemies):
        handle_player_input()
        move_enemies()
        handle_bullets()
        handle_ufo()
    redraw_game_window()
    clock.tick(60)
pygame.quit()
