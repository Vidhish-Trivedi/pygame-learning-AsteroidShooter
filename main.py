import pygame as pg
import sys

# 30 fps ==> 0.0167 seconds.

# Two ways to get inputs inside the game loop [while (True):] seperate methods outside event loops, OR via event loops.
# Usually, event loops are used for general actions like closing the window, file upload, etc and NOT player controls.

#####################################  CONSTANTS  #####################################
pg.init()  # Initialise pygame.
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

#####################################  CREATE A WINDOW  #################################
# Set up a window.
display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Asteroid Shooter")  # Set title of window.
    
# Ship.
ship_surf = pg.image.load('./graphics/ship.png').convert_alpha()  # To be used when img has transparent areas (blank/not of use).

# Manipulating images (surfaces).
# ship_surf_2x = pg.transform.scale2x(ship_surf)
# ship_surf_scaled = pg.transform.scale(ship_surf, (new_width, new_height))
# ship_surf_reversed = pg.transform.flip(surface=ship_surf ,flip_x=False, flip_y=True)  # Invert ship.
# ship_surf = pg.transform.rotate(ship_surf, 45)

ship_rect = ship_surf.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
# print(ship_rect)  # <rect(0, 0, 99, 75)> ==> <left, top, width, height>

# BG surface.
bg_surf = pg.image.load('./graphics/background.png').convert()

# Laser.
laser_surf = pg.image.load('./graphics/laser.png').convert_alpha()
laser_rect = laser_surf.get_rect(midbottom=ship_rect.midtop)

# Creating text.
# font object (style and size) --> render string --> surface.
font1 = pg.font.Font('./graphics/subatomic.ttf', 50)  # .ttf --> True Type Font.
txt_surf = font1.render("Space", True, (255, 255, 255))  # AntiAlias (bool) : smooth out edges of font.
txt_rect = txt_surf.get_rect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 25))

# To set maximum framerate.
clk = pg.time.Clock()

while(True):
    # 1.) Inputs (event loop).
    for event in pg.event.get():
        if(event.type == pg.QUIT):  # "X" at top right corner.
            pg.quit()
            print("Game Closed!")
            sys.exit()  # Ends all code currently running.

        # if(event.type == pg.MOUSEMOTION):
        #     # Use mouse position to control ship.
        #     # ship_rect.centerx = event.pos[0]
        #     # ship_rect.centery = event.pos[1]
        #     ship_rect.center = event.pos

        # if(event.type == pg.MOUSEBUTTONDOWN):
        #     # Checks for mouse button release.
        #     print('Shoot')


    # Limit maximum framerate.
    clk.tick(120)

    # Mouse Input.
    # Use mouse position to control ship.
    ship_rect.center = pg.mouse.get_pos()
    # laser_rect.midbottom = ship_rect.midtop

    # if(pg.mouse.get_pressed()[0] == True):
    #     print("Shoot!")

    laser_rect.centery -= 1  # Move laser upwards.

    # 2.) Update elements.
    display_surface.blit(bg_surf, (0, 0))
    
    display_surface.blit(txt_surf, txt_rect)
    pg.draw.rect(bg_surf, color='white', rect=txt_rect.inflate(30, 30), width=8, border_radius=5)
    
    display_surface.blit(ship_surf, ship_rect)
    display_surface.blit(laser_surf, laser_rect)

##########################  Drawing  ##############################
# [SEE DOCUMENTATION]
    # 'rect' can also be used to draw shapes.
    # 'rect' can be made without surfaces also.
    # # test_rect = pg.Rect(left, top, width, height)
    # # pg.draw.rect()
    # # pg.draw.circle()
    # # pg.draw.ellipse()
    # # # pg.draw.[other methods]
    
    # test_rect = pg.Rect(100, 200, 400, 500)
    # pg.draw.ellipse(display_surface, 'red', test_rect, width=10)

    # pg.draw.aalines(surface=bg_surf, color='red', closed=False, points=[(100, 100), (200, 100), (300, 400)])

    # Surfaces can be transformed (scale, flip).
    # pg.transform.scale()
    # pg.transform.flip()
################################################################

    # 3.) Show display_surface as a final frame.
    pg.display.update()
