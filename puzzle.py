from tkinter import *
from logic import *
from random import *
import random
import matplotlib.pyplot as plt
import util
SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e", 4096:"#f9f6f2" }
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2", 4096:"#d1cfcc" }
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"

class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        # self.master.bind("<Key>", self.key_down)
        self.score = 0
        self.alpha = 0.9
        self.gamma = 0.8
        self.qVals = util.Counter()
        self.num128 = 0
        self.num1024 = 0
        self.num256 = 0
        self.num512=0
        self.num4096=0
        self.num2048 = 0


        # self.gamelogic = gamelogic
        self.commands = {   KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right,
                            KEY_UP_ALT: up, KEY_DOWN_ALT: down, KEY_LEFT_ALT: left, KEY_RIGHT_ALT: right }

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        plt.ion()
        plt.show()


        # self.custom_move()
        # while game_state(self.matrix)!='lose':
        #     resultSc = []
        #     d = ['up', 'down', 'left', 'right']
        #     for direction in d:
        #         self.update_idletasks()
        #         self.update()
        #         child = deepcopy(self.matrix)
        #         try:
        #             child, done, score = move(child, direction)
        #             child = new_tile(child)
        #             resScore = montecarlo(child, heuristic_score(child)+score+self.score)
        #             resultSc.append(resScore)
        #         except IndexError:
        #             continue
        #             print('error')
        #     # print(resultSc)
        #     decision = d[resultSc.index(max(resultSc))]
        #     try:
        #         self.matrix, done, score = move(self.matrix, decision)
        #         self.score += score
        #         print("the score is " + str(self.score))
        #         self.matrix = new_tile(self.matrix)
        #         self.update_grid_cells()
        #     except IndexError:
        #         break

        for i in range(1, 6):
            # self.train(i)
            # self.grid_cells = []
            # self.init_grid()
            # self.init_matrix()
            # self.update_grid_cells()
            # self.score = 0
            # print('number of times 512 ', self.num512)
            # print('number of times 256 ', self.num256)
            # print('number of times 1024 ', self.num1024)
            # print('number of times 128 ', self.num128)
            while game_state(self.matrix)!='lose':
                # print(game_state(self.matrix))
                ans = -float('inf')
                d = ['up', 'down', 'left', 'right']
                for direction in d:
                    # self.update_idletasks()
                    # self.update()
                    child = deepcopy(self.matrix)
                    try:
                        child, done, score = move(child, direction)
                        child = new_tile(child)
                    except IndexError:
                        continue
                        print('error')
                    utility = expectimax(child, 4, False)
                    # print(ans)
                    if utility >= ans:
                        ans = utility
                        try:
                            self.matrix, done, score = move(self.matrix, direction)
                            self.score += score
                            # print("the score is "+str(self.score))
                            self.update_grid_cells()
                            self.matrix = new_tile(self.matrix)
                            self.update_grid_cells()
                        except IndexError:
                            break
                # y = [128, 256, 512, 1024, 2048, 4096, 8192]
            # plt.plot(i, getMaxTile(self.matrix), 'bo-')
            # plt.ylabel('Max Tile Value')
            # plt.xlabel('Number of Iterations')
            # plt.draw()
            print('iteration number is ', i)
            print('The max tile reached has value ', getMaxTile(self.matrix))
            print('The final Score reached for this iteration is ', self.score)
            if getMaxTile(self.matrix) == 512:
                self.num512 += 1
            elif getMaxTile(self.matrix) == 256:
                self.num256 += 1
            elif getMaxTile(self.matrix) == 1024:
                self.num1024 += 1
            elif getMaxTile(self.matrix) == 128:
                self.num128 += 1
            elif getMaxTile(self.matrix) == 2048:
                self.num2048 += 1
            elif getMaxTile(self.matrix) == 4096:
                self.num4096 += 1
            print('Number of 128 is ', self.num128)
            print('Number of 256 is ', self.num256)
            print('Number of 512 is ', self.num512)
            print('Number of 1024 is ', self.num1024)
            print('Number of 2048 is ', self.num2048)
            print('Number of 4096 is ', self.num4096)
            self.grid_cells = []
            self.init_grid()
            self.init_matrix()
            self.update_grid_cells()
            self.score = 0



    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)
        # self.grid_cells.append(score)

    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = new_game(4)

        self.matrix=new_tile(self.matrix)
        self.matrix=new_tile(self.matrix)
        # print(empty_cells(self.matrix))
        self.number_of_empty_cells = len(empty_cells(self.matrix))
        # print(self.number_of_empty_cells)
        # self.custom_move()


    def getActionFromAllActions(self, matrix):
        maxQval = 0.0
        resultDirection = None
        d = ['up', 'down', 'left', 'right']
        for direction in d:
            if self.qVals[(str(matrix), direction)]>=maxQval:
                resultDirection = direction
                maxQval = self.qVals[(str(matrix), direction)]
        return resultDirection

    def getValue(self, matrix):
        maxQVal = 0.0
        d = ['up', 'down', 'left', 'right']
        for direction in d:
            if self.qVals[(str(matrix), direction)] > maxQVal:
                maxQVal = self.qVals[(str(matrix), direction)]
        return maxQVal

    def train(self, i):
        while game_state(self.matrix)!='lose':
            d = ['up', 'down', 'left', 'right']
            for direction in d:
                self.update_idletasks()
                self.update()
                child = deepcopy(self.matrix)
                originalChild = deepcopy(child)
                try:
                    child, done, score = move(child, direction)
                    child = new_tile(child)
                except IndexError:
                    continue
                try:
                    if(game_state(child)=='win'):
                        alphaLearningRate = self.alpha
                        sample = 100 + (self.gamma * self.getValue(child))
                        self.qVals[(str(originalChild), direction)] = (1 - alphaLearningRate) * self.qVals[(str(originalChild),direction)] + (alphaLearningRate * sample)
                    elif game_state(child)=='lose':
                        alphaLearningRate = self.alpha
                        sample = -1000 + (self.gamma * self.getValue(child))
                        self.qVals[(str(originalChild), direction)] = (1 - alphaLearningRate) * self.qVals[(str(originalChild),direction)] + (alphaLearningRate * sample)
                    else:
                        alphaLearningRate = self.alpha
                        sample = 1+ (self.gamma * self.getValue(child))
                        self.qVals[(str(originalChild), direction)] = (1 - alphaLearningRate) * self.qVals[(str(originalChild), direction)] + (alphaLearningRate * sample)
                except IndexError:
                    continue
                    print('error')
            decision = self.getActionFromAllActions(originalChild)
            try:
                self.matrix, done, score = move(self.matrix, decision)
                self.score += score
                self.matrix = new_tile(self.matrix)
                self.update_grid_cells()
            except IndexError:
                break
        print("the score for current game " + str(self.score))
        plt.plot(i, self.score, 'bo-')
        plt.ylabel('Game Scores')
        plt.xlabel('Number of Iterations')
        plt.draw()
        print(getMaxTile(self.matrix))
        if getMaxTile(self.matrix)==512:
            self.num512+=1
        elif getMaxTile(self.matrix)==256:
            self.num256+=1
        elif getMaxTile(self.matrix)==1024:
            self.num1024+=1
        elif getMaxTile(self.matrix)==128:
            self.num128+=1


    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number], fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key in self.commands:
            self.matrix,done = self.commands[repr(event.char)](self.matrix)
            print(self.commands[repr(event.char)](self.matrix))
            print(repr(event.char))
            if done:
                self.matrix = add_two(self.matrix)
                self.update_grid_cells()
                done=False
                if game_state(self.matrix)=='win':
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!",bg=BACKGROUND_COLOR_CELL_EMPTY)
                if game_state(self.matrix)=='lose':
                    self.grid_cells[1][1].configure(text="You",bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!",bg=BACKGROUND_COLOR_CELL_EMPTY)


    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

gamegrid = GameGrid()
