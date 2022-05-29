import time
import turtle
from conway_support import Box
import random


# SETTINGS
SCREEN_SIZE = (500, 500)
## \/ \/ \/ MUST BE EVEN NUMBERS. MUST BE EVEN NUMBERS. \/ \/ \/
ROWS_X = 8
ROWS_Y = 8
## /\ /\ /\ MUST BE EVEN NUMBERS. MUST BE EVEN NUMBERS. /\ /\ /\
# Speed of the turtle, # 0.5-10.5, >10.5 = 0
SPEED = 10.5
# Determines which events should be alerted. True/False for each. (death due to overpopulation, death due to underpopulation, cell survived, cell was born)
EVENT_ALERTS = (False, False, False, False)
# Auto-continue simulation after every generation/manually continue.
AUTO_CONTINUE = True
# Choose colors manually with inputs.
CHOOSE_COLORS = True
# Border color, this is overiden if CHOOSE_COLORS is True
GRID_COLOR = 'pink'
# Cell color, this is overiden if CHOOSE_COLORS is True
ALIVE_CELL_COLOR = 'pink'
# If the state of cells should be chosen at random at runtime.
RANDOM_CELLS = True
# Weighting of a cell being alive when chosen randomly, 1"%"-100"%".
RANDOM_CELL_ALIVE_WEIGHTING = 30
# How much space there is around a cell in it's socket. MINIMUM 1, 5 is good for games without heaps of cells
# games with many cells cannot have too high an umber
CELL_PADDING = 1
# If grids should be rendered or not.
RENDER_GRIDS = True
# If border should be rendered or not.
RENDER_BORDER = True
#If the time it takes to render a new generation should be tracked
TRACK_GENERATION_TIME = True


if CHOOSE_COLORS:
    print('What color should the border be? (r for random)')
    GRID_COLOR = input("> ")
    if GRID_COLOR.lower() == "r":
        GRID_COLOR = ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])]

    print("What color should the alive cells be? (r for random)")
    ALIVE_CELL_COLOR = input("> ")
    if ALIVE_CELL_COLOR.lower() == "r":
        ALIVE_CELL_COLOR = ["#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])]

CHANGE_PER_X_ITERATION = (SCREEN_SIZE[0]-20)*2/ROWS_X
CHANGE_PER_Y_ITERATION = (SCREEN_SIZE[1]-20)*2/ROWS_Y
TOP_LEFT = -SCREEN_SIZE[0] + 20, SCREEN_SIZE[1] - 20
simulation_started = False

cell_filler = turtle.Turtle()
cell_filler.speed(SPEED)
cell_filler.color(ALIVE_CELL_COLOR)

# init
turtle.screensize(canvwidth=SCREEN_SIZE[0], canvheight=SCREEN_SIZE[1],
                  bg="black")
grid_creator = turtle.Turtle()
grid_creator.color(GRID_COLOR)
grid_creator.speed(SPEED)

# make border
grid_creator.penup()
grid_creator.goto(TOP_LEFT)
grid_creator.pendown()

### VISUALISE BORDER
if RENDER_BORDER:
    for _ in range(4):
        grid_creator.forward((SCREEN_SIZE[0] - 20)*2)
        grid_creator.right(90)


### VISUALISE ROWS
if RENDER_GRIDS:
    for row in range(int(ROWS_X/2)):
        grid_creator.forward(CHANGE_PER_X_ITERATION)
        grid_creator.right(90)
        grid_creator.forward((SCREEN_SIZE[1]-20) * 2)
        grid_creator.left(90)
        grid_creator.forward(CHANGE_PER_X_ITERATION)
        grid_creator.left(90)
        grid_creator.forward((SCREEN_SIZE[1] - 20) * 2)
        grid_creator.setheading(0)

    # Y axis row
    grid_creator.right(90)
    for row in range(int(ROWS_Y/2)):
        grid_creator.forward(CHANGE_PER_Y_ITERATION)
        grid_creator.right(90)
        grid_creator.forward((SCREEN_SIZE[1]-20) * 2)
        grid_creator.left(90)
        grid_creator.forward(CHANGE_PER_Y_ITERATION)
        grid_creator.left(90)
        grid_creator.forward((SCREEN_SIZE[1] - 20) * 2)
        grid_creator.right(90)
# X axis rows


grid_creator.hideturtle()

# list which box classes will enter
boxes = []
top_left_calculating_box = -SCREEN_SIZE[0] + 20, SCREEN_SIZE[1] - 20
for y in range(ROWS_Y):
    for x in range(ROWS_X):
        box = Box(cell_filler, CELL_PADDING, ALIVE_CELL_COLOR)
        box.top_left = top_left_calculating_box
        box.top_right = (top_left_calculating_box[0] + CHANGE_PER_X_ITERATION, top_left_calculating_box[1])
        box.bot_left = (top_left_calculating_box[0], top_left_calculating_box[1] - CHANGE_PER_Y_ITERATION)
        box.bot_right = (top_left_calculating_box[0] + CHANGE_PER_X_ITERATION, top_left_calculating_box[1] - CHANGE_PER_Y_ITERATION)

        #calculate coordinates of full box
        complete_box_coordinates = []
        starting_point = box.top_left
        for i in range(int(abs(box.top_left[0] - box.top_right[0]))):
            for x in range(int(abs(box.top_left[1] - box.bot_left[1]))):
                complete_box_coordinates.append((int(starting_point[0] + i), int(starting_point[1] - x)))

        box.entire_box = complete_box_coordinates
        boxes.append(box)
        top_left_calculating_box = box.top_right
    top_left_calculating_box = boxes[::ROWS_X][-1].bot_left



game_board = [boxes[i:i+ROWS_X] for i in range(0, len(boxes), ROWS_X)]


def update_board(current_game_board: list[list[Box]]):
    if TRACK_GENERATION_TIME:
        print("Generation started, timer started...")
        time_1 = time.time()

    global simulation_started
    simulation_started = True
    changes_this_iteration = 0
    for x_row in current_game_board:
        for cell in x_row:
            cell.update_neighbours(game_board)

    for x_row in current_game_board:
        for cell in x_row:
            if cell.alive:
                if cell.alive_neighbours in (0,1):
                    # underpopulation
                    cell.kill(CHANGE_PER_X_ITERATION, CHANGE_PER_Y_ITERATION)
                    if EVENT_ALERTS[1]:
                        print("A cell died due to underpopulation.")
                    changes_this_iteration += 1
                if cell.alive_neighbours in (2,3):
                    # correct population
                    if EVENT_ALERTS[2]:
                        print("A cell survived.")
                    continue
                if cell.alive_neighbours > 3:
                    if EVENT_ALERTS[0]:
                        print("A cell died due to overpopulation")
                    # overpopulation
                    cell.kill(CHANGE_PER_X_ITERATION, CHANGE_PER_Y_ITERATION)
                    changes_this_iteration += 1
            else:
                if cell.alive_neighbours == 3:
                    cell.resurrect(CHANGE_PER_X_ITERATION, CHANGE_PER_Y_ITERATION)
                    if EVENT_ALERTS[3]:
                        print("A cell was born.")
                    changes_this_iteration += 1

    print(changes_this_iteration)
    if changes_this_iteration == 0:
        turtle.penup()
        turtle.goto(0,0)
        turtle.pendown()
        turtle.color("yellow")
        turtle.write("The simulation has finished.", font=("Verdana",
                            35, "bold"), align="center")
        turtle.hideturtle()
        time.sleep(10)
        exit()


    if TRACK_GENERATION_TIME:
        time_2 = time.time()
        print(f"Generation finished, took {time_2 - time_1} seconds.")

    if not AUTO_CONTINUE:
        input("Press enter to continue to the next generation. ")



def screen_clicked(x, y):
    if simulation_started:
        return

    for box in boxes:
        if (x,y) in box.entire_box:
            if box.alive:
                box.kill(CHANGE_PER_X_ITERATION, CHANGE_PER_Y_ITERATION)
                return
            else:
                box.resurrect(CHANGE_PER_X_ITERATION, CHANGE_PER_Y_ITERATION)
                return
    while True:
        update_board(current_game_board=game_board)

if RANDOM_CELLS:
    for box in boxes:
        if random.randint(1,100) <= RANDOM_CELL_ALIVE_WEIGHTING:
            box.resurrect(CHANGE_PER_X_ITERATION, CHANGE_PER_Y_ITERATION)
    while True:
        update_board(current_game_board=game_board)
else:
    turtle.onscreenclick(screen_clicked)

turtle.done()

