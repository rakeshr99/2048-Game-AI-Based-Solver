#
# CS1010FC --- Programming Methodology
#
# Mission N Solutions
#
# Note that written answers are commented out to allow us to run your
# code easily while grading your problem set.
from random import *
from copy import deepcopy
import math
import random
#######
#Task 1a#
#######

# [Marking Scheme]
# Points to note:
# Matrix elements must be equal but not identical
# 1 mark for creating the correct matrix

def new_game(n):
    matrix = []

    for i in range(n):
        matrix.append([0] * n)
    return matrix

###########
# Task 1b #
###########

# [Marking Scheme]
# Points to note:
# Must ensure that it is created on a zero entry
# 1 mark for creating the correct loop

def new_tile(mat):
    seq = [2] * 90 + [4]
    newTile = choice(seq)
    emptySquareList = empty_cells(mat)
    emptySquare = choice(emptySquareList)
    mat[emptySquare[0]][emptySquare[1]] = newTile
    return mat

###########
# Task 1c #
###########

# [Marking Scheme]
# Points to note:
# Matrix elements must be equal but not identical
# 0 marks for completely wrong solutions
# 1 mark for getting only one condition correct
# 2 marks for getting two of the three conditions
# 3 marks for correct checking

def game_state(mat):
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j]==2048:
                return 'win'
    for i in range(len(mat)-1): #intentionally reduced to check the row on the right and below
        for j in range(len(mat[0])-1): #more elegant to use exceptions but most likely this will be their solution
            if mat[i][j]==mat[i+1][j] or mat[i][j+1]==mat[i][j]:
                return 'not over'
    for i in range(len(mat)): #check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j]==0:
                return 'not over'
    for k in range(len(mat)-1): #to check the left/right entries on the last row
        if mat[len(mat)-1][k]==mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1): #check up/down entries on last column
        if mat[j][len(mat)-1]==mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

###########
# Task 2a #
###########

# [Marking Scheme]
# Points to note:
# 0 marks for completely incorrect solutions
# 1 mark for solutions that show general understanding
# 2 marks for correct solutions that work for all sizes of matrices

def reverse(mat):
    new=[]
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

###########
# Task 2b #
###########

# [Marking Scheme]
# Points to note:
# 0 marks for completely incorrect solutions
# 1 mark for solutions that show general understanding
# 2 marks for correct solutions that work for all sizes of matrices

def transpose(mat):
    new=[]
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

##########
# Task 3 #
##########

# [Marking Scheme]
# Points to note:
# The way to do movement is compress -> merge -> compress again
# Basically if they can solve one side, and use transpose and reverse correctly they should
# be able to solve the entire thing just by flipping the matrix around
# No idea how to grade this one at the moment. I have it pegged to 8 (which gives you like,
# 2 per up/down/left/right?) But if you get one correct likely to get all correct so...
# Check the down one. Reverse/transpose if ordered wrongly will give you wrong result.

def cover_up(mat):
    new=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    done=False
    for i in range(4):
        count=0
        for j in range(4):
            if mat[i][j]!=0:
                new[i][count]=mat[i][j]
                if j!=count:
                    done=True
                count+=1
    return (new,done)

def merge(mat):
    score = 0
    done=False
    for i in range(4):
         for j in range(3):
             if mat[i][j]==mat[i][j+1] and mat[i][j]!=0:
                 score += mat[i][j] * 2
                 mat[i][j]*=2
                 mat[i][j+1]=0
                 done=True
    return (mat,done, score)


def empty_cells(mat):
    """
    Return a list of empty cells.
    """
    emptySquareList = []
    for row in range(len(mat)):
        for col in range(len(mat[0])):
            if mat[row][col] == 0:
                emptySquareList.append([row, col])

    return emptySquareList

def getMaxTile(mat):
    maxTile = 0
    for x in range(len(mat)):
        for y in range(len(mat[x])):
            maxTile = max(maxTile, mat[x][y])

    return maxTile

def heuristic_score(mat):
    number_of_empty_cells = len(empty_cells(mat))
    score = monotonicity(mat)*1.5 + number_of_empty_cells*2 +  + getMaxTile(mat)
    return score

def monotonicity(grid):
    grid_mask = [[2048, 1024, 256, 64],
                 [1024, 256, 64, 16],
                 [256, 64, 16, 4],
                 [64, 16, 4, 1]]

    monotonicity_score = 0
    for row in range(3):
        for column in range(3):
            monotonicity_score += grid[row][column] * grid_mask[row][column]
    return monotonicity_score


def distance(mat, max_tile):
    dis = None

    for x in range(len(mat)):

        if dis:
            break

        for y in range(len(mat)):
            if max_tile == mat[x][y]:

                if max_tile < 1024:
                    dis = -((abs(x - 0) + abs(y - 0)) * max_tile)
                else:
                    dis = -((abs(x - 0) + abs(y - 0)) * (max_tile / 2))
                break
    return dis


def a_maximize(mat, alpha, beta, depth):
    if game_state(mat)=='lose' or depth == 0:
        return heuristic_score(mat)
    maxUtility = -float('inf')
    d = ['up', 'down', 'left', 'right']
    for direction in d:
        c = deepcopy(mat)
        try:
            c, done = move(c, direction)
            if done:
                maxUtility = max(maxUtility, a_minimize(c, alpha, beta, depth-1 ))
        except IndexError:
            print("error-----------------------------------------------------------------------------")
            continue
        alpha = max(maxUtility, alpha)
        if alpha >= beta:
            break
    return maxUtility

def alphaBeta(grid, max, startDepth):
    if max:
        return a_maximize(grid, -float('inf'), float('inf'), startDepth)
    else:
        return a_minimize(grid, -float('inf'), float('inf'), startDepth)


def minimax(grid, max, startDepth):
    if max:
        return maximize(grid, startDepth)
    else:
        return minimize(grid, startDepth)


def maximize(mat, depth):
    if game_state(mat)=='lose' or depth == 0:
        return heuristic_score(mat)
    maxUtility = -float('inf')
    d = ['up', 'down', 'left', 'right']
    for direction in d:
        c = deepcopy(mat)
        try:
            c, done = move(c, direction)
            if done:
                maxUtility = max(maxUtility, minimize(c, depth - 1))
        except IndexError:
            continue
    return maxUtility


def minimize(mat, depth):
    if game_state(mat)=='lose' or depth == 0:
        return heuristic_score(mat)
    minUtility = float('inf')
    emptyCells = empty_cells(mat)
    children = []
    for c in emptyCells:
        gridCopy = deepcopy(mat)
        gridCopy = set_tile(gridCopy, c[0], c[1], 2)
        children.append(gridCopy)
        gridCopy = deepcopy(mat)
        gridCopy = set_tile(gridCopy, c[0], c[1], 4)
        children.append(gridCopy)
    for child in children:
        minUtility = min(minUtility, maximize(child, depth - 1))

        # print minUtility
    return minUtility

def a_minimize(mat, alpha, beta, depth):
    if game_state(mat)=='lose' or depth == 0:
        return heuristic_score(mat)
    minUtility = float('inf')
    emptyCells = empty_cells(mat)
    children = []
    for c in emptyCells:
        gridCopy = deepcopy(mat)
        gridCopy = set_tile(gridCopy, c[0], c[1], 2)
        children.append(gridCopy)
        gridCopy = deepcopy(mat)
        gridCopy = set_tile(gridCopy, c[0], c[1], 4)
        children.append(gridCopy)
    for child in children:
        minUtility = min(minUtility, a_maximize(child, alpha, beta, depth - 1))
        if minUtility <= alpha:
            break
        beta = min(minUtility, beta)
        # print minUtility
    return minUtility

def montecarlo(mat, initialScore):
    scores = []
    for i in range(0, 100):
        directions = ['up', 'down', 'left', 'right']
        direction = directions[random.randint(0, len(directions) - 1)]
        newMat = deepcopy(mat)
        gameScore = initialScore
        while game_state(newMat)!='lose':
            try:
                newMat, done, score = move(newMat, direction)
                newMat = new_tile(newMat)
                gameScore+=score+heuristic_score(mat)
            except IndexError:
                break
        scores.append(gameScore)
    return sum(scores)/len(scores)

def expectimax(mat, depth, maximizer):
    if depth==0:
        return heuristic_score(mat)
    if maximizer:
        currentValue = -1
        d = ['up', 'down', 'left', 'right']
        for direction in d:
            newBoard =  deepcopy(mat)
            newBoard, done, score = move(newBoard, direction)
            calculatedValue = expectimax(newBoard, depth - 1, False)
            if calculatedValue > currentValue:
                currentValue = calculatedValue
        return currentValue
    else:
        number = 0
        sum_value = 0
        emptyCells = empty_cells(mat)
        children = []
        for c in emptyCells:
            gridCopy = deepcopy(mat)
            gridCopy = set_tile(gridCopy, c[0], c[1], 2)
            children.append(gridCopy)
            gridCopy = deepcopy(mat)
            gridCopy = set_tile(gridCopy, c[0], c[1], 4)
            children.append(gridCopy)
        for child in children:
            sum_value+= expectimax(child, depth-1, True)
            number+=1
        if number == 0:
            return expectimax(mat, depth-1, True)
        return (sum_value/number)

def set_tile(mat, row, col, value):
    """
    Set the tile at position row, col to have the given value.
    """
    mat[row][col] = value
    return mat
def move(game, direction):
    if(direction=="up"):
        return up(game)
    elif direction=="down":
        return down(game)
        # down(game)
    elif direction == "left":
        return left(game)
    elif direction=="right":
        return right(game)


def up(game):
        # print("up")
        # return matrix after shifting up
        game=transpose(game)
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        done=done or temp[1]
        score = temp[2]
        game=cover_up(game)[0]
        game=transpose(game)
        return (game,done, score)

def down(game):
        # print("down")
        game=reverse(transpose(game))
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        score = temp[2]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=transpose(reverse(game))
        return (game,done, score)

def left(game):
        # print("left")
        # return matrix after shifting left
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        score = temp[2]
        done=done or temp[1]
        game=cover_up(game)[0]
        return (game,done, score)

def right(game):
        # print("right")
        # return matrix after shifting right
        game=reverse(game)
        game,done=cover_up(game)
        temp=merge(game)
        game=temp[0]
        score = temp[2]
        done=done or temp[1]
        game=cover_up(game)[0]
        game=reverse(game)
        return (game,done, score)
