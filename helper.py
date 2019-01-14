"""
Created by Rachel Xu, last updated on 05/01/2015
"""
from random import *
from copy import deepcopy
from itertools import product
import math

# Offsets for computing tile indices in each direction.
OFFSETS = {'UP': (1, 0),
           'DOWN': (-1, 0),
           'LEFT': (0, 1),
           'RIGHT': (0, -1)}
DEPTH = 1


def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    r1 = [0] * 4
    r2 = []
    pos1, pos2 = 0, 0
    score = 0

    for num in line:
        if num != 0:
            r1[pos1] = num
            pos1 += 1

    while len(r1) > 1:
        if r1[pos2] == r1[pos2 + 1]:
            r2.append(r1[pos2] * 2)
            score += r1[pos2]
            del r1[pos2:pos2 + 2]
        else:
            r2.append(r1[pos2])
            del r1[pos2]

    r2 += r1

    if len(r2) < len(line):
        r2.extend([0] * (len(line) - len(r2)))
    r2.append(score)

    return r2


def std(lst):
    """
    Helper function that calculates the standard deviation of a numeric sequence
    """
    average = sum(lst) / float(len(lst))
    variance = sum(list(map(lambda x: (x - average) ** 2, lst))) / float(len(lst))
    stdev = math.sqrt(variance)

    return stdev


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.numCol = grid_height
        self.numRow = grid_width
        self.grid = []
        self.actualScore = 0
        self.bestScores = []

        for i in range(self.numRow):
            print([0] * self.numCol)
            self.grid.append([0] * self.numCol)

        for i in range(2):
            self.new_tile()
            # print(self.heuristic_score())

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.actualScore = 0
        for i in range(self.numRow):
            for j in range(self.numCol):
                self.grid[i][j] = 0

        for i in range(2):
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        rep = ""
        g = deepcopy(self.grid)
        for i in range(self.numRow):
            for j in range(self.numCol):
                g[i][j] = str(g[i][j])

        for row in g:
            rep = rep + "   ".join(row) + "\n" * 2

        return rep

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.numRow

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.numCol

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        initialTilesDictionary = {
            'UP': [(0, 0), (0, 1), (0, 2), (0, 3)],
            'DOWN': [(3, 0), (3, 1), (3, 2), (3, 3)],
            'LEFT': [(0, 0), (1, 0), (2, 0), (3, 0)],
            'RIGHT': [(0, 3), (1, 3), (2, 3), (3, 3)]
        }
        initialTiles = initialTilesDictionary[direction]

        for tile in initialTiles:
            l = [tile]
            line = [int(self.get_tile(*tile))]
            i = 0
            while i < 3:
                c = OFFSETS[direction]
                nextTile = (tile[0] + c[0], tile[1] + c[1])
                l.append(nextTile)
                line.append(int(self.get_tile(*nextTile)))
                tile = nextTile
                i += 1
            mergedLine = merge(line)[:-1]
            self.actualScore += 2 * merge(line)[-1]
            for i in range(4):
                self.set_tile(l[i][0], l[i][1], mergedLine[i])

        self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        seq = [2] * 9 + [4]
        newTile = choice(seq)
        emptySquareList = self.empty_cells()
        emptySquare = choice(emptySquareList)
        self.grid[emptySquare[0]][emptySquare[1]] = newTile

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]

    def heuristic_score(self):
        """
        Calculate the heuristic score by combining several
        other scores to evaluate each game state.
        """
        maxValue = math.log(self.getMaxTile()) * self.number_of_empty_cells() / math.log(2)
        emptyScore = (math.log(self.number_of_empty_cells()) / math.log(
            2)) * 5 if self.number_of_empty_cells() != 0 else 0
        score = emptyScore + maxValue + (self.distance(self.getMaxTile()) * 10) - math.sqrt(
            self.hscore()) + self.smoothness() * 0.1
        #  + self.actualScore + \
        #         math.log(self.actualScore+1)*self.number_of_empty_cells()
        # +math.sqrt(self.hscore()) + self.distance(self.getMaxTile()) * 10
        # score = self.actualScore + \
        #         math.log(self.actualScore+1)*self.number_of_empty_cells() - math.sqrt(self.hscore())
        return score

    def smoothness(self):

        smoothness = 0

        for x in xrange(4):
            for y in xrange(4):
                s = float('infinity')

                if x > 0:
                    s = min(s, abs((self.grid[x][y] or 2) - (self.grid[x - 1][y] or 2)))
                if y > 0:
                    s = min(s, abs((self.grid[x][y] or 2) - (self.grid[x][y - 1] or 2)))
                if x < 3:
                    s = min(s, abs((self.grid[x][y] or 2) - (self.grid[x + 1][y] or 2)))
                if y < 3:
                    s = min(s, abs((self.grid[x][y] or 2) - (self.grid[x][y + 1] or 2)))

                smoothness -= s

        return smoothness

    def empty_cells(self):
        """
        Return a list of empty cells.
        """
        emptySquareList = []
        for row in range(self.numRow):
            for col in range(self.numCol):
                if self.grid[row][col] == 0:
                    emptySquareList.append([row, col])

        return emptySquareList

    # Return the Tile with Maximum Value
    def getMaxTile(self):
        maxTile = 0

        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                maxTile = max(maxTile, self.grid[x][y])

        return maxTile

    def distance(self, max_tile):
        dis = None

        for x in range(len(self.grid)):

            if dis:
                break

            for y in range(len(self.grid)):
                if max_tile == self.grid[x][y]:

                    if max_tile < 1024:
                        dis = -((abs(x - 0) + abs(y - 0)) * max_tile)
                    else:
                        dis = -((abs(x - 0) + abs(y - 0)) * (max_tile / 2))
                    break
        return dis

    def number_of_empty_cells(self):
        """
        Calculate the number of empty cells in the grid.
        """
        return len(self.empty_cells())

    def on_the_board(self, row, col):
        if row in range(4) and col in range(4):
            return True
        else:
            return False

    def hscore(self):
        """
        Measure how scattered the values of the board are.
        """
        count = {}
        entropy = 0
        nonZero = self.numRow * self.numCol - self.number_of_empty_cells()
        for row in range(self.numRow):
            for col in range(self.numCol):
                if self.grid[row][col] != 0:
                    if self.grid[row][col] in count:
                        count[self.grid[row][col]] += 1
                    else:
                        count[self.grid[row][col]] = 1
        for k in count.keys():
            freq = count[k] / float(nonZero)
            entropy -= freq * math.log(freq)
        entropy /= math.log(self.numRow * self.numCol)

        return nonZero + entropy

    def test_move(self, direction):
        """
        Check if a certain move changes the game state
        """
        t = deepcopy(self)
        t.move(direction)

        return t.grid == self.grid

    def game_over(self):
        """
        Check if the there's any further step that can be taken
        (or if the game has reached its final state)
        """
        gameOver = True
        for direction in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            try:
                a = self.test_move(direction)
                if not a:
                    return False
            except IndexError:
                pass
        return gameOver and not self.number_of_empty_cells()

    def a_maximize(self, t, alpha, beta, depth):
        if t.game_over() == True or depth == 0:
            return t.heuristic_score()
        maxUtility = -float('inf')
        d = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for direction in d:
            c = deepcopy(t)
            try:
                c.move(direction)
            except IndexError:
                break
            maxUtility = max(maxUtility, t.a_minimize(c, alpha, beta, depth - 1))
            if maxUtility >= beta:
                break
            alpha = max(maxUtility, alpha)
        return maxUtility

    def a_minimize(self, t, alpha, beta, depth):
        if t.game_over() == True or depth == 0:
            return t.heuristic_score()
        minUtility = float('inf')
        emptyCells = self.empty_cells()
        children = []
        for c in emptyCells:
            gridCopy = deepcopy(t)
            gridCopy.set_tile(c[0], c[1], 2)
            children.append(gridCopy)
            gridCopy = deepcopy(t)
            gridCopy.set_tile(c[0], c[1], 4)
            children.append(gridCopy)
        for child in children:
            minUtility = min(minUtility, t.a_maximize(child, alpha, beta, depth - 1))
            if minUtility <= alpha:
                break
            beta = min(minUtility, beta)
            # print minUtility
        return minUtility

    def maximize(self, t, depth):
        if t.game_over() == True or depth == 0:
            return t.heuristic_score()
        maxUtility = -float('inf')
        d = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for direction in d:
            c = deepcopy(t)
            try:
                c.move(direction)
            except IndexError:
                break
            maxUtility = max(maxUtility, self.minimize(c, depth - 1))
            # print maxUtility
        return maxUtility

    def minimize(self, t, depth):
        if t.game_over() == True or depth == 0:
            return t.heuristic_score()
        minUtility = float('inf')
        emptyCells = t.empty_cells()
        children = []
        for c in emptyCells:
            grid2 = deepcopy(t)
            grid4 = deepcopy(t)
            grid2.set_tile(c[0], c[1], 2)
            children.append(grid2)
            grid4.set_tile(c[0], c[1], 4)
            children.append(grid4)
        for child in children:
            minUtility = min(minUtility, self.maximize(child, depth - 1))
            # print minUtility
        return minUtility

    # self.depth = 1
    def minimax(self, grid, max, startDepth):
        if max:
            # print('mini')
            return self.maximize(grid, startDepth)
        else:
            return self.minimize(grid, startDepth)

    def alphaBeta(self, grid, max, startDepth):
        if max:
            return self.a_maximize(grid, -float('inf'), float('inf'), startDepth)
        else:
            return self.a_minimize(grid, -float('inf'), float('inf'), startDepth)


def Run2048():
    t = TwentyFortyEight(4, 4)
    startDepth = 4
    while t.game_over() != True:
        print ('game over or not', t.game_over())
        ans = -float('inf')
        d = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        # while(t.game_over()!=True):
        for direction in d:
            child = deepcopy(t)
            utility = child.alphaBeta(child, True, startDepth)
            if utility >= ans:
                ans = utility
                print('the depth is', startDepth)
                for i in range(len(t.grid)):
                    print(t.grid[i])
                print ('\n\n')
                try:
                    t.move(direction)
                except IndexError:
                    break
                print ('hello')
        if (ans == -float('inf')):
            break
        print('the answer is', ans)

        # if ans==-float('inf')


        # print('the value is',  t.minimax(t, True))

        # while i < 60 and not t.game_over():
        #     hScores = {}
        #     d = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        #     for direction in list(product(d, d, d)):
        #         hScores[direction] = 0
        #         c = deepcopy(t)
        #         for j in range(len(direction)):
        #             try:
        #                 c.move(direction[j])
        #                 hScores[direction] += c.hscore()
        #             except IndexError:
        #                 break
        #
        #     hScoreList = sorted(hScores.values())
        #     for key in hScores.keys():
        #         if hScores[key] == hScoreList[0]:
        #             direc = key
        #     for k in range(len(direc)):
        #         try:
        #             t.move(direc[k])
        #         except IndexError:
        #             break
        #     i += 1
        # j = 0
        # while j < 50 and not t.game_over():
        #     for dir in ['DOWN', 'LEFT', 'DOWN', 'RIGHT']:
        #         try:
        #             t.move(dir)
        #         except IndexError:
        #             break
        #         j += 1
        # return t


print(Run2048())

##total = []
##for i in range(100):
##    total.append(run2048())
# print(sum(total)/100)
