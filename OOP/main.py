import pygame as pg
import sys
# Pygame was created to be used using classes.
# Each object --> contains both the rect and the surface.

##################### VARIALBLES AND CONSTANTS AND FUNCTIONS  #######################
pg.init()
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

############################## SHIP CLASS  ###########################
# Inherit from Sprite() class of pygame.
class Ship(pg.sprite.Sprite):
    def __init__(self, groups):
        # Initialise parent class.
        super().__init__(groups)  # groups is passed to parent class. (This object will be added to these groups).
        # Create surface (called image inside Sprite class) for ship.
        self.image = pg.image.load('../graphics/ship.png').convert_alpha()  # This could also be text.
        # Create rect for ship.
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
# pg.sprite.Sprite()  # Use this to see definition of Sprit() [parent class of Ship()].

###############################  LASER CLASS  ################################
class Laser(pg.sprite.Sprite):
    def __init__(self, ship, groups):
        super().__init__(groups)
        # Create surface (image) for laser
        self.image = pg.image.load('../graphics/laser.png').convert_alpha()
        # Create rect for laser.
        self.rect = self.image.get_rect(midbottom=my_ship.rect.center)

################################  SPRITE  ####################################
# Sprites are classes, each sprite must have a rect and a surface.
# These allows us to control graphics, positions, input and updates for objects.
# Each visible element (as far as possible) should be a sprite.

# To draw a sprite, it needs to be put into a group.
# The group then draws the sprite on a surface (usually the display surface).
# The group can also update the sprite.

##############################  CREATE A WINDOW  ##############################
# Set up the window.
display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Asteroid Shooter")

# Set up background.
bg_surf = pg.image.load('../graphics/background.png').convert()

# Set up a clock.
clk = pg.time.Clock()

# Sprite groups.
ship_grp = pg.sprite.GroupSingle()  # GroupSingle() is used for group of single object, adding another object to it will remove the current one.
lsr_grp = pg.sprite.Group()

# Create a instance of Ship() class.
# my_ship = Ship()
# ship_grp.add(my_ship)  # Add this instance to a group.
# We can add a parameter in class declaration to easily add instances to groups.
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
    

    # Keep window displayed.
    pg.display.update()
