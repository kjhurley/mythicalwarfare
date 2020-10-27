#bugs:
# (1) when zombie dead he stays on screen
#
#   fix:
#      idk
#
# (2) zombie moves left only
#    fix: redo the Zombie.update method to calculate distance between
#    zombie and player as vector. Use angle of that vector to rotate the
#    zombie velocity vector. Then add velocity vector to zombie position


import pygame
from pygame import sprite
from pygame import rect
import pygame.math
import math
import random
import time
from math import sqrt

SCREEN_MAX_X = 500
SCREEN_MAX_Y = 500


pygame.init()
pygame.font.init()
# pygame.mixer.init()


font= pygame.font.SysFont(None, 25)
def message_to_screen(msg,color,pos):
    screen_text= font.render(msg, True, color)
    win.blit(screen_text, (pos))





button_click= 0

class Zombie(pygame.sprite.Sprite):
    def __init__(self, coord):
        super().__init__()
        #self.colour = (0x98, 0xfb, 0x98)  # pale green
        self.colour = (0, 50, 0) # green
        self.width = 30
        self.height = 30
        self.x, self.y = coord

        self.screen_pos = pygame.math.Vector2(0, 0)

        self.image = pygame.Surface([self.width, self.height])
        pygame.draw.rect(self.image, self.colour, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()

        # max speed of zombie
        self.velocity = pygame.math.Vector2(3, 0)

        self.hp = 9
        self.killed = False
        self.visible_range = 1000 # zombies can't see very well

    def update_screen_pos(self, player):
        """given player, update zombie screen coordinates"""
        if not self.killed:
          self.screen_pos = pygame.math.Vector2(player.screen_coord((self.x, self.y)))
          self.rect = self.image.get_rect(x=self.screen_pos.x, y=self.screen_pos.y)

    def update(self, player):
        """move toward the player"""
        if self.killed:
          return
        player_pos = pygame.math.Vector2((player.x, player.y))
        pos = pygame.math.Vector2(self.x, self.y)
        # collision calculation uses screen co-ordinates
        player_screen_pos = pygame.math.Vector2(player.player_screen_coord())
        if not self.rect.collidepoint((player_screen_pos.x, player_screen_pos.y)):
            to_player = player_pos - pos
            if to_player.length() < self.visible_range:
                _, angle_to_player = to_player.as_polar()
                move = self.velocity.rotate(angle_to_player)
                pos += move
                self.x, self.y = pos.x, pos.y
        else:
            player.hit(1)

        self.update_screen_pos(player)

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.killed = True
            self.kill()










class Button:
    def __init__(self):
        self.colour = (255, 0, 0)
        self.position= 250
        self.rect_coords = (self.position, self.position, 50, 30)
        self.rect = None
        self.clicked = False

    def draw(self):
         self.rect = pygame.draw.rect(win, self.colour, self.rect_coords)

    def click(self):
         for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = self.rect.collidepoint(pygame.mouse.get_pos())
                    if click == 1:
                        self.colour = (0, 0, 255)
                        self.clicked = True

    def message(self, msg):
            message_to_screen(msg, [0, 0, 0], [255, 255])






armour_durb= 100


class Player:
    def __init__(self, pos, radius, velocity=5, screen_size=(SCREEN_MAX_X, SCREEN_MAX_Y)):
        self.x = pos[0]
        self.y = pos[1]
        self.r = radius
        self.v = velocity
        self.energy= None
        self.hit_count = 0
        self.screen_size = screen_size # (x,y) tuple
        self.health = (100 - self.hit_count)
        self.armour_durb= 50
        self.colour = ( 236, 188, 180)
        self.hit_chance= ['hit']

    def coord(self):
        return (self.x, self.y)

    def draw_health_bar(self, win, full_size, pos_x, pos_y):
        player_hp = full_size/100
        health = (player_hp - self.hit_count)
        hp_bar = full_size - health
        pygame.draw.rect(win, (255, 0, 0), (pos_x, pos_y, full_size, 25))
        pygame.draw.rect(win, (0,255,0), (40, 30, 20, 10))
        pygame.draw.rect(win, (0, 255, 0), (pos_x, pos_y, hp_bar, 25))
    def draw_hunger_bar(self, win, full_size, pos_x, pos_y):
        player_h = full_size/100
        
        hunger = (player_h - self.energy)
        hp_bar = full_size - hunger
        pygame.draw.rect(win, (255, 0, 0), (pos_x, pos_y, full_size, 25))
        pygame.draw.rect(win, (0,255,0), (40, 30, 20, 10))
        pygame.draw.rect(win, (0, 255, 0), (pos_x, pos_y, hp_bar, 25))
        heal=random.randint(1, 5)
        if hunger== 100:
          self.health+= heal


    def map_coord(self, screen_coord):
        """convert a screen coordinate to a map coordinate"""
        x, y = screen_coord
        centre_of_screen = self.player_screen_coord()
        relative_to_player = (x - centre_of_screen[0], y - centre_of_screen[1])
        return (relative_to_player[0] + self.x, relative_to_player[1] + self.y)

    def screen_coord(self, pos):
        """convert pos to screen

        given a pos (x, y) co-ord pair, convert to screen co-ord

        e.g screen (500, 500), player at (0, 0) and pos at (-100, -200)
        then screen_pos should be 150, 50

        """
        x, y = pos
        rel_player = (x - self.x, y - self.y)
        centre_of_screen = self.player_screen_coord()

        return (rel_player[0] + centre_of_screen[0], rel_player[1] + centre_of_screen[1])

    def player_screen_coord(self):
        return (self.screen_size[0]//2, self.screen_size[1]//2)

    def draw(self, win):
        """player is always drawn in centre of screen"""

        # only draw if not dead
        if self.health > 0:
            centre_of_screen = (self.screen_size[0]//2, self.screen_size[1]//2)
            pygame.draw.circle(win, self.colour, centre_of_screen, self.r)

        # always draw health bar
        self.draw_health_bar(win, 100, 400, 0)

    def new_pos(self, dirs):
        """update position - dir is comma seperated string - 'left', 'right', 'up' or 'down'"""
        x, y = (self.x, self.y)
        for d in dirs.split(','):
            if d == 'left':
                x -= self.v
            if d == 'right':
                x += self.v
            if d == 'down':
                y -= self.v
            if d == 'up':
                y += self.v
        return (x, y)

    def move_to(self, new_pos):
        self.x, self.y = new_pos
        self.energy = random.randint(3, 5)


    def overlaps(self, pos, radius=None):
        if radius is None:
            radius = self.r
        if -radius < (pos[0] - self.x) < radius:
            if -radius < (pos[1] - self.y) < radius:
                return True
        return False

    def is_colliding(self, pos, radius):
        """True if circle at pos of given radius is touching"""
        if self.fallen:
            # can't collide with fallen trees - they're gone
            return False
        if self.overlaps(pos, radius + self.r):
            return True
        else:
            return False

    def hit(self, hit_points):
        hit= random.choice(self.hit_chance)
        if hit== 'hit':
            self.hit_count -= hit_points
            self.colour = (255, 0, 0)  # player is hit
        else:
            self.armour_durb-=1
            print('protected')
    def armour(self, level):
        hit= self.hit_chance
        hit.clear()
        hit.append('hit')
        for i in range(level):
            hit.append('proctected')
    def draw_armour(self, level):
        size= radius +5 +level
        pygame.draw.circle(win, (0, 0, 0), (250, 250), size)
    



class Tree:
    def __init__(self, pos, radius=20):
        self.x = pos[0]
        self.y = pos[1]
        self.r = radius

        self.chop_count = 4
        self.fallen = False

    def draw(self, win, player):
        screen_x, screen_y = player.screen_coord((self.x, self.y))

        if not self.fallen:
            pygame.draw.circle(win, (210, 105, 30), (screen_x, screen_y), self.r)

    def overlaps(self, pos, radius=None):
        if radius is None:
            radius = self.r
        if -radius < (pos[0] - self.x) < radius:
            if -radius < (pos[1] - self.y) < radius:
                return True
        return False

    def is_colliding(self, pos, radius):
        """True if circle at pos of given radius is touching"""
        if self.fallen:
            # can't collide with fallen trees - they're gone
            return False
        if self.overlaps(pos, radius + self.r):
            return True
        else:
            return False

    def is_chopped(self, click_pos):
        """return True if click pos is inside circle"""
        if self.fallen:
            return False

        # first, simple version
        if -self.r < (click_pos[0] - self.x) < self.r:
            if -self.r < (click_pos[1] - self.y) < self.r:
                self.chop_count -= 1
                if self.chop_count == 0:
                    self.fallen = True
                return True

class Rock(Tree):
    COLOUR = 0xd3d3d3
    def __init__(self, pos, radius=5):
        super().__init__(pos, radius)
        self.r = radius

    def draw(self, win, player):
        screen_x, screen_y = player.screen_coord((self.x, self.y))

        if (0 < screen_x < SCREEN_MAX_X) and (0 < screen_y < SCREEN_MAX_Y):
            if not self.fallen:
                pygame.draw.circle(win, self.COLOUR, (screen_x, screen_y), self.r)

    def is_colliding(self, pos, radius):
        """True if circle at pos of given radius is touching"""
        return False

    def is_chopped(self, click_pos):
        """rocks cant be chopped"""
        return False


class Lake(Tree):
    COLOUR = 0x00007f
    def __init__(self, pos, radius=15):
        super().__init__(pos, radius)
        self.r = radius

    def draw(self, win, player):
        screen_x, screen_y = player.screen_coord((self.x, self.y))
        if (0 < screen_x < SCREEN_MAX_X) and (0 < screen_y < SCREEN_MAX_Y):
            if not self.fallen:
                pygame.draw.circle(win, self.COLOUR, (screen_x, screen_y), self.r)

    def is_colliding(self, pos, radius):
        """True if circle at pos of given radius is touching"""
        if self.overlaps(pos, radius + self.r):
            return True
        else:

            return False

    def is_chopped(self, click_pos):
        """lakes cant be chopped"""
        return False


class HexagonGeometery:
    SQRT_3_OVER_2 = sqrt(3.) / 2.

    vectors = [(-1.,0),(.5, SQRT_3_OVER_2),(.5,-SQRT_3_OVER_2)]

    @classmethod
    def randinunithex(cls):
        x = random.randrange(3)
        (v1,v2) = (cls.vectors[x], cls.vectors[(x+1)%3])
        (x,y) = (random.random(), random.random())
        return (x*v1[0]+y*v2[0],x*v1[1]+y*v2[1])

    @classmethod
    def hexagon_tiler(cls, start, hex_size, num_hexagons):
        """fill a map space using hexagons"""
        central_pos = start
        neighbour_count = 0
        diameter = hex_size

        # offset
        new_pos = start

        # spiral list of new centres around the starting point
        neighbours = [(0, 1), (cls.SQRT_3_OVER_2, 0.5), (cls.SQRT_3_OVER_2, -0.5),
                      (0, -1), (-cls.SQRT_3_OVER_2, 0.5), (-cls.SQRT_3_OVER_2, -0.5)]

        next_6 = [(diameter * x, diameter * y) for (x, y) in neighbours]

        while num_hexagons > 0:
            new_pos = next_6.pop()

            yield new_pos
            if not next_6:
                diameter += hex_size
                next_6 = [(diameter * x, diameter * y) for (x, y) in neighbours]
            num_hexagons -= 1

    @classmethod
    def is_in_unithex(cls, pos):
        """return True if pos (x, y) is within a unit hexagon centred on 0,0

        """

        x, y = pos
        l2 = x * x + y * y
        if l2 > 1.0:
            return False
        if l2 < 0.75:
            return True

        px = x / cls.SQRT_3_OVER_2
        if (px > 1.0 or px < -1.0):
            return False

        py = 0.5 * px + y
        if py > 1.0 or py < -1.0:
            return False

        if (px - py > 1.0) or (px - py < -1.0):
            return False

        return True


class Biome:
    DIAMETER = 1000
    def __init__(self, centre, terrain_types, terrain_choices, size=None, num_terrain_things=50):
        self.centre = centre
        assert all(t_type in terrain_types for t_type in terrain_choices)
        self.terrain_choice = terrain_choices
        self.terrain_types = terrain_types
        self.size = size or self.DIAMETER
        self.num_terrain_things = num_terrain_things

        self.terrains = {t_type: [] for t_type in self.terrain_types}

    def _is_pos_in_biome(self, pos, radius):
        """True if pos overlaps with this biome """
        relative_pos = (pos[0] - self.centre[0], pos[1] - self.centre[1])
        unit_pos = (2*relative_pos[0] / self.size, 2*relative_pos[1] / self.size)
        return HexagonGeometery.is_in_unithex(unit_pos)

    def does_biome_need_to_be_drawn(self, player: Player):
        """check if biome needs to be drawn

        if biome center is within screen width of player then draw it
        """
        return True

        if -SCREEN_MAX_X < self.centre[0] - player.x < SCREEN_MAX_X:
            if -SCREEN_MAX_Y < self.centre[1] - player.y < SCREEN_MAX_Y:
                return True
        else:
            return False


    def draw(self, win: pygame.Surface, player: Player):
        """draw the biome around the player onto the surface"""
        if self.does_biome_need_to_be_drawn(player):
            for t_type in self.terrains.keys():
                for t in self.terrains[t_type]:
                    t.draw(win, player)

    def random_in_hex(self):
        """generate random x,y within the biome hexagon"""
        pos = HexagonGeometery.randinunithex()
        pos = pos[0] * self.size, pos[1] * self.size
        return (int(self.centre[0] + pos[0]), int(self.centre[1] + pos[1]))

    def fill(self, map):
        """biome fills map with stuff like trees, rocks, lakes"""
        creation_order = []
        # create a bunch of terrain features eg rocks, trees etc
        for _ in range(self.num_terrain_things):
            creation_order.append(random.choice(self.terrain_choice))

        for t_type in self.terrain_types:
            for t in creation_order:
                if t == t_type:
                    pos = self.random_in_hex()
                    new_terrain = t_type(pos)
                    if not new_terrain.is_colliding(player.coord(), player.r):
                        self.terrains[t_type].append(new_terrain)

    def is_colliding(self, pos, radius):
        """True if circle at pos of given radius is touching something

        First check that pos
        """
        if self._is_pos_in_biome(pos, radius):
            for t_type in self.terrain_types:
                for t in self.terrains[t_type]:
                    if t.is_colliding(pos, radius):
                        return True
        return False

class Forest(Biome):
    def __init__(self, centre):
        choices = [Rock] * 15 + [Tree] * 5 + [Lake]
        super().__init__(centre, terrain_types=[Rock, Tree, Lake], terrain_choices=choices)


class Swamp(Biome):
    def __init__(self, centre):
        super().__init__(centre, [Lake], [Lake], num_terrain_things=500)


class Grassland(Biome):
    def __init__(self, centre):
        super().__init__(centre, [Rock], [Rock], num_terrain_things=2000)


class Map:
    """tracks all the biomes etc"""
    NUM_BIOMES = 7

    def __init__(self):
        self.biomes = []

    def draw(self, win: pygame.Surface, player: Player):
        """draw part of the map around the player onto the surface"""
        for b in self.biomes:
            b.draw(win, player)

    def generate(self):
        """fill the map with biomes"""
        biome_count = self.NUM_BIOMES
        self.biomes.append(Grassland((0,0)))
        biome_count -= 1
        for center in HexagonGeometery.hexagon_tiler((0, 0), Biome.DIAMETER, biome_count):
            self.biomes.append(Swamp(center))

        for b in self.biomes:
            b.fill(self)


pygame.init()
max_x = SCREEN_MAX_X
max_y = SCREEN_MAX_Y
win = pygame.display.set_mode((max_x, max_y))
green = (0,122,0)
pygame.display.set_caption('mythical warfare')
win.fill((green))

radius = 20
player = Player((0,0), radius=radius, velocity=5, screen_size=(max_x, max_y))

left_key = pygame.K_a
right_key = pygame.K_d
up_key = pygame.K_w
down_key = pygame.K_s

# chop_sound = pygame.mixer.Sound("chop.wav")
# step_sound = pygame.mixer.Sound("./step.wav")
#
# def chop():
#     ####################################
#     pygame.mixer.Sound.play(chop_sound)
#     pygame.mixer.music.stop()
#
# def step():
#     pygame.mixer.Sound.play(step_sound)
#     pygame.mixer.music.stop()

        
world = Map()
world.generate()


zombies = pygame.sprite.Group()
z = Zombie((random.randint(1, 200), random.randint(1, 200)))
zombies.add(z)


inventory_display = False



fallen_trees = 0

spawn_x= random.randint (1,500)
spawn_y= random.randint (1,500)
game_start= 0

print('show startup button')

startup = True
button = Button()
clock = pygame.time.Clock()
pos_topleft_y= ((max_y/2)-25)
pos_topleft_x= ((max_x)/4)
full_load=	(max_x/2)
win.fill((0, 0, 0))
load= 0
while load<101:
    pygame.display.update
    percentage_load= int(load * full_load/100)
    pygame.draw.rect(win, (255, 0, 0), (pos_topleft_x, pos_topleft_y, full_load, 25))
    pygame.draw.rect(win, (0,255,0), (40, 30, 20, 10))
    pygame.draw.rect(win, (0, 255, 0), (pos_topleft_x, pos_topleft_y, percentage_load, 25))
    pygame.display.update()
    load+= 5
    time.sleep(0.1)
win.fill((green))
pygame.display.update

while startup:
    button.draw()
    button.click()
    if button.clicked:
        startup= False
    message_to_screen('MYTHICAL WARFARE', (250, 0, 0), (159, 120))
    button.message('start')
    pygame.display.update()
    win.fill((green))

def draw_crafting_grid():
    pygame.draw.rect(win, (128,128,128), (250, 0), (50, 50))
    pygame.draw.rect(win, (128,128,128), (200, 0), (50, 50))
    pygame.draw.rect(win, (128,128,128), (250, 50), (50, 50))
    pygame.draw.rect(win, (128,128,128), (200, 50), (50, 50))



print('starting')


run = True
pos_topleft_y= ((max_y/2)-25)
pos_topleft_x= ((max_x)/4)
full_load=	(max_x/2)

load= 0
while load<100:
    pygame.display.update
    percentage_load= load * full_load/100
    pygame.draw.rect(win, (255, 0, 0), (pos_topleft_x, pos_topleft_y, full_load, 25))
    pygame.draw.rect(win, (0,255,0), (40, 30, 20, 10))
    pygame.draw.rect(win, (0, 255, 0), (pos_topleft_x, pos_topleft_y, percentage_load, 25))
    pygame.display.update()


    load+= 1



max_speed= max_x/2




while run:
    command = None
    player.colour = ( 236, 188, 180)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.K_t:
            command= input('command:\n')

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: # mouse wheel up
                if player.v < max_speed:
                    player.v += 1
            if event.button == 5: # mouse wheel down
                if player.v > 0: # can't go slower than full stop!
                    player.v -= 1
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                map_pos = player.map_coord(mouse_pos)
                for b in world.biomes:
                    if Tree in b.terrains:
                        for tree in b.terrains[Tree]:
                            if tree.is_chopped(map_pos):
                                print('chop')
                                # chop()
                                if tree.fallen:
                                    fallen_trees += 1
                                    max_speed -= 5
                                    if fallen_trees == 1:
                                        print("TIMBER! That's %d tree." % fallen_trees)
                                    else:
                                        print("TIMBER! That's %d trees." % fallen_trees)

                for zombie in zombies:
                    if zombie.rect.collidepoint(pygame.mouse.get_pos()):
                        zombie.hit()
                        if zombie.killed:
                            print("Killed a zombie!")

    keys = pygame.key.get_pressed()

    if keys[pygame.K_i]:
        # toggle inventory
        inventory_display = not inventory_display

    # moving down is positive y change!
    # allow multiple keys down at same time - use if not elif
    movement = ''

    if keys[right_key]:
        movement = ','.join(['right'])
    if keys[left_key]:
        movement = ','.join(['left'])
    if keys[down_key]:
        movement = ','.join([movement, 'up'])
    if keys[up_key]:
        movement = ','.join([movement, 'down'])
    new_pos = player.new_pos(movement)
    any_collisions = False
    for b in world.biomes:
        if b.is_colliding(new_pos, player.r):
            any_collisions = True
            break
    if not any_collisions:
        player.move_to(new_pos)
        # step()

    dead_zombies = []
    for zombie in zombies:
        zombie.update(player)

    win.fill((green))


    player.hit_chance.clear()
    player.hit_chance.clear()
    if command== 'armor':
        level= input('level:\n')
        player.armour(level)

    world.draw(win, player)

    player.hit_chance.clear()
    player.hit_chance.append('hit')
    if player.armour_durb> 0:
      player.armour(3)
      player.draw_armour(3)
    zombies.draw(win)
    print(player.health)
    player.draw(win)
    player.draw_hunger_bar(win, 100, 400, 28)
    pygame.display.update()
    if player.health== 0:
      pygame.quit()

    clock.tick(30) # frames per second

message_to_screen('Why are you leaving?', [255, 0, 0], [250, 250])
pygame.display.update()
pygame.quit()