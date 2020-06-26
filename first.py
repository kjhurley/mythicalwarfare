import pygame
import random

fallen_trees = 0

spawn_x= random.randint (1,500)
spawn_y= random.randint (1,500)








class Player:
    def __init__(self, pos, radius, velocity=5, screen_size=(500,500)):
        self.x = pos[0]
        self.y = pos[1]
        self.r = radius
        self.v = velocity
        self.screen_size = screen_size # (x,y) tuple

    def coord(self):
        return (self.x, self.y)

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
        centre_of_screen = (self.screen_size[0]//2, self.screen_size[1]//2)
        pygame.draw.circle(win, ( 236, 188, 180), centre_of_screen, self.r)

    def new_pos(self, dir):
        """update position - dir is 'left', 'right', 'up' or 'down'"""
        x, y = (self.x, self.y)
        if dir == 'left':
            x -= self.v
        if dir == 'right':
            x += self.v
        if dir == 'down':
            y -= self.v
        if dir == 'up':
            y += self.v
        return (x, y)

    def move_to(self, new_pos):
        self.x, self.y = new_pos

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


class Tree:
    def __init__(self, pos, radius):
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
    def __init__(self, pos, radius):
        super().__init__(pos, radius)
        self.r = radius

    def draw(self, win, player):
        screen_x, screen_y = player.screen_coord((self.x, self.y))

        if not self.fallen:
            pygame.draw.circle(win, self.COLOUR, (screen_x, screen_y), self.r)

    def is_colliding(self, pos, radius):
        """True if circle at pos of given radius is touching"""
        if self.overlaps(pos, radius + self.r):
            return True
        else:
            return False

    def is_chopped(self, click_pos):
        """rocks cant be chopped"""
        return False


pygame.init()
max_x = 500
max_y = 500
win = pygame.display.set_mode((max_x, max_y))
green = (0,122,0)
pygame.display.set_caption('my game')
win.fill((green))

radius = 20
player = Player((0,0), radius=radius, velocity=5, screen_size=(max_x, max_y))

left_key = pygame.K_a
right_key = pygame.K_d
up_key = pygame.K_w
down_key = pygame.K_s

trees = []
for i in range(50):
    tree1_pos = (random.randint(-400, 400), random.randint(-400, 400))
    new_tree = Tree(tree1_pos, radius)
    if not new_tree.is_colliding(player.coord(), radius):
        trees.append(new_tree)
        
rocks = []
for i in range(1000):
    rock1_pos = (random.randint(-2000, 2000), random.randint(-2000, 2000))
    new_rock = Rock(rock1_pos, 5)
    if not new_rock.is_colliding(player.coord(), radius):
        rocks.append(new_rock)

inventory_display = False

run = True
while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4: # mouse wheel up
                if player.v < max_x/2:
                    player.v += 1
            if event.button == 5: # mouse wheel down
                if player.v > 0: # can't go slower than full stop!
                    player.v -= 1
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                map_pos = player.map_coord(mouse_pos)
                for tree in trees:
                    if tree.is_chopped(map_pos):
                        print('chop')
                        if tree.fallen:
                            fallen_trees += 1
                            if fallen_trees == 1:
                                print("TIMBER! That's %d tree." % fallen_trees)
                            else:
                                print("TIMBER! That's %d trees." % fallen_trees)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_i]:
        # toggle inventory
        inventory_display = not inventory_display

    # moving down is positive y change!
    # allow multiple keys down at same time - use if not elif
    key_to_dir = {
        keys[right_key]: 'right',
        keys[left_key]: 'left',
        keys[down_key]: 'up',
        keys[up_key]: 'down'
    }
    for k, dir in key_to_dir.items():
        if k:
            new_pos = player.new_pos(dir)
            any_collisions = False
            for tree in trees:
                if tree.is_colliding(new_pos, player.r):
                    any_collisions = True
                    break
            if not any_collisions:
                player.move_to(new_pos)

    win.fill((green))
    player.draw(win)
    for tree in trees:
        tree.draw(win, player)
    for rock in rocks:
        rock.draw(win, player)

    pygame.display.update()


pygame.quit()