import random
import sys

width = 8 #go board width
height = 8 #go board height

def drawboard(board):
    print(" 12345678 ")
    print(" +--------+ ")
    for y in range(height):
        print("%s|" %(y+1), end="")
        for x in range(width):
            print(board[x][y], end="")
        print('|%s' % (y + 1))
    print(" 12345678 ")
    print(" +--------+ ")

def getNewBoard():
    board = []
    for i in range(width):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board

def isonboard(x, y):
    return x >= 0 and y >=0 and x <= width -1 and y <= height -1

def isvalidmove(board, tile, xl, yl):
    if board[xl][yl] != " " or isonboard(xl,yl):
        return False

    if tile == 'X':
        othertile = "O"
    else:
        tile = 'X'

    tilesToFlip = []

    for xdirection, ydirection in [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]:
        x, y = xl, yl
        x += xdirection
        y += ydirection
    while isonboard(x, y) and board[x][y] == othertile:
        x += xdirection
        y += ydirection
        if isonboard(x, y) and board[x][y] == tile:
            while True:
                x -= xdirection
                y -= ydirection
                if x == xl and y == yl:
                    break
                tilesToFlip.append([x,y])
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip

def getBoardWithValidMove(board, tile):
    boardcopy = getBoardCopy(board)

    for x, y in getValidMoves(boardcopy, tile):
        boardcopy[x][y] = '.'
    return boardcopy

def getValidMoves(board, tile):
    validMoves = []
    for x in range(width):
        for y in range(height):
            if isvalidmove(board, tile, x, y) != False:
                validMoves.append([x,y])
    return validMoves

def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(width):
        for y in range(height):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
        return {'X':xscore, 'Y':oscore}

def enterPlayerTile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        tile = input('Do you want to be X or O>?').upper()

        if tile == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']

def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

def makeMove(board, tile, xl, yl):
    tilesToFlip = isvalidmove(board, tile, xl, yl)
    if tilesToFlip == False:
        return False

    board[xl][yl] =tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    boardCopy = getNewBoard()

    for x in range(width):
        for y in range(height):
            boardCopy[x][y] = board[x][y]

    return boardCopy

def isOnCorner(x, y):
    return (x == 0 or x == width -1) and (y == 0 or y == height -1)

def getPlayerMove(board, playerTile):
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print("Enter your move , 'quit' to end the game, or 'hints' to toggle hints.")
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isvalidmove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move.Enter the colum (1-8) and then the row(1-8)')
            print("For example, 81 will move on the top-right corner.")

    return [x, y]

def getCompuerMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)

    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    bestsocre = -1
    for x, y in possibleMoves:
        boardcopy = getBoardCopy(board)
        makeMove(boardcopy, computerTile, x, y)
        score = getScoreOfBoard(boardcopy)[computerTile]
        if score > bestsocre:
            bestMove = [x,y]
            bestsocre = score
    return bestMove

def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('You: %s points. Computer: %s points.' % (scores[playerTile], scores[computerTile]))

def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'
    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)
        if playerValidMoves == [] and computerValidMoves == []:
            return board
        elif turn == 'player':
            if playerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMove(board, playerTile)
                    drawboard(validMovesBoard)
                else:
                    drawboard(board)
                printScore(board, playerTile, computerTile)
                move = getPlayerMove(board, playerTile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()  # Terminate the program.
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, playerTile, move[0], move[1])
            turn = 'computer'

        elif turn == 'computer':
            if computerValidMoves != []:
                drawboard(board)
                printScore(board, playerTile, computerTile)

                input('Press Enter to see the computer\'s move.')
                move = getCompuerMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            turn = 'player'


print('Welcome to Reversegam!')
playerTile, computerTile = enterPlayerTile()

while True:
    finalBoard = playGame(playerTile, computerTile)
    drawboard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('X scored %s points. O scored %s points.' % (scores['X'], scores['Y']))
    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points! Congratulations!' %(scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points.' %(scores[computerTile] - scores[playerTile]))
    else:
        print('The game was tie!')

    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        break