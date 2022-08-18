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
            new_laser = Laser(my_ship, lsr_grp)
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

        # Position and direction attributes as a vector2 (float-based position).
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2((0, -1))
        self.speed = 350

    def update(self):
        # Moving the laser.
        self.pos += self.direction*self.speed*dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))

#############################  MOVING LASERS  ################################
# To address the problems with delta time, we are not going to store the position
# in rect but rather in a vector2. [rect --> (int, int)] whereas [vector2 --> (float, float)].

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
# my_laser = Laser(ship=my_ship, groups=lsr_grp)

# Game loop.
while(True):
    # Event loop.
    for event in pg.event.get():
        if(event.type == pg.QUIT):
            pg.quit()
            print("Game Closed!")
            sys.exit()

    # Delta time.
    dt = clk.tick(120)/1000  # No limit for frame rate specified yet!

    # Displat Background.
    display_surface.blit(bg_surf, (0,0))

    # Display Sprites.
    lsr_grp.draw(display_surface)
    ship_grp.draw(display_surface)

    # Update sprites.
    ship_grp.update()
    lsr_grp.update()

    # Keep window displayed.
    pg.display.update()
