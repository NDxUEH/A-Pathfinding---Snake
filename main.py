# importing libraries
import pygame
import random
import math

# ------------ Functions --------------#


def create_grid_blocked_cells(window_x, window_y, num_block):
    # defining grid_cells, blocked_cells,
    grid_cells = [[x, y] for x in range(0, window_x, 10) for y in range(0, window_y, 10)]
    random.seed(42)
    blocked_cells = random.sample(grid_cells, num_block)
    return grid_cells, blocked_cells


class Node:
    def __init__(self, current_pos, previous_pos, g, h):
        self.current_pos = current_pos
        self.previous_pos = previous_pos
        self.h = h
        self.g = g

    def f(self):
        return self.h + self.g


def choose_best_node(open_set):
    # choose the node with the minimum f value (f = g + h)
    return min(open_set, key=lambda x: x.f())


def get_heuristic(current_position):
    # return euclidean distance between current node and fruit_position
    return math.sqrt((current_position[0] - fruit_position[0])**2 + (current_position[1] - fruit_position[1])**2)


def get_adjacent_node(node):
    adjacent_node = []

    for dir in DIRECTIONS:
        new_pos = [node.current_pos[0] + dir[0], node.current_pos[1] + dir[1]]
        if 0 <= new_pos[0] <= 590 and 0 <= new_pos[1] <= 590:
            adjacent_node.append(Node(new_pos, node.current_pos, node.g + 1, get_heuristic(new_pos)))

    return adjacent_node


def get_path(current_node, close_set):
    path = []
    node = current_node
    while node.current_pos != START:
        path.append(node.current_pos)
        node_previous = node.previous_pos
        for close_node in close_set:
            if close_node.current_pos == node_previous:
                node = close_node
                break

    # Return reversed path as we need to show from start to end path
    path = path[::-1]
    return path


def is_blocked(node):
    blocked = False
    if node.current_pos in BLOCKED_CELLS:
        blocked = True
    return blocked


def main(start_position):
    open = [Node(start_position, start_position, 0, get_heuristic(START))]   # nodes are possible to move
    close = []  # nodes we have moved to and don't care further

    while True:
        current_node = choose_best_node(open)
        node_index = open.index(current_node)   # get index of current node
        close.append(current_node)  # add current_node to close set

        if current_node.current_pos == fruit_position:  # if snake reaches destination return path
            return get_path(current_node, close)

        adjacent_node = get_adjacent_node(current_node)   # get nodes around current node

        for node in adjacent_node:
            if is_blocked(node) or node.current_pos in snake_body or node.current_pos in close or node.current_pos in open:
                continue
            open.append(node)
        del open[node_index]  # delete current node in open set


if __name__ == "__main__":

    snake_speed = 15
    # Window size
    window_x = 600
    window_y = 600
    # create blocked cells
    GRID_CELLS, BLOCKED_CELLS = create_grid_blocked_cells(window_x, window_y, 130)

    # cells not in block_cells
    EXCLUDED_CELLS = [element for i, element in enumerate(GRID_CELLS) if element not in BLOCKED_CELLS]

    # defining colors
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    pink = pygame.Color(255, 0, 255)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 255, 255)

    # Initialising pygame
    pygame.init()

    # Initialise game window
    pygame.display.set_caption('A* Pathfinding Algorithm - Snake Game')
    game_window = pygame.display.set_mode((window_x, window_y))

    # FPS (frames per second) controller
    fps = pygame.time.Clock()

    # defining snake default position
    snake_position = [100, 50]

    # defining 8 blocks of snake body and suppose that snake body doesn't grow his size even if he eats fruits
    # because we want to focus on pathfinding algorithm and to avoid any unexpected situations
    snake_body = [[100, 50],  # <-- snake_body[0] is a head of snake
                  [90, 50],
                  [80, 50],
                  [70, 50],
                  [60, 50],
                  [50, 50],
                  [40, 50],
                  [30, 50]
                  ]

    # Defining 4 directions: up, down, right, left
    DIRECTIONS = [[10, 0],  # right
                  [0, 10],  # down
                  [-10, 0],  # left
                  [0, -10]]  # up

    # Initialise a fruit position
    fruit_position = random.choice(EXCLUDED_CELLS)
    fruit_spawn = False

    # Initialise some entry points
    snake_move = True
    START = snake_body[0]
    step = 0
    dest = True

    # run first main function
    path = main(START)
    running = True
    # main loop
    while running:
        # key event
        for event in pygame.event.get():
           # closing events
            if event.type == pygame.QUIT:
                running = False

        if snake_move:
            snake_body.insert(0, path[step])
            snake_body.pop()
            if snake_body[0] != fruit_position:
                step += 1
                fruit_spawn = False  # fruit_spawn = False -> snake doesn't reach fruit_position
            else:
                step = 0
                START = snake_body[0]
                fruit_spawn = True

        game_window.fill(white)

        if fruit_spawn:  # fruit_spawn = True -> snake reaches fruit_position
            while True:
                # random fruit position
                fruit_position = random.choice(EXCLUDED_CELLS)
                if fruit_position in snake_body:  # not use fruit_position which in snake_body
                    continue
                else:
                    path = main(START)
                    fruit_spawn = False
                    break

        # blocked draw
        for b in BLOCKED_CELLS:
            pygame.draw.rect(game_window, black, [b[0], b[1], 10, 10])

        # fruit draw
        if dest:
            pygame.draw.rect(game_window, green, [fruit_position[0], fruit_position[1], 10, 10])

        # snake draw
        count = len(snake_body) - 1
        while count >= 0:
            if count == 0:  # draw a head of snake -> pink color
                pygame.draw.rect(game_window, pink, [snake_body[count][0], snake_body[count][1], 10, 10])
            else:   # draw body snake -> blue color
                pygame.draw.rect(game_window, blue, [snake_body[count][0], snake_body[count][1], 10, 10])
            count -= 1

        # update display--- required
        pygame.display.update()
        fps.tick(snake_speed)

    pygame.quit()
    quit()


