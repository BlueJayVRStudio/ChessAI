# citations:
## chess piece images: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent

# is this how you enum in python?
class piece:
    def __init__(self):
        self.WhP = 0
        self.WhR = 1
        self.WhKn = 2
        self.WhB = 3
        self.WhQ = 4
        self.WhK = 5

        self.BlP = 6
        self.BlR = 7
        self.BlKn = 8
        self.BlB = 9
        self.BlQ = 10
        self.BlK = 11

Piece = piece()

class game:
    def __init__(self):
        self.ongoing = True
        self._checked = False
        self.win = False
        self.movesAdded = False

        self.previousMove = []
        self.whiteTurn = True

        self.numMoves = 0

        self.board = {}
        self.availableMoves = {}

        self.board[(1, 1)] = Piece.WhR
        self.board[(2, 1)] = Piece.WhKn
        self.board[(3, 1)] = Piece.WhB
        self.board[(4, 1)] = Piece.WhQ
        self.board[(5, 1)] = Piece.WhK
        self.board[(6, 1)] = Piece.WhB
        self.board[(7, 1)] = Piece.WhKn
        self.board[(8, 1)] = Piece.WhR

        self.board[(1, 2)] = Piece.WhP
        self.board[(2, 2)] = Piece.WhP
        self.board[(3, 2)] = Piece.WhP
        self.board[(4, 2)] = Piece.WhP
        self.board[(5, 2)] = Piece.WhP
        self.board[(6, 2)] = Piece.WhP
        self.board[(7, 2)] = Piece.WhP
        self.board[(8, 2)] = Piece.WhP

        self.board[(1, 7)] = Piece.BlP
        self.board[(2, 7)] = Piece.BlP
        self.board[(3, 7)] = Piece.BlP
        self.board[(4, 7)] = Piece.BlP
        self.board[(5, 7)] = Piece.BlP
        self.board[(6, 7)] = Piece.BlP
        self.board[(7, 7)] = Piece.BlP
        self.board[(8, 7)] = Piece.BlP

        self.board[(1, 8)] = Piece.BlR
        self.board[(2, 8)] = Piece.BlKn
        self.board[(3, 8)] = Piece.BlB
        self.board[(4, 8)] = Piece.BlQ
        self.board[(5, 8)] = Piece.BlK
        self.board[(6, 8)] = Piece.BlB
        self.board[(7, 8)] = Piece.BlKn
        self.board[(8, 8)] = Piece.BlR

    # check if current player's king is in check
    def checked(self):
        keys = list(self.board.keys())

        # check if white king is checked
        if self.whiteTurn:
            for key in keys:
                if self.board[key] == Piece.BlR or self.board[key] == Piece.BlQ:
                    # left
                    x = key[0] - 1
                    y = key[1]
                    while x > 0:
                        if (x, y) not in self.board:
                            x -= 1
                            continue

                        if (self.board[(x, y)] == Piece.WhK):
                            return True
                        else:
                            break

                    # right
                    x = key[0] + 1
                    y = key[1]
                    while x < 9:
                        if (x, y) not in self.board:
                            x += 1
                            continue

                        if (self.board[(x, y)] == Piece.WhK):
                            return True
                        else:
                            break
                    
                    # down
                    x = key[0]
                    y = key[1] - 1
                    while y > 0:
                        if (x, y) not in self.board:
                            y -= 1
                            continue

                        if (self.board[(x, y)] == Piece.WhK):
                            return True
                        else:
                            break
                    
                    # up
                    x = key[0]
                    y = key[1] + 1
                    while y < 9:
                        if (x, y) not in self.board:
                            y += 1
                            continue

                        if (self.board[(x, y)] == Piece.WhK):
                            return True
                        else:
                            break
                
                if self.board[key] == Piece.BlB or self.board[key] == Piece.BlQ:
                    # Diag I
                    x = key[0] + 1
                    y = key[1] + 1
                    while x < 9 and y < 9:
                        if (x, y) not in self.board:
                            x += 1
                            y += 1
                            continue

                        if (self.board[(x, y)] == Piece.WhK):
                            return True
                        else:
                            break
                    
                    # Diag II
                    x = key[0] - 1
                    y = key[1] + 1
                    while x > 0 and y < 9:
                        if (x, y) not in self.board:
                            x -= 1
                            y += 1
                            continue

                        if (self.board[(x, y)] == Piece.WhK):
                            return True
                        else:
                            break
                    
                    # Diag III
                    x = key[0] - 1
                    y = key[1] - 1
                    while x > 0 and y > 0:
                        if (x, y) not in self.board:
                            x -= 1
                            y -= 1
                            continue

                        if (self.board[(x, y)] == Piece.WhK):
                            return True
                        else:
                            break
                    
                    # Diag IV
                    x = key[0] + 1
                    y = key[1] - 1
                    while x < 9 and y > 0:
                        if (x, y) not in self.board:
                            x += 1
                            y -= 1
                            continue

                        if (self.board[(x, y)] == Piece.WhK):
                            return True
                        else:
                            break

                if self.board[key] == Piece.BlKn:
                    x = key[0]
                    y = key[1]
                    for knPosition in [(x+1, y+2), (x+2, y+1), (x-1, y+2), (x-2, y+1), (x-1, y-2), (x-2, y-1), (x+1, y-2), (x+2, y-1)]:
                        if knPosition not in self.board:
                            continue
                        if self.board[knPosition] == Piece.WhK:
                            return True
                
                if self.board[key] == Piece.BlP:
                    x = key[0]
                    y = key[1]
                    for pPosition in [(x-1, y-1), (x+1, y-1)]:
                        if pPosition not in self.board:
                            continue
                        if self.board[pPosition] == Piece.WhK:
                            return True

        # check if black king is checked
        else:
            for key in keys:
                if self.board[key] == Piece.WhR or self.board[key] == Piece.WhQ:
                    # left
                    x = key[0] - 1
                    y = key[1]
                    while x > 0:
                        if (x, y) not in self.board:
                            x -= 1
                            continue

                        if (self.board[(x, y)] == Piece.BlK):
                            return True
                        else:
                            break

                    # right
                    x = key[0] + 1
                    y = key[1]
                    while x < 9:
                        if (x, y) not in self.board:
                            x += 1
                            continue

                        if (self.board[(x, y)] == Piece.BlK):
                            return True
                        else:
                            break
                    
                    # down
                    x = key[0]
                    y = key[1] - 1
                    while y > 0:
                        if (x, y) not in self.board:
                            y -= 1
                            continue

                        if (self.board[(x, y)] == Piece.BlK):
                            return True
                        else:
                            break
                    
                    # up
                    x = key[0]
                    y = key[1] + 1
                    while y < 9:
                        if (x, y) not in self.board:
                            y += 1
                            continue

                        if (self.board[(x, y)] == Piece.BlK):
                            return True
                        else:
                            break
                
                if self.board[key] == Piece.WhB or self.board[key] == Piece.WhQ:
                    # Diag I
                    x = key[0] + 1
                    y = key[1] + 1
                    while x < 9 and y < 9:
                        if (x, y) not in self.board:
                            x += 1
                            y += 1
                            continue

                        if (self.board[(x, y)] == Piece.BlK):
                            return True
                        else:
                            break
                    
                    # Diag II
                    x = key[0] - 1
                    y = key[1] + 1
                    while x > 0 and y < 9:
                        if (x, y) not in self.board:
                            x -= 1
                            y += 1
                            continue

                        if (self.board[(x, y)] == Piece.BlK):
                            return True
                        else:
                            break
                    
                    # Diag III
                    x = key[0] - 1
                    y = key[1] - 1
                    while x > 0 and y > 0:
                        if (x, y) not in self.board:
                            x -= 1
                            y -= 1
                            continue

                        if (self.board[(x, y)] == Piece.BlK):
                            return True
                        else:
                            break
                    
                    # Diag IV
                    x = key[0] + 1
                    y = key[1] - 1
                    while x < 9 and y > 0:
                        if (x, y) not in self.board:
                            x += 1
                            y -= 1
                            continue

                        if (self.board[(x, y)] == Piece.BlK):
                            return True
                        else:
                            break

                if self.board[key] == Piece.WhKn:
                    x = key[0]
                    y = key[1]
                    for knPosition in [(x+1, y+2), (x+2, y+1), (x-1, y+2), (x-2, y+1), (x-1, y-2), (x-2, y-1), (x+1, y-2), (x+2, y-1)]:
                        if knPosition not in self.board:
                            continue
                        if self.board[knPosition] == Piece.BlK:
                            return True
                
                if self.board[key] == Piece.WhP:
                    x = key[0]
                    y = key[1]
                    for pPosition in [(x-1, y+1), (x+1, y+1)]:
                        if pPosition not in self.board:
                            continue
                        if self.board[pPosition] == Piece.BlK:
                            return True
            
        return False

    
    def playMove(self, start, end):
        pass

    def reverseMove(self):
        pass

    def addMoves(self):
        pass


# game instance
import pygame
import math

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Chess')

# initiate game
game1 = game()

#input related variables
drag = None
drop = None
desiredMove = None

#logic variables
legalityChecked = False

# offsets and other properties
xOffset = 160
yOffset = 60
width = 60
height = 60
blackTileRGB = (160, 84, 41)
whiteTileRGB = (225, 157, 119)

# load images onto a dictionary
pieceImages = {}
for i in range(ord("a"), ord("h") + 1):
    for j in range(1, 9):
        if game1.board[chr(i)][j] is not None:
            pieceImages[game1.board[chr(i)][j].identity] = pygame.transform.smoothscale\
                (pygame.image.load("pieces/" + game1.board[chr(i)][j].identity + ".png"), (width, height))

# create tiles
rectangles = []
for i in range(0, 8):
    for j in range(0, 8):
        if i % 2 == 0:
            if j % 2 == 0:
                rectangles.append([pygame.Rect(((i * width) + xOffset, (j * height) + yOffset), (width, height)), whiteTileRGB])
            else:
                rectangles.append([pygame.Rect(((i * width) + xOffset, (j * height) + yOffset), (width, height)), blackTileRGB])
        else:
            if j % 2 == 0:
                rectangles.append([pygame.Rect(((i * width) + xOffset, (j * height) + yOffset), (width, height)), blackTileRGB])
            else:
                rectangles.append([pygame.Rect(((i * width) + xOffset, (j * height) + yOffset), (width, height)), whiteTileRGB])

clock = pygame.time.Clock()
crashed = False
pressed = False

# game loop
while not crashed:

    ### INPUT ###

    xEdgeDrag = None
    xCoordDrag = None
    yEdgeDrag = None
    yCoordDrag = None

    xEdgeDrop = None
    xCoordDrop = None
    yEdgeDrop = None
    yCoordDrop = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = True
            drag = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            drop = pygame.mouse.get_pos()

            # calculate board position of drag
            xEdgeDrag = (drag[0]-xOffset) % width
            # x: 0 - 7
            xCoordDrag = math.floor((drag[0]-xOffset)/width)
            yEdgeDrag = (drag[1]-yOffset) % height
            # y: 0 - 7
            yCoordDrag = 7 - math.floor((drag[1]-yOffset)/height)

            # calculate board position of drop
            xEdgeDrop = (drop[0]-xOffset) % width
            # x: 0 - 7
            xCoordDrop = math.floor((drop[0]-xOffset)/width)
            yEdgeDrop = (drop[1]-yOffset) % height
            # y: 0 - 7
            yCoordDrop = 7 - math.floor((drop[1]-yOffset)/height)

            desiredMove = [None, None]
            if xEdgeDrag != 0 and yEdgeDrag != 0:
                if 0 <= xCoordDrag < 8 and 0 <= yCoordDrag < 8:
                    desiredMove[0] = (chr(97 + xCoordDrag), yCoordDrag + 1)
            if xEdgeDrop != 0 and yEdgeDrop != 0:
                if 0 <= xCoordDrop < 8 and 0 <= yCoordDrop < 8:
                    desiredMove[1] = (chr(97 + xCoordDrop), yCoordDrop + 1)

            drag = None
            drop = None

    ### UPDATE ###

    # add moves for current player
    # check legality of every available move (filtering step)
    # check if King is checked
    # if king is checked and there is no available move, current player is defeated
    # if king is not checked and there is no available move, the game is drawn

    # white turn
    # click to drag white piece; should not be able to drag black piece
    # if un-clicked on top of a valid square, move selected piece to that square and end white turn
    # update game state

    if game1.ongoing:
        if not game1.movesAdded:
            game1.addMoves()
            game1.movesAdded = True

        if game1.whiteTurn:
            if not legalityChecked:
                # check legality
                temp = None
                invalid = []
                for i in range(8):
                    for j in range(8):
                        if game1.board[chr(97 + i)][j + 1] is not None:
                            for k in game1.board[chr(97 + i)][j + 1].availableMoves:
                                if type(k) == tuple:
                                    temp = game1.board[k[0]][k[1]]
                                    game1.board[k[0]][k[1]] = game1.board[chr(97 + i)][j + 1]
                                    game1.board[k[0]][k[1]].pos = k
                                    game1.board[chr(97 + i)][j + 1] = None

                                    breaker = False
                                    for p in range(8):
                                        if breaker:
                                            break
                                        for q in range(8):
                                            if game1.board[chr(97 + p)][q + 1] is not None:
                                                if game1.board[chr(97 + p)][q + 1].identity[0] == "b":
                                                    if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                        invalid.append(k)
                                                        breaker = True
                                                        break

                                    game1.board[chr(97 + i)][j + 1] = game1.board[k[0]][k[1]]
                                    game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)
                                    game1.board[k[0]][k[1]] = temp
                                    temp = None

                                elif type(k) == str:
                                    if k == "CK":
                                        game1.board['f'][1] = game1.WhRK
                                        game1.WhRK.pos = ('f', 1)
                                        game1.board['g'][1] = game1.WhK
                                        game1.WhK.pos = ('g', 1)
                                        game1.board['e'][1] = None
                                        game1.board['h'][1] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "b":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board['e'][1] = game1.WhK
                                        game1.board['h'][1] = game1.WhRK
                                        game1.WhK.pos = ('e', 1)
                                        game1.WhRK.pos = ('h', 1)
                                        game1.board['f'][1] = None
                                        game1.board['g'][1] = None

                                        # check for tile the king passes through
                                        game1.board['f'][1] = game1.WhK
                                        game1.WhK.pos = ('f', 1)
                                        game1.board['e'][1] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "b":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            if k not in invalid:
                                                                invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board['e'][1] = game1.WhK
                                        game1.WhK.pos = ('e', 1)
                                        game1.board['f'][1] = None

                                    elif k == "CQ":
                                        game1.board['d'][1] = game1.WhRQ
                                        game1.WhRQ.pos = ('d', 1)
                                        game1.board['c'][1] = game1.WhK
                                        game1.WhK.pos = ('c', 1)
                                        game1.board['e'][1] = None
                                        game1.board['a'][1] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "b":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board['e'][1] = game1.WhK
                                        game1.board['a'][1] = game1.WhRQ
                                        game1.WhK.pos = ('e', 1)
                                        game1.WhRQ.pos = ('a', 1)
                                        game1.board['c'][1] = None
                                        game1.board['d'][1] = None

                                        # check for tile the king passes through
                                        game1.board['d'][1] = game1.WhK
                                        game1.WhK.pos = ('d', 1)
                                        game1.board['e'][1] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "b":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            if k not in invalid:
                                                                invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board['e'][1] = game1.WhK
                                        game1.WhK.pos = ('e', 1)
                                        game1.board['d'][1] = None

                                    elif k == "EPI":
                                        temp = game1.board[chr(97 + i + 1)][j + 1]
                                        game1.board[chr(97 + i + 1)][j + 2] = game1.board[chr(97 + i)][j + 1]
                                        game1.board[chr(97 + i)][j + 1] = None
                                        game1.board[chr(97 + i + 1)][j + 1] = None

                                        game1.board[chr(97 + i + 1)][j + 2].pos = (chr(97 + i + 1), j + 2)

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "b":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board[chr(97 + i + 1)][j + 1] = temp
                                        game1.board[chr(97 + i)][j + 1] = game1.board[chr(97 + i + 1)][j + 2]
                                        game1.board[chr(97 + i + 1)][j + 2] = None

                                        game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)
                                        temp = None

                                    elif k == "EPII":
                                        temp = game1.board[chr(97 + i - 1)][j + 1]
                                        game1.board[chr(97 + i - 1)][j + 2] = game1.board[chr(97 + i)][j + 1]
                                        game1.board[chr(97 + i)][j + 1] = None
                                        game1.board[chr(97 + i - 1)][j + 1] = None

                                        game1.board[chr(97 + i - 1)][j + 2].pos = (chr(97 + i - 1), j + 2)

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "b":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board[chr(97 + i - 1)][j + 1] = temp
                                        game1.board[chr(97 + i)][j + 1] = game1.board[chr(97 + i - 1)][j + 2]
                                        game1.board[chr(97 + i - 1)][j + 2] = None

                                        game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)
                                        temp = None

                                    elif k == "PPr0":
                                        game1.board[chr(97 + i)][j + 2] = game1.board[chr(97 + i)][j + 1]
                                        game1.board[chr(97 + i)][j + 1] = None

                                        game1.board[chr(97 + i)][j + 2].pos = (chr(97 + i), j + 2)

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "b":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board[chr(97 + i)][j + 1] = game1.board[chr(97 + i)][j + 2]
                                        game1.board[chr(97 + i)][j + 2] = None

                                        game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)

                                    elif k == "PPrI":
                                        temp = game1.board[chr(97 + i + 1)][j + 2]
                                        game1.board[chr(97 + i + 1)][j + 2] = game1.board[chr(97 + i)][j + 1]
                                        game1.board[chr(97 + i + 1)][j + 2].pos = (chr(97 + i + 1), j + 2)
                                        game1.board[chr(97 + i)][j + 1] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "b":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board[chr(97 + i)][j + 1] = game1.board[chr(97 + i + 1)][j + 2]
                                        game1.board[chr(97 + i + 1)][j + 2] = temp
                                        game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)
                                        temp = None

                                    elif k == "PPrII":
                                        temp = game1.board[chr(97 + i - 1)][j + 2]
                                        game1.board[chr(97 + i - 1)][j + 2] = game1.board[chr(97 + i)][j + 1]
                                        game1.board[chr(97 + i - 1)][j + 2].pos = (chr(97 + i - 1), j + 2)
                                        game1.board[chr(97 + i)][j + 1] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "b":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board[chr(97 + i)][j + 1] = game1.board[chr(97 + i - 1)][j + 2]
                                        game1.board[chr(97 + i - 1)][j + 2] = temp
                                        game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)
                                        temp = None

                            for k in invalid:
                                game1.board[chr(97 + i)][j + 1].availableMoves.remove(k)

                            invalid = []
                legalityChecked = True

            # if no available moves
            movesAvailable = False
            breaker = False
            for i in range(8):
                if breaker:
                    break
                for j in range(8):
                    if game1.board[chr(97 + i)][j + 1] is not None:
                        if game1.board[chr(97 + i)][j + 1].availableMoves == []:
                            pass
                        else:
                            movesAvailable = True
                            breaker = True
                            break
            if movesAvailable:
                pass
            else:
                game1.ongoing = False
                desiredMove = None

            # respond to player action (white)
            if desiredMove is not None:
                if None not in desiredMove:
                    if game1.board[desiredMove[0][0]][desiredMove[0][1]] is not None:
                        if desiredMove[1] in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            # move to desired position
                            if game1.board[desiredMove[1][0]][desiredMove[1][1]] is not None:
                                game1.discard.append(game1.board[desiredMove[1][0]][desiredMove[1][1]])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = False

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = (desiredMove[0], game1.numMoves)
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = desiredMove[1]
                            game1.previousMove.append(desiredMove)

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif desiredMove[1] == ('g', 1) and "CK" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            # perform king-side castle
                            game1.board['f'][1] = game1.WhRK
                            game1.board['g'][1] = game1.WhK
                            game1.WhRK.pos = ('f', 1)
                            game1.WhK.pos = ('g', 1)

                            game1.board['e'][1] = None
                            game1.board['h'][1] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = False

                            game1.WhRK.prevPos = (('h', 1), game1.numMoves)
                            game1.WhK.prevPos = (('e', 1), game1.numMoves)

                            game1.previousMove.append("CK")

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif desiredMove[1] == ('c', 1) and "CQ" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            # perform king-side castle
                            game1.board['d'][1] = game1.WhRQ
                            game1.board['c'][1] = game1.WhK
                            game1.WhRQ.pos = ('d', 1)

                            game1.WhK.pos = ('c', 1)

                            game1.board['e'][1] = None
                            game1.board['a'][1] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = False

                            game1.WhRQ.prevPos = (('a', 1), game1.numMoves)
                            game1.WhK.prevPos = (('e', 1), game1.numMoves)

                            game1.previousMove.append("CQ")

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif game1.newX(desiredMove[0][0], 1) == desiredMove[1][0] and desiredMove[0][1] + 1 == desiredMove[1][1] and "EPI" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            game1.discard.append(game1.board[game1.newX(desiredMove[0][0], 1)][desiredMove[0][1]])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None
                            game1.board[game1.newX(desiredMove[0][0], 1)][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = False

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = (desiredMove[1][0], desiredMove[1][1])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = ((desiredMove[0][0], desiredMove[0][1]), game1.numMoves)

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif game1.newX(desiredMove[0][0], -1) == desiredMove[1][0] and desiredMove[0][1] + 1 == desiredMove[1][1] and "EPII" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            game1.discard.append(game1.board[game1.newX(desiredMove[0][0], -1)][desiredMove[0][1]])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None
                            game1.board[game1.newX(desiredMove[0][0], -1)][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = False

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = (desiredMove[1][0], desiredMove[1][1])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = ((desiredMove[0][0], desiredMove[0][1]), game1.numMoves)

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif desiredMove[0][0] == desiredMove[1][0] and desiredMove[0][1] + 1 == desiredMove[1][1] and "PPr0" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = False

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = (desiredMove[1][0], desiredMove[1][1])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = ((desiredMove[0][0], desiredMove[0][1]), game1.numMoves)

                            while True:
                                promotion = input()
                                if promotion == 'k':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white knight"
                                elif promotion == 'b':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white bishop"
                                elif promotion == 'r':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white rook"
                                elif promotion == 'q':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white queen"
                                else:
                                    continue
                                break

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif game1.newX(desiredMove[0][0], 1) == desiredMove[1][0] and desiredMove[0][1] + 1 == desiredMove[1][1] and "PPrI" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            game1.discard.append(game1.board[desiredMove[1][0]][desiredMove[1][1]])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = False

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = (desiredMove[1][0], desiredMove[1][1])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = ((desiredMove[0][0], desiredMove[0][1]), game1.numMoves)

                            while True:
                                promotion = input()
                                if promotion == 'k':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white knight"
                                elif promotion == 'b':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white bishop"
                                elif promotion == 'r':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white rook"
                                elif promotion == 'q':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white queen"
                                else:
                                    continue
                                break

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif game1.newX(desiredMove[0][0], -1) == desiredMove[1][0] and desiredMove[0][1] + 1 == desiredMove[1][1] and "PPrII" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            game1.discard.append(game1.board[desiredMove[1][0]][desiredMove[1][1]])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = False

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = (desiredMove[1][0], desiredMove[1][1])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = ((desiredMove[0][0], desiredMove[0][1]), game1.numMoves)

                            while True:
                                promotion = input()
                                if promotion == 'k':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white knight"
                                elif promotion == 'b':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white bishop"
                                elif promotion == 'r':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white rook"
                                elif promotion == 'q':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "white queen"
                                else:
                                    continue
                                break

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []
            desiredMove = None

        else:
            if not legalityChecked:
                # check legality
                temp = None
                invalid = []
                for i in range(8):
                    for j in range(8):
                        if game1.board[chr(97 + i)][j + 1] is not None:
                            for k in game1.board[chr(97 + i)][j + 1].availableMoves:
                                if type(k) == tuple:
                                    temp = game1.board[k[0]][k[1]]
                                    game1.board[k[0]][k[1]] = game1.board[chr(97 + i)][j + 1]
                                    game1.board[k[0]][k[1]].pos = k
                                    game1.board[chr(97 + i)][j + 1] = None

                                    breaker = False
                                    for p in range(8):
                                        if breaker:
                                            break
                                        for q in range(8):
                                            if game1.board[chr(97 + p)][q + 1] is not None:
                                                if game1.board[chr(97 + p)][q + 1].identity[0] == "w":
                                                    if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                        invalid.append(k)
                                                        breaker = True
                                                        break

                                    game1.board[chr(97 + i)][j + 1] = game1.board[k[0]][k[1]]
                                    game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)
                                    game1.board[k[0]][k[1]] = temp
                                    temp = None

                                elif type(k) == str:
                                    if k == "CK":
                                        game1.board['f'][8] = game1.BlRK
                                        game1.BlRK.pos = ('f', 8)
                                        game1.board['g'][8] = game1.BlK
                                        game1.BlK.pos = ('g', 8)
                                        game1.board['e'][8] = None
                                        game1.board['h'][8] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "w":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board['e'][8] = game1.BlK
                                        game1.board['h'][8] = game1.BlRK
                                        game1.BlK.pos = ('e', 8)
                                        game1.BlRK.pos = ('h', 8)
                                        game1.board['f'][8] = None
                                        game1.board['g'][8] = None

                                        # check for tile the king passes through
                                        game1.board['f'][8] = game1.BlK
                                        game1.BlK.pos = ('f', 8)
                                        game1.board['e'][8] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "w":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            if k not in invalid:
                                                                invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board['e'][8] = game1.BlK
                                        game1.BlK.pos = ('e', 8)
                                        game1.board['f'][8] = None

                                    elif k == "CQ":
                                        game1.board['d'][8] = game1.BlRQ
                                        game1.BlRQ.pos = ('d', 8)
                                        game1.board['c'][8] = game1.BlK
                                        game1.BlK.pos = ('c', 8)
                                        game1.board['e'][8] = None
                                        game1.board['a'][8] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "w":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board['e'][8] = game1.BlK
                                        game1.board['a'][8] = game1.BlRQ
                                        game1.BlK.pos = ('e', 8)
                                        game1.BlRQ.pos = ('a', 8)
                                        game1.board['c'][8] = None
                                        game1.board['d'][8] = None

                                        # check for tile the king passes through
                                        game1.board['d'][8] = game1.BlK
                                        game1.BlK.pos = ('d', 8)
                                        game1.board['e'][8] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "w":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            if k not in invalid:
                                                                invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board['e'][8] = game1.BlK
                                        game1.BlK.pos = ('e', 8)
                                        game1.board['d'][8] = None

                                    elif k == "EPIII":
                                        temp = game1.board[chr(97 + i - 1)][j + 1]
                                        game1.board[chr(97 + i - 1)][j + 1 - 1] = game1.board[chr(97 + i)][j + 1]
                                        game1.board[chr(97 + i)][j + 1] = None
                                        game1.board[chr(97 + i - 1)][j + 1] = None

                                        game1.board[chr(97 + i - 1)][j + 1 - 1].pos = (chr(97 + i - 1), j + 1 - 1)

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "w":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board[chr(97 + i - 1)][j + 1] = temp
                                        game1.board[chr(97 + i)][j + 1] = game1.board[chr(97 + i - 1)][j + 1 - 1]
                                        game1.board[chr(97 + i - 1)][j + 1 - 1] = None

                                        game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)
                                        temp = None

                                    elif k == "EPIV":
                                        temp = game1.board[chr(97 + i + 1)][j + 1]
                                        game1.board[chr(97 + i + 1)][j + 1 - 1] = game1.board[chr(97 + i)][j + 1]
                                        game1.board[chr(97 + i)][j + 1] = None
                                        game1.board[chr(97 + i + 1)][j + 1] = None

                                        game1.board[chr(97 + i + 1)][j + 1 - 1].pos = (chr(97 + i + 1), j + 1 - 1)

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "w":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board[chr(97 + i + 1)][j + 1] = temp
                                        game1.board[chr(97 + i)][j + 1] = game1.board[chr(97 + i + 1)][j + 1 - 1]
                                        game1.board[chr(97 + i + 1)][j + 1 - 1] = None

                                        game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)
                                        temp = None

                                    elif k == "PPr0":
                                        game1.board[chr(97 + i)][j + 1 - 1] = game1.board[chr(97 + i)][j + 1]
                                        game1.board[chr(97 + i)][j + 1] = None

                                        game1.board[chr(97 + i)][j + 1 - 1].pos = (chr(97 + i), j + 1 - 1)

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "w":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board[chr(97 + i)][j + 1] = game1.board[chr(97 + i)][j + 1 - 1]
                                        game1.board[chr(97 + i)][j + 1 - 1] = None

                                        game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)

                                    elif k == "PPrIII":
                                        temp = game1.board[chr(97 + i - 1)][j + 1 - 1]
                                        game1.board[chr(97 + i - 1)][j + 1 - 1] = game1.board[chr(97 + i)][j + 1]
                                        game1.board[chr(97 + i - 1)][j + 1 - 1].pos = (chr(97 + i - 1), j + 1 - 1)
                                        game1.board[chr(97 + i)][j + 1] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "w":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board[chr(97 + i)][j + 1] = game1.board[chr(97 + i - 1)][j + 1 - 1]
                                        game1.board[chr(97 + i - 1)][j + 1 - 1] = temp
                                        game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)
                                        temp = None

                                    elif k == "PPrIV":
                                        temp = game1.board[chr(97 + i + 1)][j + 1 - 1]
                                        game1.board[chr(97 + i + 1)][j + 1 - 1] = game1.board[chr(97 + i)][j + 1]
                                        game1.board[chr(97 + i + 1)][j + 1 - 1].pos = (chr(97 + i + 1), j + 1 - 1)
                                        game1.board[chr(97 + i)][j + 1] = None

                                        breaker = False
                                        for p in range(8):
                                            if breaker:
                                                break
                                            for q in range(8):
                                                if game1.board[chr(97 + p)][q + 1] is not None:
                                                    if game1.board[chr(97 + p)][q + 1].identity[0] == "w":
                                                        if game1.checks(game1.board[chr(97 + p)][q + 1]) is not None:
                                                            invalid.append(k)
                                                            breaker = True
                                                            break

                                        game1.board[chr(97 + i)][j + 1] = game1.board[chr(97 + i + 1)][j + 1 - 1]
                                        game1.board[chr(97 + i + 1)][j + 1 - 1] = temp
                                        game1.board[chr(97 + i)][j + 1].pos = (chr(97 + i), j + 1)
                                        temp = None

                            for k in invalid:
                                game1.board[chr(97 + i)][j + 1].availableMoves.remove(k)

                            invalid = []
                legalityChecked = True

            # if no available moves
            movesAvailable = False
            breaker = False
            for i in range(8):
                if breaker:
                    break
                for j in range(8):
                    if game1.board[chr(97 + i)][j + 1] is not None:
                        if game1.board[chr(97 + i)][j + 1].availableMoves == []:
                            pass
                        else:
                            movesAvailable = True
                            breaker = True
                            break
            if movesAvailable:
                pass
            else:
                game1.ongoing = False
                desiredMove = None

            # respond to player action (black)
            if desiredMove is not None:
                if None not in desiredMove:
                    if game1.board[desiredMove[0][0]][desiredMove[0][1]] is not None:
                        if desiredMove[1] in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            # move to desired position
                            if game1.board[desiredMove[1][0]][desiredMove[1][1]] is not None:
                                game1.discard.append(game1.board[desiredMove[1][0]][desiredMove[1][1]])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = True

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = (desiredMove[0], game1.numMoves)
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = desiredMove[1]
                            game1.previousMove.append(desiredMove)

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif desiredMove[1] == ('g', 8) and "CK" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            # perform king-side castle
                            game1.board['f'][8] = game1.BlRK
                            game1.board['g'][8] = game1.BlK
                            game1.BlRK.pos = ('f', 8)
                            game1.BlK.pos = ('g', 8)

                            game1.board['e'][8] = None
                            game1.board['h'][8] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = True

                            game1.BlRK.prevPos = (('h', 8), game1.numMoves)
                            game1.BlK.prevPos = (('e', 8), game1.numMoves)

                            game1.previousMove.append("CK")

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif desiredMove[1] == ('c', 8) and "CQ" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            # perform king-side castle
                            game1.board['d'][8] = game1.BlRQ
                            game1.board['c'][8] = game1.BlK
                            game1.BlRQ.pos = ('d', 8)

                            game1.BlK.pos = ('c', 8)

                            game1.board['e'][8] = None
                            game1.board['a'][8] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = True

                            game1.BlRQ.prevPos = (('a', 8), game1.numMoves)
                            game1.BlK.prevPos = (('e', 8), game1.numMoves)

                            game1.previousMove.append("CQ")

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif game1.newX(desiredMove[0][0], -1) == desiredMove[1][0] and desiredMove[0][1] - 1 == desiredMove[1][1] and "EPIII" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            game1.discard.append(game1.board[game1.newX(desiredMove[0][0], -1)][desiredMove[0][1]])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None
                            game1.board[game1.newX(desiredMove[0][0], -1)][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = True

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = (desiredMove[1][0], desiredMove[1][1])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = ((desiredMove[0][0], desiredMove[0][1]), game1.numMoves)

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif game1.newX(desiredMove[0][0], 1) == desiredMove[1][0] and desiredMove[0][1] - 1 == desiredMove[1][1] and "EPIV" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            game1.discard.append(game1.board[game1.newX(desiredMove[0][0], 1)][desiredMove[0][1]])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None
                            game1.board[game1.newX(desiredMove[0][0], 1)][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = True

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = (desiredMove[1][0], desiredMove[1][1])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = ((desiredMove[0][0], desiredMove[0][1]), game1.numMoves)

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif desiredMove[0][0] == desiredMove[1][0] and desiredMove[0][1] - 1 == desiredMove[1][1] and "PPr0" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = True

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = (desiredMove[1][0], desiredMove[1][1])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = ((desiredMove[0][0], desiredMove[0][1]), game1.numMoves)

                            while True:
                                promotion = input()
                                if promotion == 'k':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black knight"
                                elif promotion == 'b':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black bishop"
                                elif promotion == 'r':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black rook"
                                elif promotion == 'q':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black queen"
                                else:
                                    continue
                                break

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif game1.newX(desiredMove[0][0], -1) == desiredMove[1][0] and desiredMove[0][1] - 1 == desiredMove[1][1] and "PPrIII" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            game1.discard.append(game1.board[desiredMove[1][0]][desiredMove[1][1]])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = True

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = (desiredMove[1][0], desiredMove[1][1])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = ((desiredMove[0][0], desiredMove[0][1]), game1.numMoves)

                            while True:
                                promotion = input()
                                if promotion == 'k':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black knight"
                                elif promotion == 'b':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black bishop"
                                elif promotion == 'r':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black rook"
                                elif promotion == 'q':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black queen"
                                else:
                                    continue
                                break

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []

                        elif game1.newX(desiredMove[0][0], 1) == desiredMove[1][0] and desiredMove[0][1] - 1 == desiredMove[1][1] and "PPrIV" in game1.board[desiredMove[0][0]][desiredMove[0][1]].availableMoves:
                            game1.discard.append(game1.board[desiredMove[1][0]][desiredMove[1][1]])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]] = game1.board[desiredMove[0][0]][desiredMove[0][1]]
                            game1.board[desiredMove[0][0]][desiredMove[0][1]] = None

                            # update game variables
                            legalityChecked = False
                            game1.numMoves += 1
                            game1.movesAdded = False
                            game1.whiteTurn = True

                            game1.board[desiredMove[1][0]][desiredMove[1][1]].pos = (desiredMove[1][0], desiredMove[1][1])
                            game1.board[desiredMove[1][0]][desiredMove[1][1]].prevPos = ((desiredMove[0][0], desiredMove[0][1]), game1.numMoves)

                            while True:
                                promotion = input()
                                if promotion == 'k':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black knight"
                                elif promotion == 'b':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black bishop"
                                elif promotion == 'r':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black rook"
                                elif promotion == 'q':
                                    game1.board[desiredMove[1][0]][desiredMove[1][1]].identity = "black queen"
                                else:
                                    continue
                                break

                            # clear available moves
                            for i in range(8):
                                for j in range(8):
                                    if game1.board[chr(97 + i)][j + 1] is not None:
                                        game1.board[chr(97 + i)][j + 1].availableMoves = []
            desiredMove = None
    else:
        if game1.whiteTurn:
            for i in range(8):
                for j in range(8):
                    if game1.board[chr(97 + i)][j + 1] is not None:
                        if game1.board[chr(97 + i)][j + 1].identity[0] == "b":
                            if game1.checks(game1.board[chr(97 + i)][j + 1]) is not None:
                                game1.checked = True
        if not game1.whiteTurn:
            for i in range(8):
                for j in range(8):
                    if game1.board[chr(97 + i)][j + 1] is not None:
                        if game1.board[chr(97 + i)][j + 1].identity[0] == "w":
                            if game1.checks(game1.board[chr(97 + i)][j + 1]) is not None:
                                game1.checked = True

        if game1.whiteTurn and game1.checked:
            print("black wins")
        elif game1.whiteTurn and not game1.checked:
            print("draw")
        elif not game1.whiteTurn and game1.checked:
            print("white wins")
        elif not game1.whiteTurn and not game1.checked:
            print("draw")
        crashed = True

    ### RENDER ###

    # refresh surface with white background
    gameDisplay.fill((255, 255, 255))

    # draw tiles
    for i in rectangles:
        pygame.draw.rect(gameDisplay, i[1], i[0])

    # draw lines
    # vertical
    for i in range(0, 9):
        pygame.draw.line(gameDisplay, (0, 0, 0), ((i * width) + xOffset, yOffset), ((i * width) + xOffset, height*8 + yOffset))

    # horizontal
    for j in range(0, 9):
        pygame.draw.line(gameDisplay, (0, 0, 0),  (xOffset, -(j * height) + (height*8 + yOffset)), (width*8 + xOffset, -(j * height) + (height*8 + yOffset)))

    xEdge = None
    xCoord = None
    yEdge = None
    yCoord = None

    if drag is not None:
        # calculate board position
        xEdge = (drag[0]-xOffset) % width
        # x: 0 - 7
        xCoord = math.floor((drag[0]-xOffset)/width)
        yEdge = (drag[1]-yOffset) % height
        # y: 0 - 7
        yCoord = 7 - math.floor((drag[1]-yOffset)/height)

    for i in range(ord("a"), ord("h") + 1):
        for j in range(1, 9):
            if game1.board[chr(i)][j] is not None:
                if drag is None:
                    gameDisplay.blit(pieceImages[game1.board[chr(i)][j].identity], (((i - 97) * width) + xOffset, -(j * height) + (height*8+yOffset)))

                else:

                    if not chr(xCoord+97) == chr(i) or not yCoord + 1 == j:
                        gameDisplay.blit(pieceImages[game1.board[chr(i)][j].identity], (((i - 97) * width) + xOffset, -(j * height) + (height*8+yOffset)))

    if drag is not None:
        if xEdge != 0 and yEdge != 0:
            if 0 <= xCoord < 8 and 0 <= yCoord < 8:
                if game1.board[chr(xCoord+97)][yCoord + 1] is not None:
                    for k in game1.board[chr(xCoord+97)][yCoord + 1].availableMoves:
                        if type(k) == tuple:
                            pygame.draw.circle(gameDisplay, (200,0,0), (((ord(k[0]) - 97) * 60) + 160 + 30, -(k[1] * 60) + 540 + 30), 10)
                        elif k == "CK":
                            if game1.whiteTurn:
                                pygame.draw.circle(gameDisplay, (200,0,0), (((ord('g') - 97) * 60) + 160 + 30, -(1 * 60) + 540 + 30), 10)
                            else:
                                pygame.draw.circle(gameDisplay, (200,0,0), (((ord('g') - 97) * 60) + 160 + 30, -(8 * 60) + 540 + 30), 10)

                        elif k == "CQ":
                            if game1.whiteTurn:
                                pygame.draw.circle(gameDisplay, (200,0,0), (((ord('c') - 97) * 60) + 160 + 30, -(1 * 60) + 540 + 30), 10)
                            else:
                                pygame.draw.circle(gameDisplay, (200,0,0), (((ord('c') - 97) * 60) + 160 + 30, -(8 * 60) + 540 + 30), 10)
                        elif k == "EPI":
                            pygame.draw.circle(gameDisplay, (200,0,0), (((xCoord + 1) * 60) + 160 + 30, -((yCoord + 1 + 1) * 60) + 540 + 30), 10)
                        elif k == "EPII":
                            pygame.draw.circle(gameDisplay, (200,0,0), (((xCoord - 1) * 60) + 160 + 30, -((yCoord + 1 + 1) * 60) + 540 + 30), 10)
                        elif k == "EPIII":
                            pygame.draw.circle(gameDisplay, (200,0,0), (((xCoord - 1) * 60) + 160 + 30, -((yCoord + 1 - 1) * 60) + 540 + 30), 10)
                        elif k == "EPIV":
                            pygame.draw.circle(gameDisplay, (200,0,0), (((xCoord + 1) * 60) + 160 + 30, -((yCoord + 1 - 1) * 60) + 540 + 30), 10)
                        elif k == "PPr0":
                            if game1.whiteTurn:
                                pygame.draw.circle(gameDisplay, (200,0,0), ((xCoord * 60) + 160 + 30, -((yCoord + 1 + 1) * 60) + 540 + 30), 10)
                            else:
                                pygame.draw.circle(gameDisplay, (200,0,0), ((xCoord * 60) + 160 + 30, -((yCoord + 1 - 1) * 60) + 540 + 30), 10)
                        elif k == "PPrI":
                            pygame.draw.circle(gameDisplay, (200,0,0), (((xCoord + 1) * 60) + 160 + 30, -((yCoord + 1 + 1) * 60) + 540 + 30), 10)
                        elif k == "PPrII":
                            pygame.draw.circle(gameDisplay, (200,0,0), (((xCoord - 1) * 60) + 160 + 30, -((yCoord + 1 + 1) * 60) + 540 + 30), 10)
                        elif k == "PPrIII":
                            pygame.draw.circle(gameDisplay, (200,0,0), (((xCoord - 1) * 60) + 160 + 30, -((yCoord + 1 - 1) * 60) + 540 + 30), 10)
                        elif k == "PPrIV":
                            pygame.draw.circle(gameDisplay, (200,0,0), (((xCoord + 1) * 60) + 160 + 30, -((yCoord + 1 - 1) * 60) + 540 + 30), 10)

                    temp = pygame.mouse.get_pos()
                    gameDisplay.blit(pieceImages[game1.board[chr(xCoord+97)][yCoord + 1].identity], (temp[0] - (width/2), temp[1] - (height/2)))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()

