from copy import deepcopy

# create global variables
open_plus_closed_length = 0
closed_length = 0


class Puzzle:
    # puzzle class to contain all information about a singular node
    def __init__(self, puzzle, parent):
        self.board = puzzle
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0


def a_star(initial_puzzle, goal, heuristic):
    nodes_to_visit = []
    visited_nodes = []
    global open_plus_closed_length
    global closed_length

    # add initial puzzle to list of nodes to visit
    nodes_to_visit.append(initial_puzzle)

    # until nodes to visit is empty, search list
    while nodes_to_visit:

        # find node with the lowest f in the list of nodes to visit
        nodes_to_visit.sort(key=lowest_f)
        current_node = nodes_to_visit[0]

        # check node isn't the goal state
        if current_node.board == goal:
            open_plus_closed_length = len(nodes_to_visit) + len(visited_nodes)
            closed_length = len(visited_nodes)
            return current_node

        # remove current node from list of ones to visit and add it to 'already visited'
        nodes_to_visit.remove(current_node)
        visited_nodes.append(current_node)

        # generate succesors of current node by moving zero in every possible direction
        expanded_parent = get_children(current_node)

        # check each of its children
        for child in expanded_parent:
            already_checked = False
            in_nodes_to_visit = False

            # check node hasn't already been checked by searching visited nodes list for it
            for node in visited_nodes:
                if node.board == child.board:
                    already_checked = True
                    break

            if not already_checked:
                childs_g = current_node.g + 1

                # check node isn't already in the list of nodes to visit
                for i in range(len(nodes_to_visit)):
                    if nodes_to_visit[i].board == child.board:
                        in_nodes_to_visit = True

                        # if it is in the list with a g value bigger than its current instance,
                        # update the instance in the list's g, f, and parent to match current instance
                        if childs_g < nodes_to_visit[i].g:
                            nodes_to_visit[i].g = childs_g
                            nodes_to_visit[i].f = nodes_to_visit[i].g + \
                                nodes_to_visit[i].h
                            nodes_to_visit[i].parent = current_node

                # if not, populate child's information and add to list of nodes to visit
                if not in_nodes_to_visit:
                    child.g = childs_g

                    # apply heuristic
                    if(heuristic == 1):
                        child.h = manhattan(child, goal)
                    else:
                        child.h = number_misplaced(child, goal)
                    child.f = child.g + child.h
                    child.parent = current_node
                    nodes_to_visit.append(child)

    return None


def number_misplaced(puzzle, goal):
    # calculate number of tiles out of place
    number = 0
    h = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if(puzzle.board[i][j] != goal[i][j]):
                h += 1
            number += 1
    return h


def manhattan(puzzle, goal):
    # calculate distance each number is away from their goal and total them
    flatten_puzzle = [i for row in puzzle.board for i in row]
    flatten_goal = [j for row in goal for j in row]

    return sum(abs(x % 3 - y % 3) + abs(x//3 - y//3)
               for x, y in ((flatten_puzzle.index(i), flatten_goal.index(i)) for i in range(1, 9)))


def lowest_f(x):
    # helper function for sorting list
    return x.f


def get_children(parent):
    parent = parent.board

    # get x and y coordinates of the zero
    for i in range(3):
        for j in range(3):
            if parent[i][j] == 0:
                x, y = i, j
                break

    # check puzzle can move in any four directions and add that move to list of children
    if y-1 >= 0:
        yield get_left(parent, x, y)
    if y+1 < 3:
        yield get_right(parent, x, y)
    if x-1 >= 0:
        yield get_up(parent, x, y)
    if x+1 < 3:
        yield get_down(parent, x, y)


def get_left(parent, x, y):
    # swap value at coordinates x,y with the value on the left and create this as new child
    child_puzzle = deepcopy(parent)
    child_puzzle[x][y] = child_puzzle[x][y-1]
    child_puzzle[x][y-1] = 0
    child = Puzzle(child_puzzle, parent)
    return child


def get_right(parent, x, y):
    # swap value at coordinates x,y with the value on the right and create this as new child
    child_puzzle = deepcopy(parent)
    child_puzzle[x][y] = child_puzzle[x][y+1]
    child_puzzle[x][y+1] = 0
    child = Puzzle(child_puzzle, parent)
    return child


def get_up(parent, x, y):
    # swap value at coordinates x,y with the value above and create this as new child
    child_puzzle = deepcopy(parent)
    child_puzzle[x][y] = child_puzzle[x-1][y]
    child_puzzle[x-1][y] = 0
    child = Puzzle(child_puzzle, parent)
    return child


def get_down(parent, x, y):
    # swap value at coordinates x,y with the value below and create this as new child
    child_puzzle = deepcopy(parent)
    child_puzzle[x][y] = child_puzzle[x+1][y]
    child_puzzle[x+1][y] = 0
    child = Puzzle(child_puzzle, parent)
    return child


def reconstruct_path(result):
    # traverse result tree from goal, upwards to print the path of the solution

    no_of_moves = 0
    moves = []

    moves.append(result.board)
    parent = result.parent

    while parent:
        no_of_moves += 1
        moves.append(parent.board)
        parent = parent.parent

    moves.reverse()
    for x in moves:
        for move in x:
            print(move)
        print("\n")

    print("Solution Depth: " + str(no_of_moves))


heuristic_choice = int(
    input("Enter 1 for Manhattan, Enter 2 for Misplaced Tiles: "))
start = input(
    "Enter Start State of Puzzle (in form [[x, y, z], [a, b, c], [i, j, k]]: ")
goal = input(
    "Enter Goal State of Puzzle (in form [[x, y, z], [a, b, c], [i, j, k]]: ")

start = Puzzle(eval(start), None)
goal = eval(goal)
result = a_star(start, goal, heuristic_choice)

if result:
    reconstruct_path(result)
else:
    print("No Solution Found")

print("Number of nodes traversed:",  closed_length)
print("Number of expanded nodes:", open_plus_closed_length)
