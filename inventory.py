import pygame


SCREEN_MAX_X = 500
SCREEN_MAX_Y = 500


class ScreenInventory:
    def __init__(self, inventory):
        self.inventory = inventory
        self.rects = {'main_hand': None, 'other_hand': None,
                      'belt': [None] * len(inventory['belt'])}
        self.border_width = 5
        self.spacing = 2
        self.large_width = 50
        self.narrow_width = 25

    def colour_of_contents(self, contents):
        if contents is not None:
            colour = (128,96,128)
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
        if self.rects['main_hand'].collidepoint(mouse_pos):
            print('main_hand')

    def draw(self, win):
        # large slots at top - main hand + other hand
        # then backpack - 1 col, 5 rows (must press e to show)
        # belt - 1 col, 4 rows

        # top 2 slots: main hand and other hand
        start_x = SCREEN_MAX_X - 2 * self.large_width - self.spacing
        x = start_x
        y = 0

        self.rects['main_hand'] = self.draw_a_slot(win, x, y, self.large_width, self.inventory['main_hand'])
        x += self.large_width + self.spacing
        self.rects['other_hand'] = self.draw_a_slot(win, x, y, self.large_width, self.inventory['other_hand'])
        y += self.large_width + self.spacing
        x = SCREEN_MAX_X - self.narrow_width
        for i, c in enumerate(self.inventory['belt']):
            self.rects['belt'][i] = self.draw_a_slot(win, x, y, self.narrow_width, c)
            y += self.narrow_width + self.spacing



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

    inventory = {
        'main_hand': None,
        'other_hand': 'apple',
        'belt': [None, None, 'sword', None]
    }

    scr_inv = ScreenInventory(inventory)

    while run:

        scr_inv.draw(win)
        pygame.display.update()

        clock.tick(30) # frames per second

if __name__ == '__main__':
    main()