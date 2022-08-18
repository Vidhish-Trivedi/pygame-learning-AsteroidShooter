import pygame as pg
import sys

##################### VARIALBLES AND CONSTANTS AND FUNCTIONS  #######################
pg.init()
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

############################## SHIP CLASS  ###########################
# Inherit from Sprite() class of pygame.
class Ship(pg.sprite.Sprite):
    def __init__(self, groups):
        # Initialise parent class.
        super().__init__(groups)  # groups is passed to parent class.
        self.image = pg.image.load('../graphics/ship.png').convert_alpha()  # This could also be text.
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        # Attribute for creating timer (for laser shots).
        self.since_last_shot = -1000

    def pos_input(self):
        pos = pg.mouse.get_pos()
        self.rect.center = pos
    
    def shoot_lsr(self):
        mouse_input = pg.mouse.get_pressed()[0]
        if(mouse_input and (pg.time.get_ticks() - self.since_last_shot > 500)):  # Computer checks this every frame, a 'click' lasts more than one frame. To fix this, we need a timer.
            print("shoot")
            self.since_last_shot = pg.time.get_ticks()

    def update(self):
        self.pos_input()
        self.shoot_lsr()
        # print("update")

###############################  LASER CLASS  ################################
class Laser(pg.sprite.Sprite):
    def __init__(self, ship, groups):
        super().__init__(groups)
        self.image = pg.image.load('../graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=my_ship.rect.center)

##############################  UPDATING SPRITES  #############################
# We can run any kind of code inside a sprite class.
# Like inputs, timers, heath, animations or physics.
# The group calls a method 'update()' for all sprites inside it.
# We can create many methods and then call them inside update method, then call only the update method.

# NOTE: Inside a class, we can not get access to the event loop.

###############################################################################

##############################  CREATE A WINDOW  ##############################
# Set up the window.
display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Asteroid Shooter")

# Set up background.
bg_surf = pg.image.load('../graphics/background.png').convert()

# Set up a clock.
clk = pg.time.Clock()

# Sprite groups.
ship_grp = pg.sprite.GroupSingle()
lsr_grp = pg.sprite.Group()

# Create Instances.
my_ship = Ship(ship_grp)
my_laser = Laser(ship=my_ship, groups=lsr_grp)

# Game loop.
while(True):
    # Event loop.
    for event in pg.event.get():
        if(event.type == pg.QUIT):
            pg.quit()
            print("Game Closed!")
            sys.exit()

    # Delta time.
    dt = clk.tick()/1000  # No limit for frame rate specified yet!

    # Displat Background.
    display_surface.blit(bg_surf, (0,0))

    # Display Sprites.
    lsr_grp.draw(display_surface)
    ship_grp.draw(display_surface)

    # Update sprites.
    ship_grp.update()

    # Keep window displayed.
    pg.display.update()
