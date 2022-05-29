import numpy as np

class Box:
    def __init__(self, box_filler, padding, color, top_right: tuple[int,int] = (), top_left: tuple[int,int] = (), bot_right: tuple[int,int] = (), bot_left: tuple[int,int] = ()):
        # coordinates of box on turtle screen
        self.top_right = top_right
        self.top_left = top_left
        self.bot_right = bot_right
        self.bot_left = bot_left
        self.entire_box = []
        # dead/alive (highlighted/unhighlighted)
        self.alive = False
        # neighbour data
        self.neighbours = []
        self.alive_neighbours = None
        self.dead_neighbours = None
        self.box_filler = box_filler
        self.padding = padding
        self.color = color

    def resurrect(self, CHANGE_PER_X_ITERATION, CHANGE_PER_Y_ITERATION):
        self.box_filler.color(self.color)
        self.box_filler.showturtle()
        self.alive = True
        self.box_filler.penup()
        self.box_filler.goto(self.top_left[0] + self.padding, self.top_left[1] - self.padding)
        self.box_filler.setheading(0)
        self.box_filler.begin_fill()
        for _ in range(2):
            self.box_filler.forward(CHANGE_PER_X_ITERATION - self.padding * 2)
            self.box_filler.right(90)
            self.box_filler.forward(CHANGE_PER_Y_ITERATION - self.padding * 2)
            self.box_filler.right(90)
        self.box_filler.end_fill()

        self.box_filler.hideturtle()

    def kill(self, CHANGE_PER_X_ITERATION, CHANGE_PER_Y_ITERATION):
        self.box_filler.showturtle()

        self.box_filler.color('black')
        self.alive = False
        self.box_filler.penup()
        self.box_filler.goto(self.top_left[0] + self.padding, self.top_left[1] - self.padding)
        self.box_filler.setheading(0)
        self.box_filler.begin_fill()
        for _ in range(2):
            self.box_filler.forward(CHANGE_PER_X_ITERATION - self.padding * 2)
            self.box_filler.right(90)
            self.box_filler.forward(CHANGE_PER_Y_ITERATION - self.padding * 2)
            self.box_filler.right(90)
        self.box_filler.end_fill()

        self.box_filler.hideturtle()

    def update_neighbours(self, current_game_board):
        self.neighbours = get_neighbours_of_item(current_game_board, item=self)
        self.alive_neighbours = len([b for b in self.neighbours if b.alive])
        self.dead_neighbours = 8 - self.alive_neighbours

def get_neighbours_of_item(array: list, item: Box):
    array = np.array(array)
    item_loc = tuple(np.asarray(np.where(array == item)).T[0].tolist())
    s = tuple(np.array(array.shape) - 1)
    n = np.array([-1, 0, +1])
    rows = item_loc[0] + n
    cols = item_loc[1] + n
    neighbor_loc = [
        (x, y) for x in rows for y in cols if (0 <= x <= s[0]) & (0 <= y <= s[1])
    ]
    neighbor_loc.remove(item_loc)

    return array[tuple(np.transpose(neighbor_loc))].tolist()
