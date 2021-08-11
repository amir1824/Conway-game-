#Amir Ben Shimol

class Conway:
#Announcement of the start of the game
    print("Welcome to Conway's the game of life")

#Setting up the output
def gameOfLife(array):
    s = []
    for row in array:
        for cell in row:
            s.append('▓▓ ' if cell else '░░ ')
        s.append('\n')
    return ''.join(s)


cell_state_map = {}

#Build the map and operate the bits according to the rules
def build_state_map():
    for i in range(512):
        all_but_center_bit = 0b111101111 & i
        active_bit_count = bin(all_but_center_bit).count('1')

        if active_bit_count < 2:
            cell_state_map[i] = 0
        elif active_bit_count > 3:
            cell_state_map[i] = 0
        elif active_bit_count == 3:
            cell_state_map[i] = 1
        else:
            cell_state_map[i] = 1 if 0b000010000 & i else 0

#The method checks the cell values
def get_cell_value(row, col, cells, empty_universe):
    if row < 0 or row > len(empty_universe) - 1:
        return 0
    if col < 0 or col > len(empty_universe[0]) - 1:
        return 0

    cell_coords = (0, 0)

    if row != 0 and row != len(empty_universe) - 1:
        if col != 0 and col != len(empty_universe[0]) - 1:
            return cells[row - 1][col - 1]

    return empty_universe[row][col]

#The method cuts through the universe and prepares it
def crop_universe(universe, top_left, bottom_right):
    cropped_universe = universe[top_left[0]: bottom_right[0] + 1]
    return list(map(lambda row: row[top_left[1]: bottom_right[1] + 1], cropped_universe))

#The method scans the list according to established rules and re-divides by generations
def get_generation(cells, generations):
    if generations == 0:
        return cells

    build_state_map()
    top_left = [-1, -1]
    bottom_right = [-1, -1]

    for g in range(generations):
        empty_universe = [[0] * (len(cells[0]) + 2) for _ in range(len(cells) + 2)]
        for row in range(len(empty_universe)):
            for col in range(len(empty_universe[0])):
                cell_state = 0

                for i in range(-1, 2):
                    for j in range(-1, 2):
                        cell_state |= get_cell_value(row + i, col + j, cells, empty_universe)
                        cell_state <<= 1

                cell_state >>= 1
                next_state = cell_state_map[cell_state]

                # Keep track of top left and bottom right coords of live cells for cropping
                if next_state and g == generations - 1:
                    if top_left[0] == -1:
                        top_left[0] = row
                        top_left[1] = col
                        bottom_right[0] = row
                        bottom_right[1] = col

                    if col < top_left[1]:
                        top_left[1] = col

                    if row > bottom_right[0]:
                        bottom_right[0] = row

                    if col > bottom_right[1]:
                        bottom_right[1] = col

                empty_universe[row][col] = next_state

        cells = empty_universe

    return crop_universe(cells, top_left, bottom_right)

#This list has all the cases:
#1. Died of loneliness
#2. Density dies
#3. Rise to life
#4. Survives
input_board_state = [
    [0,1,0],
    [0,1,1],
    [1,0,1],
    [0,0,0]

]


#The first generation before the game
print("this is the start generation:",'\n',input_board_state)
#The user selects the number of generations
generation_count = (int)(input("Please enter your next(up) generation you want"))
#Print the method
output_board_state = get_generation(input_board_state, generation_count)
print(gameOfLife(output_board_state))


