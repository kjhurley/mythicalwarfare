import pygame


SCREEN_MAX_X = 500
SCREEN_MAX_Y = 500

class Inventory:
    NUM_BELT_ITEMS = 4
    def __init__(self):
        self.main_hand = None
        self.other_hand = None
        self.belt = []

    def pick_up(self, thing):
        """pick up - try main hand, then other hand

        :return True if picked up, else False"""
        if self.main_hand is None:
            self.main_hand = thing
            return True
        elif self.other_hand is None:
            self.other_hand = thing
            return True
        else:
            return False

    def put_down(self):
        """always put down main hand first

        :return dropped thing or None if nothing to drop
        """
        dropped = None
        if self.main_hand:
            dropped = self.main_hand
            self.main_hand = None
        elif self.other_hand:
            dropped = self.other_hand
            self.other_hand = None
        return dropped

    def put_from_main_hand_to_belt(self):
        if self.main_hand:
            if len(self.belt) < self.NUM_BELT_ITEMS:
                self.belt.append(self.main_hand)
                self.main_hand = None
                return True
        return False

    def put_from_other_hand_to_belt(self):
        if self.other_hand:
            if len(self.belt) < self.NUM_BELT_ITEMS:
                self.belt.append(self.other_hand)
                self.other_hand = None
                return True
        return False


colour_of_item = {
    'apple': (128,96,128),
    'sword': pygame.color.Color('lightsteelblue1'),
    'tree': pygame.color.Color('brown3'),
    'bread': pygame.color.Color('salmon')
}


class ScreenInventory:
    def __init__(self, inventory: Inventory):
        self.inventory = inventory
        self.rects = {'main_hand': None, 'other_hand': None}
        self.rects.update({f'belt{i}': None for i in range(inventory.NUM_BELT_ITEMS)})

        self.border_width = 5
        self.spacing = 2
        self.large_width = 50
        self.narrow_width = 25

    def colour_of_contents(self, contents):
        if contents is not None:
            if contents in colour_of_item:
                colour = colour_of_item[contents]
            else:
                colour = pygame.Color('black')
        else:
            colour = (255, 255, 255)
        return colour

    def draw_a_slot(self, win, top_left_x, top_left_y, width, contents):
        # first draw large rect in black, then slightly smaller inside in white
        pygame.draw.rect(win, (0, 0, 0), (top_left_x, top_left_y, width, width))
        colour = self.colour_of_contents(contents)
        r = pygame.draw.rect(win, colour, (top_left_x + self.border_width,
                                       top_left_y + self.border_width,
                                       width - 2 * self.border_width,
                                       width - 2 * self.border_width))
        return r

    def handle_click(self, mouse_pos):
        # is mouse over slot
        rects_to_inv = {
            'main_hand': self.inventory.main_hand,
            'other_hand': self.inventory.other_hand
        }
        rects_to_inv.update({f'belt{i}': self.inventory.belt[i] if i < len(self.inventory.belt) else None for i in range(self.inventory.NUM_BELT_ITEMS)})
        for k in rects_to_inv:
            if self.rects[k].collidepoint(mouse_pos):
                print(rects_to_inv[k])

    def draw(self, win):
        # large slots at top - main hand + other hand
        # then backpack - 1 col, 5 rows (must press e to show)
        # belt - 1 col, 4 rows

        # top 2 slots: main hand and other hand
        start_x = SCREEN_MAX_X - 2 * self.large_width - self.spacing
        x = start_x
        y = 0

        self.rects['main_hand'] = self.draw_a_slot(win, x, y, self.large_width, self.inventory.main_hand)
        x += self.large_width + self.spacing
        self.rects['other_hand'] = self.draw_a_slot(win, x, y, self.large_width, self.inventory.other_hand)
        y += self.large_width + self.spacing
        x = SCREEN_MAX_X - self.narrow_width
        for i in range(self.inventory.NUM_BELT_ITEMS):
            try:
                thing = self.inventory.belt[i]
            except IndexError:
                thing = None
            self.rects[f'belt{i}'] = self.draw_a_slot(win, x, y, self.narrow_width, thing)
            y += self.narrow_width + self.spacing

def actions(inventory):
    inventory.pick_up('apple')
    yield
    inventory.pick_up('sword')
    yield
    inventory.put_down()
    yield
    inventory.pick_up('bread')
    yield
    inventory.put_from_main_hand_to_belt()
    yield
    inventory.put_from_other_hand_to_belt()
    yield
    inventory.pick_up('tree')
    yield
    inventory.pick_up('bread')
    yield
    inventory.put_down()

def main():
    """run standalone"""

    pygame.init()
    max_x = SCREEN_MAX_X
    max_y = SCREEN_MAX_Y
    pygame.init()
    pygame.font.init()
    # pygame.mixer.init()

    font = pygame.font.SysFont(None, 25)

    win = pygame.display.set_mode((max_x, max_y))
    green = (0, 122, 0)
    pygame.display.set_caption('inventory')
    win.fill((green))

    run = True
    clock = pygame.time.Clock()

    inventory = Inventory()

    scr_inv = ScreenInventory(inventory)

    g = actions(inventory)

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    scr_inv.handle_click(mouse_pos)
                if event.button == 3:
                    next(g)

        scr_inv.draw(win)
        pygame.display.update()

        clock.tick(30) # frames per second

if __name__ == '__main__':
    main()