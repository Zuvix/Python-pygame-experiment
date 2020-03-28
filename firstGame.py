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
big_font = pygame.font.Font(os.path.join("assets", "fonts", 'unifont.ttf'), 64)
pygame.display.set_caption("Pygame: Space Invaders")
icon = pygame.image.load(os.path.join('assets', 'images', 'icon.png'))
pygame.display.set_icon(icon)

#Load Sound Assets
bullet_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'shoot.wav'))

##enemy sounds
enemy_laser_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'enemy_laser.wav'))
enemy_death_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'invaderkilled.wav'))
spawn_sound = pygame.mixer.Sound(os.path.join('assets', 'nSounds',
                                              'spawn.wav'))
##ufo sounds
ufo_sound = pygame.mixer.Sound(os.path.join('assets', 'nSounds', 'ufo.wav'))
ufo_kill_sounds = []
for i in range(1, 4):
    ufo_kill_sounds.append(
        pygame.mixer.Sound(
            os.path.join('assets', 'nSounds', 'ufo_kill' + str(i) + '.wav')))

##background music during gamerun
track_sounds = []
for i in range(1, 5):
    track_sounds.append(
        pygame.mixer.Sound(
            os.path.join('assets', 'nSounds',
                         'fastinvader' + str(i) + '.wav')))
    track_sounds[i - 1].set_volume(0.4)

##menu sounds
menu_music = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'menusong.ogg'))
start_game_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'start_game.wav'))
enemy_laser_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'enemy_laser.wav'))

##gamover sounds
explosion_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'explosion.wav'))
gameover_sound = pygame.mixer.Sound(
    os.path.join('assets', 'nSounds', 'game_over.ogg'))
end_music = pygame.mixer.Sound(os.path.join('assets', 'nSounds',
                                            'endsong.ogg'))

#Set volume for sounds
bullet_sound.set_volume(0.4)
enemy_death_sound.set_volume(0.15)
spawn_sound.set_volume(0.5)
ufo_sound.set_volume(0.3)
enemy_laser_sound.set_volume(0.4)

#Load Images
img_title = pygame.image.load(os.path.join('assets', 'images', 'title.png'))
img_p = pygame.image.load(os.path.join('assets', 'images', 'Ship.png'))
img_a1 = pygame.image.load(os.path.join('assets', 'images', 'InvaderA1.png'))
img_a2 = pygame.image.load(os.path.join('assets', 'images', 'InvaderA2.png'))
img_b1 = pygame.image.load(os.path.join('assets', 'images', 'InvaderB2.png'))
img_b2 = pygame.image.load(os.path.join('assets', 'images', 'InvaderB1.png'))
img_c1 = pygame.image.load(os.path.join('assets', 'images', 'InvaderC1.png'))
img_c2 = pygame.image.load(os.path.join('assets', 'images', 'InvaderC2.png'))
img_ufo = pygame.image.load(os.path.join('assets', 'images', 'ufo.png'))

#Define Colors
ORANGE = pygame.Color(255, 100, 0)
GREEN = pygame.Color(78, 255, 87)
YELLOW = pygame.Color(241, 255, 0)
BLUE = pygame.Color(0, 100, 255)
PURPLE = pygame.Color(203, 0, 255)
RED = pygame.Color(237, 28, 36)
WHITE = pygame.Color(255, 255, 255)


#function used to set color of surface
def set_color(img, color):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color.a = img.get_at((x, y)).a  # Preserve the alpha value.
            img.set_at((x, y), color)  # Set the color of the pixel.


#set colors for invaders
set_color(img_a1, BLUE)
set_color(img_a2, BLUE)
set_color(img_b1, PURPLE)
set_color(img_b2, PURPLE)
set_color(img_c1, ORANGE)
set_color(img_c2, ORANGE)


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


#basic bullet used by enemies and player
class RectProjectile(Projectile):
    def __init__(self, width, height, *args):
        self.width = width
        self.height = height
        super().__init__(*args)

    def draw(self, window):
        self.horiznotal_move()
        pygame.draw.rect(window, self.color,
                         (int(self.x), int(self.y), self.width, self.height))


#player class for the ship object
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


#class for all enemies in spaceinvaders excluding ufo
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

        #scale and set color of default img
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
            destroy_player()

    def change_anim(self):
        if self.image_id == 1:
            self.image_id = 2
            self.enemy_image = self.enemy_image2
        else:
            self.image_id = 1
            self.enemy_image = self.enemy_image1

    def shoot(self, bullets):
        if self.is_active == True and self.y < win_height - 50:
            #Here we set initial cd value, so enemies dont shoot at the same interal
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
                pygame.mixer.find_channel().play(enemy_laser_sound)
                self.cd = 0
                self.set_cd = random.randrange(self.min_shoot_cd,
                                               self.max_shoot_cd)


#class for ufo objects
class Ufo:
    def __init__(self, x, y, width, height, vel, img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.img = img

    def move(self):
        self.x += self.vel

    def draw(self, window):
        window.blit(self.img, (int(self.x), int(self.y)))


#general class for text objects
class Text:
    def __init__(self, font, color, x, y):

        self.font = font
        self.color = color
        self.x = x
        self.y = y

    def draw(self, window, text):
        text_obj = self.font.render(text, 1, self.color)
        window.blit(text_obj, (self.x, self.y))


#class for looping music
class Music:
    def __init__(self):
        self.index = 0

    def check_and_play(self):
        pygame.mixer.find_channel().play(track_sounds[self.index])
        self.index += 1
        if self.index > 3:
            self.index = 0


class Stats:
    def __init__(self):
        self.a_killed = 0
        self.b_killed = 0
        self.c_killed = 0
        self.ufo_killed = 0
        self.ufo_colledted_points = 0


#redraw all existing gameobjects
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


#handle player controlls and shooting
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


#check if enemies are by wall and should change direction
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


#handle bullet collisions
def handle_bullets():
    global player_bullet
    global score
    global game_speed
    global run
    global stats

    #move player bullet
    if player_bullet != None:
        if player_bullet.y > -5:
            player_bullet.y -= player_bullet.vel
        else:
            player_bullet = None
            player.can_fire = True

    #bullets out of bounds
    for bullet in bullets:
        if bullet.y < win_height:
            bullet.y += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    #collisions with enemies
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
                pygame.mixer.find_channel().play(enemy_death_sound)
                game_speed -= 2
                activate_next_enemy(enemy, enemies)
                if enemy.score == 10:
                    stats.a_killed += 1
                if enemy.score == 20:
                    stats.b_killed += 1
                if enemy.score == 30:
                    stats.c_killed += 1
                enemies.pop(enemies.index(enemy))
        enemy.shoot(bullets)

    #collision with player
    for bullet in bullets:
        if pygame.Rect(int(bullet.x), int(bullet.y), bullet.width,
                       bullet.height).colliderect(
                           pygame.Rect(int(player.x), int(player.y),
                                       player.width, player.height)):
            bullets.pop(bullets.index(bullet))
            destroy_player()


#spawn enemies in waves
def spawn_enemies(iter):
    global enemies
    spawn_sound.play(-1)
    #OFFSET X,Y
    x = 130
    y = 34 + 36 * iter
    #spawn upper row
    for d in range(1):
        for i in range(11):
            enemies.append(
                Enemy(x + i * 48, y + d * 32 + 8, 32, 24, 30, ORANGE, img_c1,
                      img_c2, False, d, i, 250, 420, 4))
            clock.tick(20)
            redraw_game_window()
    #spawn middle rows
    for d in range(1, 3):
        for i in range(11):
            enemies.append(
                Enemy(x + i * 48, y + d * 32 + 8, 32, 24, 20, PURPLE, img_b1,
                      img_b2, False, d, i, 350, 700, 6))
            clock.tick(20)
            redraw_game_window()
    #spawn lower rows
    for d in range(3, 5):
        for i in range(11):
            enemies.append(
                Enemy(x + i * 48, y + d * 32 + 8, 32, 24, 10,
                      pygame.Color(0, 100, 255), img_a1, img_a2, False, d, i,
                      350, 700, 4))
            clock.tick(20)
            redraw_game_window()
    for enemy in enemies:
        if enemy.depth == 4:
            enemy.is_active = True
    spawn_sound.stop()
    clock.tick(3)


#when one enemy dies he enebles the enemy above him to shoot
def activate_next_enemy(enemy_out, enemies):
    if enemy_out.is_active == True:
        new_max_depth = -1
        new_enemy = None
        for enemy in enemies:
            if enemy.row == enemy_out.row and enemy.depth < enemy_out.depth:
                if enemy.depth > new_max_depth:
                    new_max_depth = enemy.depth
                    new_enemy = enemy
        if new_enemy != None:
            new_enemy.is_active = True


#move enemies depending on the speed of the game
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


# create ufo object and change music
def spawn_ufo():
    global ufo
    global music_muted
    music_muted = True
    pygame.mixer.find_channel().play(ufo_sound, loops=100)
    ufo = Ufo(0, 40, 50, 22, 1.75, img_ufo)


#control ufo behaviour and spawntime
def handle_ufo():
    global ufo
    global player_bullet
    global player
    global score
    global music_muted
    global player_shot_count
    global stats
    if ufo == None:
        if ufo_milestone == player_shot_count and len(enemies) > 4:
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
                stats.ufo_killed += 1
                player_bullet = None
                player.can_fire = True
                possible_scores = (50, 100, 150)
                random_num = random.randrange(0, 3)
                score += possible_scores[random_num]
                stats.ufo_colledted_points += possible_scores[random_num]
                pygame.mixer.find_channel().play(ufo_kill_sounds[random_num])


#destroys ufo and resets original music
def destroy_ufo():
    global ufo
    global music_muted
    ufo = None
    ufo_sound.stop()
    music_muted = False


def redraw_menu():
    global state
    win.fill((0, 0, 0))
    intro_text = Text(font, WHITE, 272, win_height - 60)
    controls_text = Text(font, WHITE, 220, win_height - 130)
    shoot_text = Text(font, WHITE, 460, win_height - 130)
    value1_text = Text(font, BLUE, 262, 280)
    value2_text = Text(font, ORANGE, 492, 280)
    value3_text = Text(font, PURPLE, 262, 400)
    value4_text = Text(font, RED, 492, 400)
    if state == 1:
        state = 0
        intro_text.color = GREEN
        win.blit(img_a1, (250, 240))
        win.blit(img_b1, (250, 360))
        win.blit(img_c1, (480, 240))
        win.blit(img_ufo, (480, 365))
    else:
        state = 1
        intro_text.color = WHITE
        win.blit(img_a2, (250, 240))
        win.blit(img_b2, (250, 360))
        win.blit(img_c2, (480, 240))
        win.blit(img_ufo, (480, 365))
    controls_text.draw(win, "Move: Arrows")
    shoot_text.draw(win, "Shoot: Space")
    value1_text.draw(win, "10p")
    value2_text.draw(win, "30p")
    value3_text.draw(win, "20p")
    value4_text.draw(win, "???")
    intro_text.draw(win, "Hold Space to start the race!")
    win.blit(img_title, (206, 30))
    pygame.display.update()


def change_event(next_event):
    global current_event
    global score
    global enemies
    global state
    global player_bullet
    global bullets
    global iteration
    if next_event == "menu":
        end_music.stop()
        menu_music.play(-1)
        score = 0
        iteration = 0
        bullets = []
        current_event = "menu"
    if next_event == "game":
        current_event = "game"
        menu_music.stop()
        start_game_sound.play()
        clock.tick(1)
    if next_event == "end":
        state = 0
        current_event = "end"
        enemies = []
        pygame.mixer.find_channel().play(gameover_sound)
        end_music.play(-1)


def show_number(number, desired_units, fill_chareacter):
    current_units = len(str(number))
    needed_units = desired_units - current_units
    if needed_units > 0:
        return needed_units * fill_chareacter + str(number)
    else:
        return number


def destroy_player():
    global player_bullet
    player_bullet = None
    player.can_fire = True
    pygame.mixer.find_channel().play(explosion_sound)
    clock.tick(1)
    player_bullet
    change_event("end")


def redraw_end_screen():
    global state
    img_end_a1 = pygame.transform.scale(img_a1, (28, 21))
    img_end_b1 = pygame.transform.scale(img_b1, (28, 21))
    img_end_c1 = pygame.transform.scale(img_c1, (28, 21))
    gameover_text = Text(big_font, WHITE, 250, 20)
    kills_text = Text(font, WHITE, 292, 90 + 60 * state)
    equal_text = Text(font, WHITE, 360 + 60, 90 + 60 * state)
    value_text = Text(font, WHITE, 385 + 60, 90 + 60 * state)
    final_text = Text(font, WHITE, 290, 390)
    final_score = Text(font, WHITE, 421, 390)
    goodbye_text = Text(font, BLUE, 515, win_height - 40)
    restart_text = Text(font, YELLOW, 50, win_height - 40)

    if state == 0:
        win.fill((0, 0, 0))
        gameover_text.draw(win, "Game Over")
    if state == 1:
        win.blit(img_end_a1, (365, 150))
        kills_text.draw(win, show_number(stats.a_killed, 3, "0") + "  x")
        equal_text.draw(win, "=")
        value_text.draw(win, show_number(stats.a_killed * 10, 5, "0"))
    if state == 2:
        kills_text.draw(win, show_number(stats.b_killed, 3, "0") + "  x")
        win.blit(img_end_b1, (365, 210))
        equal_text.draw(win, "=")
        value_text.draw(win, show_number(stats.b_killed * 20, 5, "0"))
    if state == 3:
        kills_text.draw(win, show_number(stats.c_killed, 3, "0") + "  x")
        win.blit(img_end_c1, (365, 270))
        equal_text.draw(win, "=")
        value_text.draw(win, show_number(stats.c_killed * 30, 5, "0"))
    if state == 4:
        kills_text.color = RED
        equal_text.color = RED
        value_text.color = RED
        kills_text.draw(win, show_number(stats.ufo_killed, 3, "0") + "  x")
        win.blit(img_ufo, (355, 325))
        equal_text.draw(win, "=")
        value_text.draw(win, show_number(stats.ufo_colledted_points, 5, "0"))
    if state == 5:
        pygame.draw.rect(win, WHITE, (280, 370, 220, 1))
    if state == 6:
        final_text.draw(win, "Total:")
        final_score.draw(win, show_number(score, 8, " "))
    if state == 8:
        goodbye_text.draw(win, "Better luck in another galaxy.")
        restart_text.draw(win, "Hold R to return Home!")
    state += 1
    pygame.display.update()


#initialize game variables
player = Player(win_width // 2 - 45, win_height - 24, 45, 24, 3)
clock = pygame.time.Clock()

#bullets
player_bullet = None
bullets = []

#enemies
enemies = []
direction = "right"
enemy_move_cycle = 0

#game-menu-end control
current_event = "end"
run = True

#game
current_time = 80
game_speed = 130

#menu
state = 0

#score and wave
score = 0
iteration = 0
score_text = Text(font, WHITE, 12, 12)
level_text = Text(font, WHITE, 360, 12)

#main music theme
music_loop = Music()
music_muted = False

#stats
stats = Stats()

#ufo event
ufo = None
player_shot_count = 0
ufo_milestone = 0

# Gameloop
change_event("menu")
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if current_event == "menu":
        redraw_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            change_event("game")
        clock.tick(4)
    if current_event == "game":
        if not enemies:
            iteration += 1
            spawn_enemies(iteration)
            current_time = 80
            enemy_move_cycle = 1
            game_speed = 130
            direction = "right"
            player_shot_count = 0
            ufo_milestone = random.randrange(20, 30)
        if (enemies):
            handle_player_input()
            move_enemies()
            handle_bullets()
            handle_ufo()
        redraw_game_window()
        clock.tick(60)
    if current_event == "end":
        redraw_end_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            change_event("menu")
        clock.tick(2)
pygame.quit()
