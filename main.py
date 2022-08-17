import pygame as pg
import sys
pg.init()  # Initialise pygame.

# LOOP:
    # Player input and check for changes.
    # Use input to update player and other properties on screen.
    # Combine all elements (UI) on screen.
    # Display screen to user.

# 30 fps ==> 0.0167 seconds.

#####################################  CONSTANTS  #####################################
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
ship_y = 600

#####################################  CREATE A WINDOW  #################################
display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Asteroid Shooter")  # Set title of window.

# We have 2 types of surfaces --> 'Display surface' (Main canvas (unique))
#                             and 'surface' (other images, to be placed on the Display surface).
# Surfaces (3 ways).
# a.) Creating one using pygame.
# test_surface = pg.Surface((400, 100))
    
# b.) Importing an image, should convert formats for better performance.
ship_surf = pg.image.load('./graphics/ship.png').convert_alpha()  # To be used when img has transparent areas (blank/not of use).
ship_rect = ship_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
# print(ship_rect)  # <rect(0, 0, 99, 75)> ==> <left, top, width, height>

bg_surf = pg.image.load('./graphics/background.png').convert()

# c.) Creating text.
# font object (style and size) --> render string --> surface.
font1 = pg.font.Font('./graphics/subatomic.ttf', 50)  # .ttf --> True Type Font.
txt_surf = font1.render("Hello, World!", True, (255, 255, 255))  # AntiAlias (bool) : smooth out edges of font.
txt_rect = txt_surf.get_rect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT))

# To keep window displayed.
# Inside this loop, we will check for input, update elements and place graphics
# the display_surface. At the end of the loop, we will show the display_surface.
# This while loop determines speed of game. (system dependent).

# Easy Solution --> set maximum framerate.
clk = pg.time.Clock()


while(True):
    # 1.) Player inputs (events).
    for event in pg.event.get():
        if(event.type == pg.QUIT):  # "X" at top right corner.
            pg.quit()
            print("Game Closed!")
            sys.exit()  # Ends all code currently running.

    # Limit maximum framerate.
    clk.tick(120)

    # 2.) Update elements.
    # display_surface.fill(BG_COLOR)
    # test_surface.fill((186, 120, 39))  # Changing color.
    # Place surface on display using 'blit' method (block image transfer).
    # display_surface.blit(test_surface, (0, 0))  # Position is of top left corner of surface to be placed.
    # display_surface.blit(test_surface, (WINDOW_WIDTH - test_surface.get_width(), 300))
    
    # Surfaces are placed in order of code, i.e, on top (overlapping) one another.
    display_surface.blit(bg_surf, (0, 0))
    # display_surface.blit(ship_surf, (300, ship_y))
    # ship_y -= 2  # To move ship upwards.
    # Positions (x, y) are difficult to work with, so we use 'rect' for positioning and movement (only the rect moves!).
    
    if(ship_rect.top > 0):
        ship_rect.bottom -= 2  # Moving the ship using 'rect'.

    display_surface.blit(ship_surf, ship_rect)
    # display_surface.blit(txt_surf, ((WINDOW_WIDTH - txt_surf.get_width())/2, (WINDOW_HEIGHT - 50)))
    display_surface.blit(txt_surf, txt_rect)
    
    

    # 3.) Show display_surface.
    pg.display.update()
