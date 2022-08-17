from math import ceil
import pygame as pg
import sys
import random

#####################################  VARIABLES AND CONSTANTS AND FUNCTIONS #####################################
pg.init()
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
tf = 0
t_r = None
last_fire_time = -1
game_score = 0

def lsr_move(lsr_list, speed = 200):
    for lsr in lsr_list:
        lsr.centery -= ceil(speed*dt)
        
        if(lsr.bottom < 0):
            lsr_list.remove(lsr)

def get_time_since_start(tf, t_r):
    if(tf != 0):
        pg.draw.rect(bg_surf, color=(42,45,51), rect=t_r, width=8, border_radius=5)

    time_txt = f"Score: {game_score}"
    txt_surf = font1.render(time_txt, True, (255, 255, 255))
    txt_rect = txt_surf.get_rect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 30))
    display_surface.blit(txt_surf, txt_rect)
    return(pg.draw.rect(bg_surf, color='white', rect=txt_rect.inflate(50, 50), width=8, border_radius=5))

def mtr_move(mtr_list, speed = 180):
    for (mtr, dir) in mtr_list:
        
        mtr.center += (dir*speed*dt)
        
        if(mtr.top > WINDOW_HEIGHT):
            mtr_list.remove((mtr, dir))

############################################  COLLISIONS  ##############################################
# Detect collisions/overlaps between 2 rects (rects containing objects are checked). --> IN THIS FILE.
# Check if a point lies inside a rect.
# Check how close 2 objects are to each other (usually for round objects).
# Pixel-Perfect Collisions. (Every pixel inside each surface is checked to see if any overlap is there). (MORE PRECISE/COSTLY).
#########################################################################################################

#############################################  CREATE A WINDOW  #########################################
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

# Import sounds.
lsr_sound = pg.mixer.Sound('./sounds/laser.ogg')
blast_sound = pg.mixer.Sound('./sounds/explosion.wav')
bg_music = pg.mixer.Sound('./sounds/music.wav')

bg_music.play(loops = -1)  # loop bg_music forever.

while(True):
    # 1.) Inputs (event loop).
    for event in pg.event.get():
        if(event.type == pg.QUIT):
            pg.quit()
            print("Game Closed!")
            print(f"Final Score: {game_score}")
            sys.exit()

        if(event.type == pg.MOUSEBUTTONDOWN):
            # Applying timer logic to limit how fast (once every half second) lasers can be shot,
            if(pg.time.get_ticks() - last_fire_time >= 400):
                laser_rect = laser_surf.get_rect(midbottom=ship_rect.center)
                lsr_sound.play()  # Play lsr_sound.
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

    # Check for collisions between meteors and ship.
    for (mtr, dir) in meteor_list:
        is_colliding = ship_rect.colliderect(mtr)  # boolean.
        # Game over on collision.
        if(is_colliding):
            pg.quit()
            print("Game Over!")
            print(f"Final Score: {game_score}")
            sys.exit()

    # Check for collisions between lasers and meteors.
    for (mtr, dir) in meteor_list:
        for lsr in lasers:
            is_blast = lsr.colliderect(mtr)  # boolean.
            if(is_blast):
                blast_sound.play()  # Play blast_sound.
                lasers.remove(lsr)
                meteor_list.remove((mtr, dir))
                game_score += 1



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
