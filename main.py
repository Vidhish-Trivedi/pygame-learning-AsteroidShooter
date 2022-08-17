from math import ceil
import pygame as pg
import sys

#####################################  CONSTANTS AND FUNCTIONS #####################################
pg.init()  # Initialise pygame.
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def lsr_move(lsr_list, speed = 120):
    for lsr in lsr_list:
        lsr.centery -= ceil(speed*dt)
        # Optimization. (Remove lasers which are outside the screen).
        if(lsr.bottom < 0):
            lasers.remove(lsr)

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
font1 = pg.font.Font('./graphics/subatomic.ttf', 50)
txt_surf = font1.render("Space", True, (255, 255, 255))  # AntiAlias (bool) : smooth out edges of font.
txt_rect = txt_surf.get_rect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 25))

# Set up a clock.
clk = pg.time.Clock()   # But what if the game runs even slower?.

# Ideally, we don't want to limit the frame rate, so that the game is 'fluid'.

#############################################################  DELTA TIME  ######################################################################
# Measures how long it took to create our current frame (one frame).
# For example, if frame rate is 60 fps, then DT = 1/60 = 0.0167 seconds.  (This can vary depending on frame rate).
# This information can be used to keep the game at a constant speed regardless of framerate.
# We multiply any movement inside the game with delta time.  (speed)*(frame rate)*(delta time) ==> (pixels per second)*(FPS)*(seconds per frame).
# Now, if the frame rate becomes half, DT becomes twice, negating any effect on time taken for movement.

######################  PROBLEMS WITH DELTA TIME  ############################
# When moving rects, we always place integers (at pixel positions (can not be decimals)).
# But, DT gives us floating point values, which are converted by pygame.
# For example, 5(original pos) + 0.835(move by) = 5.835 ==> 5 (by pygame) (for ever at 5 (recursion)). # HERE, NO MOVEMENT OCCURS.
# So, movement can sporadically stop/fail.
#################################################################################################################################################

while(True):
    # 1.) Inputs (event loop).
    for event in pg.event.get():
        if(event.type == pg.QUIT):
            pg.quit()
            print("Game Closed!")
            sys.exit()

        if(event.type == pg.MOUSEBUTTONDOWN):
            laser_rect = laser_surf.get_rect(midbottom=ship_rect.center)
            lasers.append(laser_rect)
            # print(len(lasers), lasers)

    # Get delta time.
    dt = clk.tick(120)/1000  # in milliseconds.

    # Mouse Input.
    ship_rect.center = pg.mouse.get_pos()
    
    # Applying delta time concept for movement.
    # laser_rect.centery -= ceil(1*dt)  # Move laser upwards. (By integer, round up to avoid problem with DT (mentioned above) ==> game becomes faster than it is supposed to be).
    # laser_rect.centery -= ceil(120*dt)
    lsr_move(lasers)

    # 2.) Update elements.
    display_surface.blit(bg_surf, (0, 0))
    
    display_surface.blit(txt_surf, txt_rect)
    pg.draw.rect(bg_surf, color='white', rect=txt_rect.inflate(30, 30), width=8, border_radius=5)
    
    # display_surface.blit(laser_surf, laser_rect)
    # Display lasers.
    for lsr in lasers:
        display_surface.blit(laser_surf, lsr)
    
    display_surface.blit(ship_surf, ship_rect)

    # 3.) Show display_surface as a final frame.
    pg.display.update()
