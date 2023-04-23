import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle of the Gays")

WHITE = (255,255,255)
PINK = (159, 43, 104)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (255, 255, 0)
FPS = 60
SPRITE_HEIGHT, SPRITE_WIDTH = 70,99
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans',30)
WINNER_FONT = pygame.font.SysFont('helvetica',60)


G_HIT = pygame.USEREVENT + 1
E_HIT = pygame.USEREVENT + 2

BOARDER = pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT)
BACKGROUND_IMG = pygame.image.load(
    os.path.join("Assets","space.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND_IMG,(WIDTH,HEIGHT))
ELLIOT_IMG = pygame.image.load(
    os.path.join("Assets","Elliot_Sprite.png"))
ELLIOT = pygame.transform.scale(ELLIOT_IMG,(SPRITE_HEIGHT,SPRITE_WIDTH))
GEORGE_IMG = pygame.image.load(
    os.path.join('Assets', 'George_Sprite.png'))
GEORGE = pygame.transform.scale(GEORGE_IMG,(SPRITE_HEIGHT,SPRITE_WIDTH))

# CREATE THE WINDOW
    # FILL = pink background | BLIT = draw the sprite
def draw_window(g,e, g_bullets, e_bullets, g_lives, e_lives):
    WINDOW.blit(BACKGROUND, (0, 0))
    g_lives_text = HEALTH_FONT.render("Lives: " + str(g_lives),1,WHITE)
    e_lives_text = HEALTH_FONT.render("Lives: " + str(e_lives),1,WHITE)

    WINDOW.blit(g_lives_text,(WIDTH - g_lives_text.get_width() - 10, 10))
    WINDOW.blit(e_lives_text,(10, 10))
    WINDOW.blit(GEORGE, (g.x, g.y))
    WINDOW.blit(ELLIOT, (e.x, e.y))
    pygame.draw.rect(WINDOW,BLACK, BOARDER )

    for bullet in g_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    for bullet in e_bullets:
        pygame.draw.rect(WINDOW, GREEN, bullet)

    pygame.display.update()


def george_movement(keys_pressed, g):
    if keys_pressed[pygame.K_a] and g.x -VEL > 0:  # LEFT
        g.x -= VEL
    if keys_pressed[pygame.K_d] and g.x +VEL +g.width < BOARDER.x: # RIGHT
        g.x += VEL
    if keys_pressed[pygame.K_w] and g.y -VEL >0: # UP
        g.y -= VEL
    if keys_pressed[pygame.K_s] and g.y + VEL + g.height < HEIGHT -20: # DOWN
        g.y += VEL

def elliot_movement(keys_pressed, e):
    if keys_pressed[pygame.K_LEFT] and e.x - VEL > BOARDER.x+30: # LEFT
        e.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and e.x + VEL + 10 < WIDTH-SPRITE_WIDTH/2: # RIGHT
        e.x += VEL
    if keys_pressed[pygame.K_UP] and e.y -VEL >0: # UP
        e.y -= VEL
    if keys_pressed[pygame.K_DOWN] and e.y + VEL + e.height < HEIGHT -20: # DOWN
        e.y += VEL


def handle_bullets(g_bullets, e_bullets, g, e):
    for bullet in g_bullets:
        bullet.x += BULLET_VEL
        if e.colliderect(bullet):
            pygame.event.post(pygame.event.Event(G_HIT))
            g_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            g_bullets.remove(bullet)
        

    for bullet in e_bullets:
        bullet.x -= BULLET_VEL
        if g.colliderect(bullet):
            pygame.event.post(pygame.event.Event(E_HIT))
            e_bullets.remove(bullet)
        elif bullet.x < 0:
            e_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WINDOW.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

# Main Game Running - Checking for events
def main():
    g = pygame.Rect(100,300, SPRITE_WIDTH,SPRITE_HEIGHT)
    e = pygame.Rect(700,300, SPRITE_WIDTH,SPRITE_HEIGHT)

    g_bullets = []
    e_bullets = []
    g_lives = 10
    e_lives = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(g_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(g.x + g.width, g.y + g.height//2 -2, 10,5)
                    g_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(e_bullets) <MAX_BULLETS:
                    bullet = pygame.Rect(e.x, e.y + e.height//2 -2, 10,5)
                    e_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == E_HIT:
                e_lives -= 1
                BULLET_HIT_SOUND.play()
            if event.type == G_HIT:
                g_lives -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if g_lives <= 0:
            winner_text = 'George Wins!!!'
        if e_lives <= 0:
            winner_text = 'Elliot Wins!!!'
        if winner_text != "":
            draw_winner(winner_text)
            break
        print(e_lives, g_lives)
        print(g_bullets, e_bullets)
        keys_pressed = pygame.key.get_pressed()
        george_movement(keys_pressed,g)
        elliot_movement(keys_pressed,e)

        handle_bullets(g_bullets, e_bullets, g, e)

        
        draw_window(g,e, g_bullets, e_bullets, g_lives, e_lives)
    main()


if __name__ == "__main__":
    main()