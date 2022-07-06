from random import randint,seed

class Maze:
    def __init__(self, cols=8, rows=8, key='default'):
        '''Creates maze (2D matrix of ints) via Randomized Prim's Algorithm, given a seed for random numbers.'''
        if cols < 3 or rows < 3:
            raise ValueError('Dimensions must be at least 3x3.')
        # 0 is undefined, 1 is wall, 2 is cell
        seed(key)
        self.cols = cols
        self.rows = rows
        self.maze = [[0]*cols for i in range(rows)]
        currRow = randint(1,self.rows-2) # start (not on edge)
        currCol = randint(1,self.cols-2)
        self.maze[currRow][currCol] = 2 # start
        self.makeWalls(currRow,currCol)
        walls = self.findAdjVal(currRow,currCol,1)
        while walls: # empty list evaluates as boolean
            randWall = walls[randint(0,len(walls)-1)] # select wall
            adjCells = self.findAdjVal(randWall[0],randWall[1],2)
            if (self.inBounds(randWall[0]+1,randWall[1]+1) and
                self.inBounds(randWall[0]-1,randWall[1]-1) and
                ((self.maze[randWall[0]][randWall[1]+1] == 0 and self.maze[randWall[0]][randWall[1]-1] == 2) or
                 (self.maze[randWall[0]][randWall[1]+1] == 2 and self.maze[randWall[0]][randWall[1]-1] == 0) or
                 (self.maze[randWall[0]+1][randWall[1]] == 0 and self.maze[randWall[0]-1][randWall[1]] == 2) or
                 (self.maze[randWall[0]+1][randWall[1]] == 2 and self.maze[randWall[0]-1][randWall[1]] == 0)) and
                len(adjCells) == 1): # wall not on border, between undefined and cell, only 1 adjacent cell
                self.maze[randWall[0]][randWall[1]] = 2 # wall becomes cell
                # in the direction of the just-changed wall, make a wall
                if randWall[0]-currRow == -1: # wall was row above
                    try: 
                        self.maze[currRow-2][currCol] = 1
                    except IndexError:
                        continue
                elif randWall[0]-currRow == 1: # wall was row below
                    try: 
                        self.maze[currRow+2][currCol] = 1
                    except IndexError:
                        continue
                elif randWall[1]-currCol == -1: # wall was left
                    try:
                        self.maze[currRow][currCol-2] = 1
                    except IndexError:
                        continue
                elif randWall[1]-currCol == 1: # wall was right
                    try:
                        self.maze[currRow][currCol+2] = 1
                    except IndexError:
                        continue
                currRow = randWall[0] # wall becomes current cell
                currCol = randWall[1] 
                self.makeWalls(currRow,currCol)
                walls += self.findAdjVal(currRow,currCol,1)
            walls.remove(randWall)
        for i in range(self.rows): # poking start and end into border
            if self.maze[i][1] == 2:
                self.maze[i][0] = 2
                break
        for i in range(self.rows): # poking start and end into border
            if self.maze[i][self.rows-2] == 2:
                self.maze[i][self.rows-1] = 2
                break
        for r in range(self.rows): # replace leftover undefined with walls
            for c in range(self.cols):
                if self.maze[r][c] == 0:
                    self.maze[r][c] = 1

    def findAdjVal(self, r, c, value):
        '''Helper method that returns list corresponding to 4 locations surrounding point:
        tuple coordinate if the value is at the location, None otherwise.'''
        # 0 is undefined, 1 is wall, 2 is cell
        locs = []
        for i in range(-1,2,2):
            if self.inBounds(r+i,c) and self.maze[r+i][c] == value:
                locs.append((r+i,c))
        for i in range(-1,2,2):
            if self.inBounds(r,c+i) and self.maze[r][c+i] == value:
                locs.append((r,c+i))
        return locs
    
    def makeWalls(self, r, c):
        '''Helper method that makes walls adjacent to cell.'''
        for i in range(-1,2,2): # starting walls
            if self.inBounds(r+i,c) and self.maze[r+i][c] != 2: # not cells
                self.maze[r+i][c] = 1
        for i in range(-1,2,2):
            if self.inBounds(r,c+i) and self.maze[r][c+i] != 2: # not cells
                self.maze[r][c+i] = 1

    def inBounds(self, r, c):
        '''Helper method determining whether coordinates are within maze bounds.'''
        return 0 <= r < self.rows and 0 <= c < self.cols
    
    def __str__(self):
        string = ''
        for r in range(self.rows):
            for v in self.maze[r]:
                string += str(v) + '  '
            string += '\n'
        return string

if __name__ == '__main__':
    print(Maze())