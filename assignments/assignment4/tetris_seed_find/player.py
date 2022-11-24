from board import Direction, Rotation, Action, Shape
from random import Random
from exceptions import NoBlockException
import time
import weights

# https://engf0002.cs.ucl.ac.uk/submissions/tetris

class Player:
    def choose_action(self, board):
        raise NotImplementedError


def print_board(board):
    print("--------")
    print(board.cells)
    for y in range(24):
        s = ""
        for x in range(10):
            if (x,y) in board.cells:
                s += "#"
            else:
                s += "."
        print(s, y)


def height(sandbox, falling=None):
    height = 0
    test = sandbox.cells.copy()
    if falling:
        test.update(falling)
    for cell in test:
        height = max(height, 24-cell[1])
    return height


class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        print("========")
        print("print_board")
        print_board(board)
        print("board.falling.shape")
        print(board.falling.shape)
        print("board.falling.cells")
        print(board.falling.cells)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])

# incorrect
class greedyScorePlayer(Player):
    def __init__(self):
        pass

    def sandbox_trial(self, board):
        sandbox = board.clone()
        actions = [Direction.Left, 
                   Direction.Right, 
                   Direction.Down, 
                   Rotation.Anticlockwise, 
                   Rotation.Clockwise,
                   Action.Discard,
                   Action.Bomb]
        highest_score = 0
        best_action = None
        for action in actions:
            if action in [Direction.Left, Direction.Right, Direction.Down, Action.Discard, Action.Bomb]:
                sandbox.move(action)
            else:
                sandbox.rotate(action)
            if sandbox.score > highest_score:
                highest_score = sandbox.score
                best_action = action
            sandbox = board.clone()
        return best_action

    def choose_action(self, board):
        return self.sandbox_trial(board)

# only foresee 1 step: 278
class greedyHeightPlayer(Player):
    def __init__(self):
        pass
    def print_board(self, board):
        print(board.cells)
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)

    # height of dropped blocks
    def height(self, sandbox, falling=None):
        height = 0
        test = sandbox.cells.copy()
        if falling:
            test.update(falling)
        for cell in test:
            height = max(height, 24-cell[1])
        return height

    def sandbox_trial(self, board):
        sandbox = board.clone()
        actions = [Direction.Down, 
                   Direction.Left, 
                   Direction.Right, 
                   Rotation.Anticlockwise, 
                   Rotation.Clockwise,
                   Action.Discard,
                   Action.Bomb]
        lowest_height = 100
        best_action = None
        for action in actions:
            if action in [Direction.Left, Direction.Right, Direction.Down, Action.Discard, Action.Bomb]:
                sandbox.move(action)
            else:
                sandbox.rotate(action)
            if self.height(sandbox) < lowest_height:
                lowest_height = self.height(sandbox)
                best_action = action
            sandbox = board.clone()
        return best_action

    def choose_action(self, board):
        # time.sleep(0.1)
        self.print_board(board)
        print(self.height(board))
        return self.sandbox_trial(board)


# foresee current block until it's dropped: 700+
class greedyHeightDroppedPlayer(Player):
    def __init__(self):
        pass

    def sandbox_trial(self, board):
        lowest_height = 100
        best_actions = []
        for right in range(-4, 4):
            # iterate possible horizontal moves
            for rotate in range(4):
                # iterate possible rotations
                this_actions = []
                sandbox = board.clone()
                try:
                    for i in range(rotate):  # rotate
                        sandbox.rotate(Rotation.Clockwise)
                        this_actions.append(Rotation.Clockwise)
                    if right < 0:
                        for i in range(-right):  # move left
                            sandbox.move(Direction.Left)
                            this_actions.append(Direction.Left)
                    elif right > 0:
                        for i in range(right):  # move right
                            sandbox.move(Direction.Right)
                            this_actions.append(Direction.Right)

                    sandbox.move(Direction.Drop)  # drop to the ground
                    this_actions.append(Direction.Drop)
                except NoBlockException:
                    pass
                if height(sandbox) < lowest_height:
                    lowest_height = height(sandbox)
                    best_actions = this_actions
        return best_actions  # return actions makes the lowest height

    def choose_action(self, board):
        # time.sleep(0.1)
        print_board(board)
        print(height(board))
        return self.sandbox_trial(board)


class greedyStepScoringPlayer(Player):
    def __init__(self):
        self.height_penalty = weights.height_penalty
        self.well_penalty = weights.well_penalty
        self.roughness_penalty = weights.roughness_penalty
        self.row_weigh_by_level = [0, 25, 100, 400, 1600]
        self.row_general = weights.row_general
        pass

    # provide a sandbox, returns the number of blocks in the well
    def count_wells(self, sandbox):
        num_well_blocks = 0
        for x in range(0, 10):
            for y in range(1, 24):
                if (x, y) in sandbox.cells:
                    # detect empty cells below
                    for y2 in range(y+1, 24):
                        if (x, y2) not in sandbox.cells:
                            num_well_blocks += 1
                        else:
                            break
        return num_well_blocks

    def count_cleared_rows(self, board, sandbox):
        increment_cells = len(sandbox.cells) - len(board.cells)
        if increment_cells >= 4:
            # print("increment_cells", increment_cells)
            return 0
        else:
            cleared_rows = (-increment_cells+4)//10
            # print("cleared_rows", cleared_rows)
            return cleared_rows

    def eval_roughness(self, sandbox):
        roughness = 0
        highest = [0 for _ in range(10)]
        for cell in sandbox.cells:
            highest[cell[0]] = max(highest[cell[0]], cell[1])
        for i in range(9):
            roughness += abs(highest[i] - highest[i+1])
        return roughness

    def scorer(self, board, sandbox):
        # print("scorer")
        # print_board(sandbox)
        # check if there is line cleared
        score = 0

        num_cleared_rows = self.count_cleared_rows(board, sandbox)
        score += self.row_weigh_by_level[num_cleared_rows] * num_cleared_rows

        height_difference = height(sandbox)-height(board)
        score -= max(0, height_difference+num_cleared_rows)*self.height_penalty

        wells = self.count_wells(sandbox)
        score -= wells*self.well_penalty

        roughness = self.eval_roughness(sandbox)
        score -= roughness*self.roughness_penalty
        return score


    def sandbox_trial(self, board):
        highestScore = -100000
        best_actions = []
        for right in range(-5, 4):
            # iterate possible horizontal moves
            for rotate in range(4):
                this_actions = []
                sandbox = board.clone()
                try:
                    if rotate == 3:
                        sandbox.rotate(Rotation.Anticlockwise)
                        this_actions.append(Rotation.Anticlockwise)
                    else:
                        for j in range(rotate):
                            sandbox.rotate(Rotation.Clockwise)
                            this_actions.append(Rotation.Clockwise)

                    if right < 0:
                        for i in range(-right):  # move left
                            sandbox.move(Direction.Left)
                            this_actions.append(Direction.Left)
                    elif right > 0:
                        for i in range(right):  # move right
                            sandbox.move(Direction.Right)
                            this_actions.append(Direction.Right)

                    sandbox.move(Direction.Drop)  # drop to the ground
                    this_actions.append(Direction.Drop)

                except NoBlockException:
                    pass

                if self.scorer(board, sandbox) > highestScore:
                    highestScore = self.scorer(board, sandbox)
                    # print("highestScore", highestScore)
                    best_actions = this_actions

        return best_actions  # return actions makes the lowest height

    def choose_action(self, board):
        # time.sleep(0.01)
        # print_board(board)
        # print(height(board))
        # print("====================================")
        return self.sandbox_trial(board)

class manualTestPlayer(Player):
    def __init__(self):
        pass

    def choose_action(self, board):
        # time.sleep(0.1)
        # print_board(board)
        return [Direction.Left, Direction.Right, Rotation.Clockwise, Direction.Drop]


SelectedPlayer = greedyStepScoringPlayer
