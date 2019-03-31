# 15-112, Summer 2, Homework 4.2 snake.py
######################################
# Full name: Wenkai Pan
# Section: A
# Andrew ID:wenkaip
######################################
######################################################################
######################################################################
######################################################################
##### ignore_rest: The autograder will ignore all code below here ####
######################################################################
######################################################################
from tkinter import *
import random

# Initialize the data which will be used to draw on the screen.
def init(data): # load data as appropriate
    data.rows = 8
    data.cols = 15
    data.headRow = data.rows//2
    data.headCol = data.cols//2
    initBoard(data)
    data.dir = (1,0)
    placeFood(data)
    data.count = 0
    data.countMove = 0
    data.leastMove = 20
    data.isGameOver = False
    data.margin = 100
    data.isIgnoreStep = False
    data.isPaused = False
    data.score = 0
    data.highScoreNum = 3
    data.highScoreList = []
    data.poison = -3
    data.levelTransfer = 3

def reInit(data): # restart the game and reinitialize data
    data.rows = 8
    data.cols = 15
    data.headRow = data.rows//2
    data.headCol = data.cols//2
    initBoard(data)
    data.dir = (1,0)
    placeFood(data)
    data.count = 0
    data.countMove = 0
    data.leastMove = 20
    data.isGameOver = False
    data.margin = 100
    data.isIgnoreStep = False
    data.isPaused = False
    data.highScoreNum = 3
    data.score = 0
    
def placeFood(data): # random place food 
    r = random.randint(0, data.rows-1)
    c = random.randint(0, data.cols-1)
    while (data.board[r][c] != 0): # if not on the snake body
        r = random.randint(0, data.rows-1)
        c = random.randint(0, data.cols-1)
    data.board[r][c] = -1
    
def placePoison(data, headRow, headCol): # random place poison
    r = random.randint(0, data.rows-1)
    c = random.randint(0, data.cols-1)
    poisonLoc = data.board[r][c]
    headLoc = data.board[headRow][headCol]
    while (poisonLoc != 0):
    # if not on the snake body or food or one square from snake head
        if (r == headRow or c == headCol):
            if (r + 1 == headRow or r - 1 == headRow or c + 1 == headCol
            or c - 1 == headCol): 
                r = random.randint(0, data.rows-1)
                c = random.randint(0, data.cols-1)
                count = 0
                for row in data.rows:
                    for col in data.cols:
                        if (data.board[row][col] == 0):
                            count += 1
                            r, c == row, col
                if (count == 1): break
        else: break
    data.board[r][c] = -2
    
def initBoard(data): # initialize the board
    data.board = []
    for row in range(data.rows):
        data.board.append([0] * data.cols)
    data.board[data.headRow][data.headCol] = 1


# These are the CONTROLLERs.
# IMPORTANT: CONTROLLER does *not* draw at all!
# It only modifies data according to the events.
def mousePressed(event, data): # click to form or destroy walls
    if (data.isPaused):
        margin = data.margin
        w = data.width - 2 * margin
        h = data.height - 2 * margin
        cellW = w / data.cols
        cellH = h / data.rows
        for row in range(data.rows):
            for col in range(data.cols):
                x0 = cellW * col
                y0 = cellH * row
                x1 = cellW * (col + 1)
                y1 = cellH * (row + 1)
                if (event.x >= (x0 + margin) and event.x <= (x1 + margin) 
                and event.y >= (y0 + margin) and event.y <= (y1 + margin) 
                and data.board[row][col] == 0):
                    data.board[row][col] = data.poison
                elif (event.x >= (x0 + margin) and event.x <= (x1 + margin) 
                and event.y >= (y0 + margin) and event.y <= (y1 + margin) 
                and data.board[row][col] == data.poison):
                    data.board[row][col] = 0

def keyPressed(event, data): # keypressed operation
    if (event.keysym == 'r'): reInit(data); return 
    elif (event.keysym == 'p'): 
        data.isPaused = not data.isPaused
        return
    if (data.isGameOver or data.isPaused): return # if game over or paused
    if (event.keysym == 'Up'):
        data.dir = (-1, 0)
    elif (event.keysym == 'Down'):
        data.dir = (1, 0)
    elif (event.keysym == 'Left'):
        data.dir = (0, -1)
    elif (event.keysym == 'Right'): 
        data.dir = (0, 1) 
    takeStep(data)
    data.isIgnoreStep = True

def timerFired(data): # time delay for each move and draw
    if (data.isIgnoreStep): # ignore double clicks
        data.isIgnoreStep = False
    else:
        if (not data.isPaused and not data.isGameOver):
            takeStep(data)
        
def gameOver(data): # when hit the wall or itself or the poison
    data.isGameOver = True
    data.highScoreList.append(data.score) # store the three highest scores
    length = 3
    if (len(data.highScoreList) > length):
        data.highScoreList.remove(min(data.highScoreList))
    data.highScoreList.sort()
    data.highScoreList.reverse()

def hitFood(data, newHeadRow, newHeadCol): # when hit food
    data.board[newHeadRow][newHeadCol] = \
        data.board[data.headRow][data.headCol] + 1
    
    data.headRow = newHeadRow
    data.headCol = newHeadCol
    data.score += 1
    data.count += 1
    placeFood(data)
    if (data.count == data.levelTransfer): # if in the second level
        placePoison(data, newHeadRow, newHeadCol)

def hitWall(data, newHeadRow, newHeadCol): # when hit wall
    data.board[newHeadRow][newHeadCol] = \
        data.board[data.headRow][data.headCol] + 1

    data.headRow = newHeadRow
    data.headCol = newHeadCol
    removeTail(data)
    data.score -= 1
    if (data.score < 0):
        gameOver(data)
    
def moveForward(data, newHeadRow, newHeadCol): # when move to another grid
    data.board[newHeadRow][newHeadCol] = \
        data.board[data.headRow][data.headCol] + 1

    data.headRow = newHeadRow
    data.headCol = newHeadCol
    removeTail(data)

def takeStep(data): # move one step at a time
    drow, dcol = data.dir
    newHeadRow = data.headRow + drow
    newHeadCol = data.headCol + dcol
    # snake moves off board or hits self
    if (newHeadRow < 0 or newHeadRow >= data.rows or 
        newHeadCol < 0 or newHeadCol >= data.cols or 
        data.board[newHeadRow][newHeadCol] > 0):
        gameOver(data)
        return
    elif (data.board[newHeadRow][newHeadCol] == -1): # hit food
        hitFood(data, newHeadRow, newHeadCol)
    elif (data.board[newHeadRow][newHeadCol] == 0): # move snake forward
        moveForward(data, newHeadRow, newHeadCol)
    elif (data.board[newHeadRow][newHeadCol] == -2): # hit poison
        gameOver(data)
    elif (data.board[newHeadRow][newHeadCol] == data.poison): # hit wall
        hitWall(data, newHeadRow, newHeadCol)
    searchForWall(data)

def searchForWall(data): # judge whether any walls existed after each step
    wallExisted = False
    for row in range(data.rows):
        for col in range(data.cols):
            if (data.board[row][col] == data.poison):
                wallExisted = True
    if (wallExisted):
        data.countMove += 1
    if (data.countMove >= 20): # if wall existed for at least 20 moves
        data.score += 1
        data.countMove = 0

def removeTail(data): # remove tail of the snake
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] > 0:
                data.board[row][col] -= 1

# This is the VIEW
# IMPORTANT: VIEW does *not* modify data at all!
# It only draws on the canvas.
def redrawAll(canvas, data):  # draw in canvas
    drawBoard(canvas, data)
    margin = 20
    canvas.create_text(data.width / 2, margin, text="Score = " + 
    str(data.score), font="eHelvetica 32 bold")
    if (data.isGameOver): # if game is over
        rowMargin = 100
        height = data.height / 2 - rowMargin * 2
        canvas.create_text(data.width / 2, height,
        text="Game Over!", font = "Helvetica 32 bold")
        canvas.create_text(data.width / 2, height + rowMargin, 
        text="High Score List:", font="Helvetica 32 bold")
        for i in range(len(data.highScoreList)):
            canvas.create_text(data.width / 2, height + rowMargin * (i+2),
            text = str(data.highScoreList[i]), font="Helvetica 32 bold")

def rgbString(red, green, blue): # rgb color
    return "#%02x%02x%02x" % (red, green, blue)
    
def drawBoard(canvas, data): # draw the board in different modes
    for row in range(data.rows):
        for col in range(data.cols):
            if (not data.isPaused): # when paused
                drawSnakeCell(canvas, data, row, col)
            else:
                drawDimCell(canvas, data, row, col)
                
def drawSnakeCell(canvas, data, row, col): # draw the cell
    margin = data.margin
    w = data.width - 2 * margin
    h = data.height - 2 * margin
    cellW = w / data.cols
    cellH = h / data.rows
    x0 = cellW * col
    y0 = cellH * row
    x1 = cellW * (col + 1)
    y1 = cellH * (row + 1)
    fill = "white"
    if (data.board[row][col] > 0):
        fill= "blue"
    elif (data.board[row][col] == -1):
        fill = "green"
    elif (data.board[row][col] == -2):
        fill = "red"
    elif (data.board[row][col] == data.poison):
        fill = "brown"
    canvas.create_rectangle(x0+margin,y0+margin,x1+margin,y1+margin, fill=fill)

def drawDimCell(canvas, data, row, col): # draw the cell when paused
    margin = data.margin
    w, h = data.width - 2 * margin, data.height - 2 * margin
    cellW = w / data.cols
    cellH = h / data.rows
    x0 = cellW * col
    y0 = cellH * row
    x1 = cellW * (col + 1)
    y1 = cellH * (row + 1)
    rgbWhite, rgbGreen, rgbRed, rgbBlue = 220, 139, 139, 128
    rgbBrown1, rgbBrown2, rgbBrown3 = 139, 69, 19
    fill = rgbString(rgbWhite, rgbWhite, rgbWhite)
    if (data.board[row][col] > 0):
        fill= rgbString(0, 0, rgbBlue)
    elif (data.board[row][col] == -1):
        fill= rgbString(0, rgbGreen, 0)
    elif (data.board[row][col] == -2):
        fill = rgbString(rgbRed, 0, 0)
    elif (data.board[row][col] == data.poison):
        fill = rgbString(rgbBrown1, rgbBrown2, rgbBrown3)
    canvas.create_rectangle(x0+margin,y0+margin,x1+margin,y1+margin, fill=fill)

####################################
####################################
# use the run function as-is(cited from lecture notes)
####################################
####################################

def runSnake(width=300, height=300): # run function
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        if (data.count < data.levelTransfer):
            canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        else:
            delay = 100
            canvas.after(delay, timerFiredWrapper, canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 400 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def run(): # top Level Function
    width = 1500
    height = 800
    runSnake(width, height)

run() # run the program
######################################################################
######################################################################
# Main: you may modify this to run just the parts you want to test
######################################################################

def main():
    # include function calls for your own test functions
    pass

if __name__ == "__main__":
     main()
     
