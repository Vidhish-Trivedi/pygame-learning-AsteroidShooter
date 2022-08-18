import pygame as pg
import sys
import random

##################### VARIALBLES AND CONSTANTS AND FUNCTIONS  #######################
pg.init()
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
game_score = 0  # This would be a global variable.

############################## SHIP CLASS  ###########################
class Ship(pg.sprite.Sprite):
    def __init__(self, groups):
        # Initialise parent class.
        super().__init__(groups)  # groups is passed to parent class.
        self.image = pg.image.load('../graphics/ship.png').convert_alpha()  # This could also be text.
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        # Attribute for creating timer (for laser shots).
        self.since_last_shot = -1000

        # Add a mask.
        self.mask = pg.mask.from_surface(self.image)  # This attribute "has to be" called 'mask'.

    def pos_input(self):
        pos = pg.mouse.get_pos()
        self.rect.center = pos
    
    def shoot_lsr(self):
        mouse_input = pg.mouse.get_pressed()[0]
        if(mouse_input and (pg.time.get_ticks() - self.since_last_shot > 500)):
            new_laser = Laser(my_ship, lsr_grp)
            self.since_last_shot = pg.time.get_ticks()

    def mtr_collide(self):
        if(pg.sprite.spritecollide(self, mtr_grp, False, pg.sprite.collide_mask)):  # condition statement returns a list (checks empty or not).
            pg.quit()
            print("Game Over!")
            print(f"Final Score: {game_score}.")
            sys.exit()

    def update(self):
        self.pos_input()
        self.shoot_lsr()
        self.mtr_collide()

###############################  LASER CLASS  ################################
class Laser(pg.sprite.Sprite):
    def __init__(self, ship, groups):
        super().__init__(groups)
        self.image = pg.image.load('../graphics/laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=my_ship.rect.center)
        # Add a mask.
        self.mask = pg.mask.from_surface(self.image)

        # Position and direction attributes as a vector2 (float-based position).
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2((0, -1))
        self.speed = 350

    def mtr_collide(self):
        global game_score
        if(pg.sprite.spritecollide(self, mtr_grp, True, pg.sprite.collide_mask)):
            game_score += 1  # Increment score.
            pg.sprite.Sprite.kill(self)  # Removing Laser which collided.
            

    def update(self):
        # Moving the lasers.
        self.pos += self.direction*self.speed*dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.mtr_collide()
        if(self.pos.y < -100):
            self.kill()  # Destroy this sprite.

################################  METEOR CLASS  ###############################
# Timer for creating meteors.
meteor_timer = pg.event.custom_type()
pg.time.set_timer(meteor_timer, 800)

class Meteor(pg.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pg.image.load('../graphics/meteor.png').convert_alpha()
        
        scale_factor = random.choice([0.5, 1, 1.5, 2])
        self.image = pg.transform.scale(self.image, (scale_factor*self.image.get_width(), scale_factor*self.image.get_height()))
        
        self.initial_surf = self.image
        self.rect = self.image.get_rect(center=position)
        # Add a mask.
        self.mask = pg.mask.from_surface(self.image)

        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2((random.uniform(-0.5, 0.5), 1))
        self.speed = 200

        self.rotation = 0
        self.rotation_speed = random.randint(20, 50)

    def rotate_mtr(self):
        self.rotation += self.rotation_speed*dt
        self.image = pg.transform.rotozoom(self.initial_surf, self.rotation, scale=1)  # To fix wobbly movement.
        self.rect = self.image.get_rect(center=self.rect.center)  # To fix wobbly movement. (Still persists at high speeds).
        self.mask = pg.mask.from_surface(self.image)  # Updating the mask.

    def update(self):
        # Moving the meteors.
        self.pos += self.direction*self.speed*dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.rotate_mtr()
        if(self.pos.y > WINDOW_HEIGHT + 100):
            self.kill()  # Destroy this sprite.

#############################  SCORE CLASS  ##################################
# It is simple, so doesn't necessarily need to be a child of Sprite() class.
class Score:
    def __init__(self):
        self.font1 = pg.font.Font('../graphics/subatomic.ttf', 40)

    def display(self):
        score_txt = f"Score: {game_score}"
        txt_surf = self.font1.render(score_txt, True, "white")
        txt_rect = txt_surf.get_rect(midbottom=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 25))
        display_surface.blit(txt_surf, txt_rect)
        pg.draw.rect(display_surface, "white", txt_rect.inflate(30, 30), width=8, border_radius=5)

#############################  COLLISIONS  ##################################
# Rectangular Collisions.
# pygame.sprit.spritecollide(sprite, group, DoKill). (DoKill --> for group, won't destroy the sprite object).

# Better collisions using 'masks'. [Pixel-Perfect Collisions].
# A seperate object that checks which pixels are occupied inside a surface.



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
mtr_grp = pg.sprite.Group()

# Create Instances.
my_ship = Ship(ship_grp)
my_txt = Score()

# Game loop.
while(True):
    # Event loop.
    for event in pg.event.get():
        if(event.type == pg.QUIT):
            pg.quit()
            print("Game Closed!")
            sys.exit()

        if(event.type == meteor_timer):
            position = (random.randint(-50, WINDOW_WIDTH + 50), random.randint(-100, -50))
            new_mtr = Meteor(position, mtr_grp)

    # Delta time.
    dt = clk.tick(120)/1000

    # Displat Background.
    display_surface.blit(bg_surf, (0,0))

    # Update sprites.
    ship_grp.update()
    lsr_grp.update()
    mtr_grp.update()

    # Display Sprites.
    my_txt.display()
    lsr_grp.draw(display_surface)
    mtr_grp.draw(display_surface)
    ship_grp.draw(display_surface)

    # Keep window displayed.
    pg.display.update()
