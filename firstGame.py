import pygame

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")

vel = 5
run = True
x = 50
y = 50
clock = pygame.time.Clock()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_DOWN]:
        y += vel
    if keys[pygame.K_UP]:
        y -= vel
    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 0, 0), (x, y, 40, 60))
    pygame.display.update()
    win.fill((0))
    clock.tick(60)

pygame.quit()
