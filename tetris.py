# 15-112, Summer 2, Homework 4.2 tetris.py
######################################
# Full name: Wenkai Pan
# Section: A
# Andrew ID:wenkaip
# Collaborate classmate's full name: Tianyang Lan
# Section: A
# Andrew ID:tianyanl
######################################
######################################################################
######################################################################
######################################################################
##### ignore_rest: The autograder will ignore all code below here ####
######################################################################
######################################################################
from tkinter import *
import random
import copy

def init(data):
    # set board dimensions and margin
    data.rows = 15
    data.cols = 10
    data.margin = 20
    # make board
    data.emptyColor = "blue"
    data.board = [([data.emptyColor] * data.cols) for row in range(data.rows)]
    data.tetrisPieces = getTetrisPieces()
    data.tetrisPieceColors = getTetrisPiecesColors()
    data.fallingPiece = None
    data.fallingPieceColor = None
    newFallingPiece(data)
    data.isGameOver = False
    data.score = 0
    data.isPaused = False
    
def getTetrisPieces(): # get seven pieces
#Seven "standard" pieces (tetrominoes)
  iPiece = [[ True,  True,  True,  True]]
  jPiece = [[ True, False, False ],[ True, True,  True]]  
  lPiece = [[ False, False, True],[ True,  True,  True]]  
  oPiece = [[ True, True],[ True, True]]
  sPiece = [[ False, True, True], [ True,  True, False ]]  
  tPiece = [[ False, True, False ],[ True,  True, True]]
  zPiece = [[ True,  True, False ],[ False, True, True]]
  tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
  return tetrisPieces

def getTetrisPiecesColors(): # get seven colors
    tetrisPiecesColors = ["red", "yellow", "magenta", "pink", "cyan", "green", "orange"]
    return tetrisPiecesColors

def newFallingPiece(data): # renew falling piece
    index = random.randint(0, len(data.tetrisPieces)-1)
    data.fallingPiece = data.tetrisPieces[index]
    data.fallingPieceColor = data.tetrisPieceColors[index]
    data.fallingPieceCols = getFallingPieceCols(data)
    data.fallingPieceRows = getFallingPieceRows(data)
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols // 2 - data.fallingPieceCols // 2
    if(not fallingPieceIsLegal(data)):
        data.isGameOver = True

def getFallingPieceCols(data): # get the start col
    cols = len(data.fallingPiece[0])
    return cols

def getFallingPieceRows(data): # get the start row
    rows = len(data.fallingPiece)
    return rows

# getCellBounds from grid-demo.py
def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)

def moveFallingPiece(data, drow, dcol): # move the piece
    row, col = data.fallingPieceRow, data.fallingPieceCol
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if (not fallingPieceIsLegal(data)):
        data.fallingPieceRow = row
        data.fallingPieceCol = col
        return False
    return True
    
def rotateFallingPiece(data): # rotate the piece
    oldFallingPiece = copy.deepcopy(data.fallingPiece)
    (oldRowLoc, oldColLoc) = \
        (copy.copy(data.fallingPieceRow),copy.copy(data.fallingPieceCol))
    (oldRowCount, oldColCount) = \
        (copy.copy(data.fallingPieceRows),copy.copy(data.fallingPieceCols))
    centerRow, centerCol = oldRowLoc + oldRowCount // 2,\
        oldColLoc + oldColCount//2
    newFallingPiece = [[False] * len(oldFallingPiece)\
    for i in range(len(oldFallingPiece[0]))]
    newRowCount, newColCount = oldColCount, oldRowCount
    for row in range(oldRowCount):
        newCol = row
        for col in range(oldColCount):
            newRow = oldColCount - 1 - col
            newFallingPiece[newRow][newCol] = oldFallingPiece[row][col]
    renewFallingPiece(data, newFallingPiece, centerRow, centerCol, newRowCount,
    newColCount)
    if (not fallingPieceIsLegal(data)):
        OldFallingPiece(data, oldFallingPiece, oldRowLoc, oldColLoc, 
        oldRowCount, oldColCount)
    
def renewFallingPiece(data, newFallingPiece, centerRow, centerCol, newRowCount,
newColCount): # renew falling piece
    data.fallingPiece = newFallingPiece
    data.fallingPieceRow, data.fallingPieceCol = centerRow - newRowCount //2, centerCol - newColCount // 2
    data.fallingPieceRows, data.fallingPieceCols = newRowCount, newColCount  

def OldFallingPiece(data, oldFallingPiece, oldRowLoc, oldColLoc, oldRowCount,
oldColCount): # keep the original falling piece
    data.fallingPiece = oldFallingPiece
    data.fallingPieceRow, data.fallingPieceCol = oldRowLoc, oldColLoc
    data.fallingPieceRows, data.fallingPieceCols = oldRowCount, oldColCount

def fallingPieceIsLegal(data): # check if the piece is out of bound or overlap
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if (data.fallingPiece[row][col]):
                cellRow = row + data.fallingPieceRow
                cellCol = col + data.fallingPieceCol
                if (cellRow < 0 or cellRow >= data.rows):
                    return False
                elif (cellCol < 0 or cellCol >= data.cols):
                    return False
                elif (data.board[cellRow][cellCol] != data.emptyColor):
                    return False
    return True

def placeFallingPiece(data): # place the piece on the board
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if (data.fallingPiece[row][col]):
                cellRow = row + data.fallingPieceRow
                cellCol = col + data.fallingPieceCol
                data.board[cellRow][cellCol] = data.fallingPieceColor

def removeFullRows(data): # remove the rols that has no empty cells
    newRow = data.rows - 1
    fullRows = 0
    for oldRow in reversed(range(data.rows)):
        if(isFullRow(data, data.board[oldRow])):
            fullRows += 1
        else:
            data.board[newRow] = copy.copy(data.board[oldRow])
            newRow -= 1
    data.score += fullRows ** 2
    for row in reversed(range(newRow + 1)):
        clearRow(data, data.board[row])

def clearRow(data, row): # clear the full row
    for i in range(len(row)):
        row[i] = data.emptyColor
    
def isFullRow(data, rows): # judge if it is full
    for elem in rows:
        if (elem == data.emptyColor):
            return False
    return True

def mousePressed(event, data): # mouse pressed operation
    pass

def keyPressed(event, data): # key pressed operation
    if (event.keysym == "p"): 
        data.isPaused = not data.isPaused
        return 
    if (event.keysym == "r"):
        init(data)
        return 
    if (data.isGameOver or data.isPaused):
        return
    if (event.keysym == "Left"):
        moveFallingPiece(data, 0, -1)
    elif (event.keysym == "Right"):
        moveFallingPiece(data, 0, +1)
    elif (event.keysym == "Down"):
        moveFallingPiece(data, +1, 0)
    elif (event.keysym == "Up"):
        rotateFallingPiece(data)
    elif (event.keysym == "space"):
        while (moveFallingPiece(data, +1, 0)):
            continue
        
def timerFired(data): # steps for some amount of time
    if (not data.isGameOver and not data.isPaused):
        if(not moveFallingPiece(data, +1, 0)):
            placeFallingPiece(data)
            newFallingPiece(data)
            removeFullRows(data)


def drawGame(canvas, data): # draw the whole game
    canvas.create_rectangle(0, 0, data.width, data.height, fill="orange")
    drawBoard(canvas, data)
    print(data.width)
    drawFallingPiece(canvas, data)
    drawScore(canvas, data)
    if (data.isGameOver):
        h = 50
        canvas.create_text(data.width // 2, data.height // 2, text="Game Over!",
        fill = "yellow", font = "Helvetica 32 bold")
        canvas.create_text(data.width // 2, data.height // 2 + h, 
        fill = "yellow", text="Press 'r' to reset", font="Helvetica 16")

def drawScore(canvas, data): # draw the score on the top
    canvas.create_text(data.width // 2, 10, text="Score: " + str(data.score), font="Helvetica 16")
    
def drawBoard(canvas, data): # draw the board
    # draw grid of cells
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])

def drawCell(canvas, data, row, col, color): # draw each cell
    (x0, y0, x1, y1) = getCellBounds(row, col, data)
    m = 1 # cell outline margin
    canvas.create_rectangle(x0, y0, x1, y1, fill="black")
    canvas.create_rectangle(x0+m, y0+m, x1-m, y1-m, fill=color)

def drawFallingPiece(canvas, data): # draw the piece
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if (data.fallingPiece[row][col]):
                cellRow = row + data.fallingPieceRow
                cellCol = col + data.fallingPieceCol
                drawCell(canvas, data, cellRow, cellCol, data.fallingPieceColor)
        
def redrawAll(canvas, data): # top level draw function
    drawGame(canvas, data)

####################################
# use the run function as-is (copy from lecture code)
####################################

def runTetris(width=300, height=300):
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
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 500 # milliseconds
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

####################################
# playTetris() [calls run()]
####################################

def run(): # start playing tetris
    rows = 15
    cols = 10
    margin = 20 # margin around grid
    cellSize = 20 # width and height of each cell
    width = 2*margin + cols*cellSize
    height = 2*margin + rows*cellSize
    runTetris(width, height)

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
     
