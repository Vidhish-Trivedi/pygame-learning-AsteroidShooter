from math import ceil
import pygame as pg
import sys
import random

#####################################  VARIABLES AND CONSTANTS AND FUNCTIONS #####################################
pg.init()  # Initialise pygame.
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
tf = 0
t_r = None
last_fire_time = -1

def lsr_move(lsr_list, speed = 200):
    for lsr in lsr_list:
        lsr.centery -= ceil(speed*dt)
        # Optimization. (Remove lasers which are outside the screen).
        if(lsr.bottom < 0):
            lsr_list.remove(lsr)

def get_time_since_start(tf, t_r):
    if(tf != 0):
        pg.draw.rect(bg_surf, color=(42,45,51), rect=t_r, width=8, border_radius=5)

    time_txt = f"Score: {pg.time.get_ticks()//1000}"
    txt_surf = font1.render(time_txt, True, (255, 255, 255))  # AntiAlias (bool) : smooth out edges of font.
    txt_rect = txt_surf.get_rect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 30))
    display_surface.blit(txt_surf, txt_rect)
    return(pg.draw.rect(bg_surf, color='white', rect=txt_rect.inflate(50, 50), width=8, border_radius=5))

def mtr_move(mtr_list, speed = 180):
    for (mtr, dir) in mtr_list:
        # mtr.centery += ceil(speed*dt)
        mtr.center += (dir*speed*dt)
        # Optimization. (Remove meteors which are outside the screen).
        if(mtr.top > WINDOW_HEIGHT):
            mtr_list.remove((mtr, dir))

#######################################  VECTOR2  #########################################
# vector2 can be thought of as a (2 x 1) matrix --> like a tuple of (x, y).
# 5 * (x, y) = (5x, 5y); 4.3 * (x, y) = (4.3x, 4.3y)
# Let rect.center = (30, 19), then, rect.center + (10, 17) moves rect.center to (40, 36).
# Hence, we may use: rect.center += direction * speed * DT. (direction --> vector2).
# Moving any point of a rect moves all points of that rect relative to the one being moved.

###########################################################################################

#####################################  CREATE A WINDOW  #################################
# Set up a window.
display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Asteroid Shooter")  # Set title of window.
    
# Ship.
ship_surf = pg.image.load('./graphics/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

# BG surface.
bg_surf = pg.image.load('./graphics/background.png').convert()

# Laser.
lasers = []  # To maintain all lasers.
laser_surf = pg.image.load('./graphics/laser.png').convert_alpha()

# Creating text.
font1 = pg.font.Font('./graphics/subatomic.ttf', 40)

# Meteors.
meteor_timer = pg.event.custom_type()  # custom event (recurring timer).
pg.time.set_timer(meteor_timer, 1000)  # pygame calls this method every 500 milliseconds ==> gives event of custom_type as set above.

meteor_list = []
meteor_surf = pg.image.load('./graphics/meteor.png').convert_alpha()

# Set up a clock.
clk = pg.time.Clock()

while(True):
    # 1.) Inputs (event loop).
    for event in pg.event.get():
        if(event.type == pg.QUIT):
            pg.quit()
            print("Game Closed!")
            sys.exit()

        if(event.type == pg.MOUSEBUTTONDOWN):
            # Applying timer logic to limit how fast (once every half second) lasers can be shot,
            if(pg.time.get_ticks() - last_fire_time >= 400):
                laser_rect = laser_surf.get_rect(midbottom=ship_rect.center)
                lasers.append(laser_rect)
                last_fire_time = pg.time.get_ticks()

        if(event.type == meteor_timer):
            x_cor = random.randint(meteor_surf.get_width() + 5, WINDOW_WIDTH - meteor_surf.get_width() - 5)
            y_cor = random.randint(-100, -50)  # So that meteors would be differently spaced.
            
            direction = pg.math.Vector2(random.uniform(-0.5, 0.5), 1)
            
            meteor_rect = meteor_surf.get_rect(midbottom=(x_cor, y_cor))
            meteor_list.append((meteor_rect, direction))

    # Get delta time.
    dt = clk.tick(120)/1000  # in milliseconds.

    # Mouse Input.
    ship_rect.center = pg.mouse.get_pos()
    
    # Applying delta time concept for movement.
    lsr_move(lasers)
    mtr_move(meteor_list)

    # 2.) Update elements.
    display_surface.fill("black")
    display_surface.blit(bg_surf, (0, 0))
    
    # Using some temporary variables to display updated values such as time or score,
    # This will help in removing/hiding older rectangles which were drawn.
    t_r = get_time_since_start(tf, t_r)
    tf += 1
    
    # Display meteors.
    for (mtr, dir) in meteor_list:
        display_surface.blit(meteor_surf, mtr)

    # Display lasers.
    for lsr in lasers:
        display_surface.blit(laser_surf, lsr)
    
    display_surface.blit(ship_surf, ship_rect)

    # 3.) Show display_surface as a final frame.
    pg.display.update()
