from math import ceil
import pygame as pg
import sys

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
            lasers.remove(lsr)

def get_time_since_start(tf, t_r):
    if(tf != 0):
        pg.draw.rect(bg_surf, color=(42,45,51), rect=t_r, width=8, border_radius=5)

    time_txt = f"Score: {pg.time.get_ticks()//1000}"
    txt_surf = font1.render(time_txt, True, (255, 255, 255))  # AntiAlias (bool) : smooth out edges of font.
    txt_rect = txt_surf.get_rect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 30))
    display_surface.blit(txt_surf, txt_rect)
    return(pg.draw.rect(bg_surf, color='white', rect=txt_rect.inflate(50, 50), width=8, border_radius=5))

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
# laser_rect = laser_surf.get_rect(midbottom=ship_rect.center)

# Creating text.
font1 = pg.font.Font('./graphics/subatomic.ttf', 40)
# txt_surf = font1.render(f"Score: {pg.time.get_ticks()}", True, (255, 255, 255))  # AntiAlias (bool) : smooth out edges of font.
# txt_rect = txt_surf.get_rect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 25))

##############################################  TIME IN PYGAME  ##############################################
# Pygame can get the time since pygame.init() was called.
# We can create repeated timers.

##############################  CREATING A TIMER  ################################
# Check start time and end time (current time), their difference can be used.

##############################################################################################################
# Set up a clock.
clk = pg.time.Clock()   # But what if the game runs even slower?.

# Ideally, we don't want to limit the frame rate, so that the game is 'fluid'.

while(True):
    # 1.) Inputs (event loop).
    for event in pg.event.get():
        if(event.type == pg.QUIT):
            pg.quit()
            print("Game Closed!")
            sys.exit()

        if(event.type == pg.MOUSEBUTTONDOWN):
            # Applying timer logic to limit how fast (once every half second) lasers can be shot,
            # else, game would become too easy.
            if(pg.time.get_ticks() - last_fire_time >= 500):
                laser_rect = laser_surf.get_rect(midbottom=ship_rect.center)
                lasers.append(laser_rect)
                last_fire_time = pg.time.get_ticks()

    # Get delta time.
    dt = clk.tick(120)/1000  # in milliseconds.

    # Mouse Input.
    ship_rect.center = pg.mouse.get_pos()
    
    # Applying delta time concept for movement.
    lsr_move(lasers)

    # Get time since game started (since pg.init() was called).
    # time_since_start = pg.time.get_ticks() # milliseconds in seconds.

    # 2.) Update elements.
    display_surface.fill("black")
    display_surface.blit(bg_surf, (0, 0))
    
    # display_surface.blit(txt_surf, txt_rect)
    # pg.draw.rect(bg_surf, color='white', rect=txt_rect.inflate(30, 30), width=8, border_radius=5)
    
    # Using some temporary variables to display updated values such as time or score.
    t_r = get_time_since_start(tf, t_r)
    tf += 1
    
    # Display lasers.
    for lsr in lasers:
        display_surface.blit(laser_surf, lsr)
    
    display_surface.blit(ship_surf, ship_rect)

    # 3.) Show display_surface as a final frame.
    pg.display.update()
