# citations:
## chess piece images: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent

import math
import random
from multiprocessing import Process, Manager
import time

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

        self.Names = {self.WhP:"white pawn", self.WhR:"white rook", self.WhKn:"white knight", self.WhB:"white bishop", self.WhQ:"white queen", self.WhK:"white king", self.BlP:"black pawn", self.BlR:"black rook", self.BlKn:"black knight", self.BlB:"black bishop", self.BlQ:"black queen", self.BlK:"black king"}

Piece = piece()

class gameConditions:
    def __init__(self, wTurn, hasWKM, hasWRQM, hasWRKM, hasBKM, hasBRQM, hasBRKM):
        self.whiteTurn = wTurn
        self.hasWhiteKingMoved = hasWKM
        self.hasWRookQMoved = hasWRQM
        self.hasWRookKMoved = hasWRKM
        self.hasBlackKingMoved = hasBKM
        self.hasBRookQMoved = hasBRQM
        self.hasBRookKMoved = hasBRKM
    def getCopy(self):
        return gameConditions(self.whiteTurn, self.hasWhiteKingMoved, self.hasWRookQMoved, self.hasWRookKMoved, self.hasBlackKingMoved, self.hasBRookQMoved, self.hasBRookKMoved)


class game:
    def __init__(self):
        self.nodesTraversed = 0

        self.currentConditions = gameConditions(True, False, False, False, False, False, False)
        self.previousConditions = []
        
        # self.movesAdded = False

        # for Monte Carlo
        self.actionsInitialized = False
        self.nActions = []

        self.previousMovesHashed = {}
        self.previousMoves = []
        self.previousTaken = []
        self.previousPromoted = []
        self.whitePiecesTaken = []
        self.blackPiecesTaken = []

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
    
    def getCopy(self): #board, conditions, previousMovesHashed):
        newGame = game()
        newGame.board = {}

        for key in self.board:
            newGame.board[key] = self.board[key]

        newGame.currentConditions = self.currentConditions.getCopy()

        for key in self.previousMovesHashed:
            newGame.previousMovesHashed[key] = self.previousMovesHashed[key]
        
        for i in self.previousMoves:
            newGame.previousMoves.append(i)

        for i in self.previousTaken:
            newGame.previousTaken.append(i)

        for i in self.previousPromoted:
            newGame.previousPromoted.append(i)

        for i in self.whitePiecesTaken:
            newGame.whitePiecesTaken.append(i)

        for i in self.blackPiecesTaken:
            newGame.blackPiecesTaken.append(i)

        return newGame


    # check if current player's king is in check
    def checked(self):
        keys = list(self.board.keys())

        # check if white king is checked
        if not self.currentConditions.whiteTurn:
            for key in keys:                
                if self.board[key] == Piece.WhK:
                    # left
                    x = key[0] - 1
                    y = key[1]
                    while x > 0:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x -= 1
                            continue

                        if self.board[(x, y)] == Piece.BlR or self.board[(x, y)] == Piece.BlQ:
                            return True
                        else:
                            break
                    
                    # right
                    x = key[0] + 1
                    y = key[1]
                    while x < 9:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x += 1
                            continue

                        if self.board[(x, y)] == Piece.BlR or self.board[(x, y)] == Piece.BlQ:
                            return True
                        else:
                            break
                    
                    # down
                    x = key[0]
                    y = key[1] - 1
                    while y > 0:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            y -= 1
                            continue

                        if self.board[(x, y)] == Piece.BlR or self.board[(x, y)] == Piece.BlQ:
                            return True
                        else:
                            break
                    
                    # up
                    x = key[0]
                    y = key[1] + 1
                    while y < 9:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            y += 1
                            continue

                        if self.board[(x, y)] == Piece.BlR or self.board[(x, y)] == Piece.BlQ:
                            return True
                        else:
                            break
                    
                    # Diag I
                    x = key[0] + 1
                    y = key[1] + 1
                    while x < 9 and y < 9:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x += 1
                            y += 1
                            continue

                        if self.board[(x, y)] == Piece.BlB or self.board[(x, y)] == Piece.BlQ or (abs(key[0]-x) == 1 and self.board[(x, y)] == Piece.BlP):
                            return True
                        else:
                            break
                    
                    # Diag II
                    x = key[0] - 1
                    y = key[1] + 1
                    while x > 0 and y < 9:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x -= 1
                            y += 1
                            continue

                        if self.board[(x, y)] == Piece.BlB or self.board[(x, y)] == Piece.BlQ or (abs(key[0]-x) == 1 and self.board[(x, y)] == Piece.BlP):
                            return True
                        else:
                            break
                    
                    # Diag III
                    x = key[0] - 1
                    y = key[1] - 1
                    while x > 0 and y > 0:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x -= 1
                            y -= 1
                            continue

                        if self.board[(x, y)] == Piece.BlB or self.board[(x, y)] == Piece.BlQ:
                            return True
                        else:
                            break
                    
                    # Diag IV
                    x = key[0] + 1
                    y = key[1] - 1
                    while x < 9 and y > 0:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x += 1
                            y -= 1
                            continue

                        if self.board[(x, y)] == Piece.BlB or self.board[(x, y)] == Piece.BlQ:
                            return True
                        else:
                            break
                    
                    # Check knights
                    x = key[0]
                    y = key[1]
                    for knPosition in [(x+1, y+2), (x+2, y+1), (x-1, y+2), (x-2, y+1), (x-1, y-2), (x-2, y-1), (x+1, y-2), (x+2, y-1)]:
                        self.nodesTraversed += 1
                        if knPosition not in self.board:
                            continue
                        if self.board[knPosition] == Piece.BlKn:
                            return True
                    
                    # Check kings (hypothetical)
                    x = key[0]
                    y = key[1]
                    for kPosition in [(x+1, y+0), (x+1, y+1), (x+0, y+1), (x-1, y+1), (x-1, y+0), (x-1, y-1), (x+0, y-1), (x+1, y-1)]:
                        self.nodesTraversed += 1
                        if kPosition not in self.board:
                            continue
                        if self.board[kPosition] == Piece.BlK:
                            return True

        # check if black king is checked
        else:
            for key in keys:
                if self.board[key] == Piece.BlK:
                    # left
                    x = key[0] - 1
                    y = key[1]
                    while x > 0:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x -= 1
                            continue

                        if self.board[(x, y)] == Piece.WhR or self.board[(x, y)] == Piece.WhQ:
                            return True
                        else:
                            break
                    
                    # right
                    x = key[0] + 1
                    y = key[1]
                    while x < 9:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x += 1
                            continue

                        if self.board[(x, y)] == Piece.WhR or self.board[(x, y)] == Piece.WhQ:
                            return True
                        else:
                            break
                    
                    # down
                    x = key[0]
                    y = key[1] - 1
                    while y > 0:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            y -= 1
                            continue

                        if self.board[(x, y)] == Piece.WhR or self.board[(x, y)] == Piece.WhQ:
                            return True
                        else:
                            break
                    
                    # up
                    x = key[0]
                    y = key[1] + 1
                    while y < 9:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            y += 1
                            continue

                        if self.board[(x, y)] == Piece.WhR or self.board[(x, y)] == Piece.WhQ:
                            return True
                        else:
                            break
                    
                    # Diag I
                    x = key[0] + 1
                    y = key[1] + 1
                    while x < 9 and y < 9:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x += 1
                            y += 1
                            continue

                        if self.board[(x, y)] == Piece.WhB or self.board[(x, y)] == Piece.WhQ:
                            return True
                        else:
                            break
                    
                    # Diag II
                    x = key[0] - 1
                    y = key[1] + 1
                    while x > 0 and y < 9:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x -= 1
                            y += 1
                            continue

                        if self.board[(x, y)] == Piece.WhB or self.board[(x, y)] == Piece.WhQ:
                            return True
                        else:
                            break
                    
                    # Diag III
                    x = key[0] - 1
                    y = key[1] - 1
                    while x > 0 and y > 0:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x -= 1
                            y -= 1
                            continue

                        if self.board[(x, y)] == Piece.WhB or self.board[(x, y)] == Piece.WhQ or (abs(key[0]-x) == 1 and self.board[(x, y)] == Piece.WhP):
                            return True
                        else:
                            break
                    
                    # Diag IV
                    x = key[0] + 1
                    y = key[1] - 1
                    while x < 9 and y > 0:
                        self.nodesTraversed += 1
                        if (x, y) not in self.board:
                            x += 1
                            y -= 1
                            continue

                        if self.board[(x, y)] == Piece.WhB or self.board[(x, y)] == Piece.WhQ or (abs(key[0]-x) == 1 and self.board[(x, y)] == Piece.WhP):
                            return True
                        else:
                            break
                    
                    # Check knights
                    x = key[0]
                    y = key[1]
                    for knPosition in [(x+1, y+2), (x+2, y+1), (x-1, y+2), (x-2, y+1), (x-1, y-2), (x-2, y-1), (x+1, y-2), (x+2, y-1)]:
                        self.nodesTraversed += 1
                        if knPosition not in self.board:
                            continue
                        if self.board[knPosition] == Piece.WhKn:
                            return True
                    
                    # Check kings (hypothetical)
                    x = key[0]
                    y = key[1]
                    for kPosition in [(x+1, y+0), (x+1, y+1), (x+0, y+1), (x-1, y+1), (x-1, y+0), (x-1, y-1), (x+0, y-1), (x+1, y-1)]:
                        self.nodesTraversed += 1
                        if kPosition not in self.board:
                            continue
                        if self.board[kPosition] == Piece.WhK:
                            return True
        return False

    def currChecked(self):
        self.currentConditions.whiteTurn = not self.currentConditions.whiteTurn
        toReturn = self.checked()
        self.currentConditions.whiteTurn = not self.currentConditions.whiteTurn
        return toReturn

    def playMove(self, move):
        self.previousMoves.append(move)
        ((start, end), special) = move

        self.previousConditions.append(self.currentConditions)
        self.currentConditions = self.currentConditions.getCopy()
        if special == "" or special == "WK" or special == "BK" or (len(special) >= 3 and special[0:3] == "PPr"):
            if self.board[start] == Piece.WhR and start == (1, 1):
                self.currentConditions.hasWRookQMoved = True
            elif self.board[start] == Piece.WhR and start == (8, 1):
                self.currentConditions.hasWRookKMoved = True
            elif self.board[start] == Piece.BlR and start == (1, 8):
                self.currentConditions.hasBRookQMoved = True
            elif self.board[start] == Piece.BlR and start == (8, 8):
                self.currentConditions.hasBRookKMoved = True
             
            if end in self.board:
                self.previousTaken.append(self.board[end])

                if self.board[end] == Piece.WhR and end == (1, 1):
                    self.currentConditions.hasWRookQMoved = True
                elif self.board[end] == Piece.WhR and end == (8, 1):
                    self.currentConditions.hasWRookKMoved = True
                elif self.board[end] == Piece.BlR and end == (1, 8):
                    self.currentConditions.hasBRookQMoved = True
                elif self.board[end] == Piece.BlR and end == (8, 8):
                    self.currentConditions.hasBRookKMoved = True
                    
            else:
                self.previousTaken.append(None)
            self.board[end] = self.board[start]
            self.board.pop(start)

        if special == "WK":
            self.currentConditions.hasWhiteKingMoved = True
        
        if special == "BK":
            self.currentConditions.hasBlackKingMoved = True

        if special == "WQC":
            self.board[(3, 1)] = Piece.WhK
            self.board[(4, 1)] = Piece.WhR
            self.board.pop((1, 1))
            self.board.pop((5, 1))
            self.previousTaken.append(None)
            self.currentConditions.hasWhiteKingMoved = True
            self.currentConditions.hasWRookQMoved = True
        
        if special == "BQC":
            self.board[(3, 8)] = Piece.BlK
            self.board[(4, 8)] = Piece.BlR
            self.board.pop((1, 8))
            self.board.pop((5, 8))
            self.previousTaken.append(None)
            self.currentConditions.hasBlackKingMoved = True
            self.currentConditions.hasBRookQMoved = True
        
        if special == "WKC":
            self.board[(7, 1)] = Piece.WhK
            self.board[(6, 1)] = Piece.WhR
            self.board.pop((8, 1))
            self.board.pop((5, 1))
            self.previousTaken.append(None)
            self.currentConditions.hasWhiteKingMoved = True
            self.currentConditions.hasWRookKMoved = True
        
        if special == "BKC":
            self.board[(7, 8)] = Piece.BlK
            self.board[(6, 8)] = Piece.BlR
            self.board.pop((8, 8))
            self.board.pop((5, 8))
            self.previousTaken.append(None)
            self.currentConditions.hasBlackKingMoved = True
            self.currentConditions.hasBRookKMoved = True
        
        if special == "EP":
            self.board[end] = self.board[start]
            self.board.pop(start)
            self.previousTaken.append(self.board[(end[0], start[1])])
            self.board.pop((end[0], start[1]))
        
        
        if special == "PPrQ":
            self.board[end] = Piece.WhQ if self.currentConditions.whiteTurn else Piece.BlQ
            self.previousPromoted.append(self.board[end])
        if special == "PPrR":
            self.board[end] = Piece.WhR if self.currentConditions.whiteTurn else Piece.BlR
            self.previousPromoted.append(self.board[end])
        if special == "PPrB":
            self.board[end] = Piece.WhB if self.currentConditions.whiteTurn else Piece.BlB
            self.previousPromoted.append(self.board[end])
        if special == "PPrKn":
            self.board[end] = Piece.WhKn if self.currentConditions.whiteTurn else Piece.BlKn
            self.previousPromoted.append(self.board[end])
        
        self.currentConditions.whiteTurn = not self.currentConditions.whiteTurn

    def reverseMove(self):
        self.currentConditions = self.previousConditions.pop()
        ((start, end), special) = self.previousMoves.pop()
        previousTaken = self.previousTaken.pop()

        if special == "" or special == "WK" or special == "BK" or (len(special) >= 3 and special[0:3] == "PPr"):
            self.board[start] = self.board[end]
            if previousTaken == None:
                self.board.pop(end)
            else:
                self.board[end] = previousTaken
        
        if special == "WQC":
            self.board[(1, 1)] = Piece.WhR
            self.board[(5, 1)] = Piece.WhK
            self.board.pop((3, 1))
            self.board.pop((4, 1))
        
        if special == "BQC":
            self.board[(1, 8)] = Piece.BlR
            self.board[(5, 8)] = Piece.BlK
            self.board.pop((3, 8))
            self.board.pop((4, 8))
        
        if special == "WKC":
            self.board[(5, 1)] = Piece.WhK
            self.board[(8, 1)] = Piece.WhR
            self.board.pop((7, 1))
            self.board.pop((6, 1))
        
        if special == "BKC":
            self.board[(5, 8)] = Piece.BlK
            self.board[(8, 8)] = Piece.BlR
            self.board.pop((7, 8))
            self.board.pop((6, 8))
        
        if special == "EP":
            self.board[start] = self.board[end]
            self.board.pop(end)
            self.board[(end[0], start[1])] = previousTaken
        
        if special == "PPrQ" or special == "PPrR" or special == "PPrB" or special == "PPrKn":
            self.board[start] = Piece.WhP if self.currentConditions.whiteTurn else Piece.BlP
            self.previousPromoted.pop()
            
    def isGameOver(self):
        _hash = self.hashOnlyBoard()
        if _hash in self.previousMovesHashed:
            if self.previousMovesHashed[_hash] == 3:
                return (True, "draw")

        self.addMoves()
        availableMoves = self.availableMoves
        availableKeys = list(availableMoves.keys())
        if len(availableKeys) == 0:
            if self.currChecked():
                if self.currentConditions.whiteTurn:
                    # black victory
                    # print("black wins")
                    return (True, "black")
                else:
                    # white victory
                    # print("white wins")
                    return (True, "white")
            # draw
            else:
                # print("draw")
                return (True, "draw")
        else:
            count = 0
            whiteKing = False
            blackKing = False
            for i in range(1, 9):
                for j in range(1, 9):
                    if (i, j) in self.board:
                        count += 1
                        if self.board[(i, j)] == Piece.WhK:
                            whiteKing = True
                        elif self.board[(i,j)] == Piece.BlK:
                            blackKing = True
            if count == 2 and whiteKing and blackKing:
                print("draw")
                return (True, "draw")
        if len(self.previousTaken) >= 100:
            return (True, "draw")
        return (False, "ongoing")

    def staticEvaluation(self):
        gameover = self.isGameOver()
        if not gameover[0]:
            return 0
        else:
            if gameover[1] == "white":
                return 1
            elif gameover[1] == "black":
                return -1
            elif gameover[1] == "draw":
                return 0

    def hashBoard(self):
        hashString = ""
        for i in range(1, 9):
            for j in range(1, 9):
                if (i, j) in self.board:
                    hashString += str(i)
                    hashString += str(j)
                    hashString += str(self.board[(i, j)])
        hashString += str(int(self.currentConditions.hasBlackKingMoved))
        hashString += str(int(self.currentConditions.hasBRookKMoved))
        hashString += str(int(self.currentConditions.hasBRookQMoved))
        hashString += str(int(self.currentConditions.hasWhiteKingMoved))
        hashString += str(int(self.currentConditions.hasWRookKMoved))
        hashString += str(int(self.currentConditions.hasWRookQMoved))
        hashString += str(int(self.currentConditions.whiteTurn))
        return hashString

    def hashOnlyBoard(self):
        hashString = ""
        for i in range(1, 9):
            for j in range(1, 9):
                if (i, j) in self.board:
                    hashString += str(i)
                    hashString += str(j)
                    hashString += str(self.board[(i, j)])
        return hashString

    def hashBitBoard(self):
        WhP = 0
        WhR = 0
        WhKn = 0
        WhB = 0
        WhQ = 0
        WhK = 0
        BlP = 0
        BlR = 0
        BlKn = 0
        BlB = 0
        BlQ = 0
        BlK = 0

        for i in range(1, 9):
            for j in range(1, 9):
                if (i, j) in self.board:
                    if self.board[(i, j)] == Piece.WhP:
                        WhP |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.WhR:
                        WhR |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.WhKn:
                        WhKn |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.WhB:
                        WhB |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.WhQ:
                        WhQ |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.WhK:
                        WhK |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.BlP:
                        BlP |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.BlR:
                        BlR |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.BlKn:
                        BlKn |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.BlB:
                        BlB |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.BlQ:
                        BlQ |= (1 << (i * 8 + j))
                    if self.board[(i, j)] == Piece.BlK:
                        BlK |= (1 << (i * 8 + j))

        return (WhP, WhR, WhKn, WhB, WhQ, WhK, BlP, BlR, BlKn, BlB, BlQ, BlK, int(self.currentConditions.hasBlackKingMoved),
                int(self.currentConditions.hasBRookKMoved), int(self.currentConditions.hasBRookQMoved), 
                int(self.currentConditions.hasWhiteKingMoved), int(self.currentConditions.hasWRookKMoved), 
                int(self.currentConditions.hasWRookQMoved), int(self.currentConditions.whiteTurn))

    # add legal moves
    def addMoves(self):
        keys = list(self.board.keys())
        self.availableMoves = {}

        # add moves for white
        if self.currentConditions.whiteTurn:
            for key in keys:
                self.availableMoves[key] = []

                if self.board[key] == Piece.WhR or self.board[key] == Piece.WhQ:
                    # left
                    x = key[0] - 1
                    y = key[1]
                    while x > 0:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), "")) # special == "WRQ" if queen side rook to keep track of castling condition
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            x -= 1
                            continue
                        
                        # if the piece in question is a black piece
                        if (self.board[(x, y)] > 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break

                    # right
                    x = key[0] + 1
                    y = key[1]
                    while x < 9:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            x += 1
                            continue
                        
                        # if the piece in question is a black piece
                        if (self.board[(x, y)] > 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                    
                    # down
                    x = key[0]
                    y = key[1] - 1
                    while y > 0:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            y -= 1
                            continue
                        
                        # if the piece in question is a black piece
                        if (self.board[(x, y)] > 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                    
                    # up
                    x = key[0]
                    y = key[1] + 1
                    while y < 9:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            y += 1
                            continue
                        
                        # if the piece in question is a black piece
                        if (self.board[(x, y)] > 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                
                if self.board[key] == Piece.WhB or self.board[key] == Piece.WhQ:
                    # Diag I
                    x = key[0] + 1
                    y = key[1] + 1
                    
                    while x < 9 and y < 9:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            x += 1
                            y += 1
                            continue
                        
                        # if the piece in question is a black piece
                        if (self.board[(x, y)] > 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break

                    # Diag II
                    x = key[0] - 1
                    y = key[1] + 1
                    while x > 0 and y < 9:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            x -= 1
                            y += 1
                            continue
                        
                        # if the piece in question is a black piece
                        if (self.board[(x, y)] > 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                    
                    # Diag III
                    x = key[0] - 1
                    y = key[1] - 1
                    while x > 0 and y > 0:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            x -= 1
                            y -= 1
                            continue
                        
                        # if the piece in question is a black piece
                        if (self.board[(x, y)] > 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                    
                    # Diag IV
                    x = key[0] + 1
                    y = key[1] - 1
                    while x < 9 and y > 0:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                            
                            x += 1
                            y -= 1
                            continue
                        
                        # if the piece in question is a black piece
                        if (self.board[(x, y)] > 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                
                if self.board[key] == Piece.WhKn:
                    x = key[0]
                    y = key[1]
                    for knPosition in [(x+1, y+2), (x+2, y+1), (x-1, y+2), (x-2, y+1), (x-1, y-2), (x-2, y-1), (x+1, y-2), (x+2, y-1)]:
                        if knPosition not in self.board:
                            if 0 < knPosition[0] < 9 and 0 < knPosition[1] < 9:
                                self.playMove(((key, knPosition), ""))
                                if not self.checked():
                                    self.availableMoves[key].append(((key, knPosition), ""))
                                self.reverseMove()
                        
                        elif self.board[knPosition] > 5:
                            self.playMove(((key, knPosition), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, knPosition), ""))
                            self.reverseMove()
                
                if self.board[key] == Piece.WhK:
                    # [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
                    x = key[0]
                    y = key[1]
                    for kPosition in [(x+1, y+0), (x+1, y+1), (x+0, y+1), (x-1, y+1), (x-1, y+0), (x-1, y-1), (x+0, y-1), (x+1, y-1)]:
                        if kPosition not in self.board and 0 < kPosition[0] < 9 and 0 < kPosition[1] < 9:
                            self.playMove(((key, kPosition), "WK"))
                            if not self.checked():
                                self.availableMoves[key].append(((key, kPosition), "WK"))
                            self.reverseMove()
                        elif 0 < kPosition[0] < 9 and 0 < kPosition[1] < 9 and self.board[kPosition] > 5:
                            self.playMove(((key, kPosition), "WK"))
                            if not self.checked():
                                self.availableMoves[key].append(((key, kPosition), "WK"))
                            self.reverseMove()

                    # cannot currently be in check and king cannot cross through check. (DONE)
                    # you also have to check if the rook is captured or not. It could have never moved but still have been captured... (DONE)
                    if not self.currChecked() and not self.currentConditions.hasWhiteKingMoved and not self.currentConditions.hasWRookQMoved:
                        if (2, 1) not in self.board and (3, 1) not in self.board and (4, 1) not in self.board:
                            self.playMove(((key, (3, 1)), "WQC"))
                            self.board[(3, 1)] = Piece.WhK
                            self.board[(4, 1)] = Piece.WhK
                            if not self.checked():
                                self.availableMoves[key].append(((key, (3, 1)), "WQC"))
                            self.reverseMove()
                            
                    if not self.currChecked() and not self.currentConditions.hasWhiteKingMoved and not self.currentConditions.hasWRookKMoved:
                        if (6, 1) not in self.board and (7, 1) not in self.board:
                            self.playMove(((key, (7, 1)), "WKC"))
                            self.board[(6, 1)] = Piece.WhK
                            if not self.checked():
                                self.availableMoves[key].append(((key, (7, 1)), "WKC"))
                            self.reverseMove()
                
                if self.board[key] == Piece.WhP:
                    x = key[0]
                    y = key[1]
                    # if pawn in starting position
                    if y == 2:
                        if (x, y+2) not in self.board and (x, y+1) not in self.board:
                            self.playMove(((key, (x, y+2)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y+2)), ""))
                            self.reverseMove()
                    
                    if (x, y+1) not in self.board:
                        self.playMove(((key, (x, y+1)), ""))
                        if not self.checked():
                            if y+1 < 8:
                                self.availableMoves[key].append(((key, (x, y+1)), ""))
                            else:
                                self.availableMoves[key].append(((key, (x, y+1)), "PPrQ"))
                                self.availableMoves[key].append(((key, (x, y+1)), "PPrR"))
                                self.availableMoves[key].append(((key, (x, y+1)), "PPrB"))
                                self.availableMoves[key].append(((key, (x, y+1)), "PPrKn"))
                        self.reverseMove()
                    
                    if (x+1, y+1) in self.board and self.board[(x+1, y+1)] > 5:
                        self.playMove(((key, (x+1, y+1)), ""))
                        if not self.checked():
                            if y+1 < 8:
                                self.availableMoves[key].append(((key, (x+1, y+1)), ""))
                            else: 
                                self.availableMoves[key].append(((key, (x+1, y+1)), "PPrQ"))
                                self.availableMoves[key].append(((key, (x+1, y+1)), "PPrR"))
                                self.availableMoves[key].append(((key, (x+1, y+1)), "PPrB"))
                                self.availableMoves[key].append(((key, (x+1, y+1)), "PPrKn"))
                        self.reverseMove()
                    
                    if (x-1, y+1) in self.board and self.board[(x-1, y+1)] > 5:
                        self.playMove(((key, (x-1, y+1)), ""))
                        if not self.checked():
                            if y+1 < 8:
                                self.availableMoves[key].append(((key, (x-1, y+1)), ""))
                            else:
                                self.availableMoves[key].append(((key, (x-1, y+1)), "PPrQ"))
                                self.availableMoves[key].append(((key, (x-1, y+1)), "PPrR"))
                                self.availableMoves[key].append(((key, (x-1, y+1)), "PPrB"))
                                self.availableMoves[key].append(((key, (x-1, y+1)), "PPrKn"))
                        self.reverseMove()

                    # if pawn eligible for en passant
                    if y == 5:
                        if (x-1, y) in self.board and self.board[(x-1, y)] == 6 and (x-1, y+1) not in self.board:
                            ((start, end), special) = self.previousMoves[len(self.previousMoves) - 1]
                            if start == (x-1, y+2) and end  == (x-1, y):
                                self.playMove(((key, (x-1, y+1)), "EP"))
                                if not self.checked():
                                    self.availableMoves[key].append(((key, (x-1, y+1)), "EP"))
                                self.reverseMove()
                        if (x+1, y) in self.board and self.board[(x+1, y)] == 6 and (x+1, y+1) not in self.board:
                            ((start, end), special) = self.previousMoves[len(self.previousMoves) - 1]
                            if start == (x+1, y+2) and end  == (x+1, y):
                                self.playMove(((key, (x+1, y+1)), "EP"))
                                if not self.checked():
                                    self.availableMoves[key].append(((key, (x+1, y+1)), "EP"))
                                self.reverseMove()
                    
                if len(self.availableMoves[key]) == 0:
                    self.availableMoves.pop(key)
        # add moves for black
        else:
            for key in keys:
                self.availableMoves[key] = []

                if self.board[key] == Piece.BlR or self.board[key] == Piece.BlQ:
                    # left
                    x = key[0] - 1
                    y = key[1]
                    while x > 0:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            x -= 1
                            continue
                        
                        # if the piece in question is a white piece
                        if (self.board[(x, y)] <= 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break

                    # right
                    x = key[0] + 1
                    y = key[1]
                    while x < 9:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            x += 1
                            continue
                        
                        # if the piece in question is a white piece
                        if (self.board[(x, y)] <= 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                    
                    # down
                    x = key[0]
                    y = key[1] - 1
                    while y > 0:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            y -= 1
                            continue
                        
                        # if the piece in question is a white piece
                        if (self.board[(x, y)] <= 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                    
                    # up
                    x = key[0]
                    y = key[1] + 1
                    while y < 9:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            y += 1
                            continue
                        
                        # if the piece in question is a white piece
                        if (self.board[(x, y)] <= 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                
                if self.board[key] == Piece.BlB or self.board[key] == Piece.BlQ:
                    # Diag I
                    x = key[0] + 1
                    y = key[1] + 1
                    while x < 9 and y < 9:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            x += 1
                            y += 1
                            continue
                        
                        # if the piece in question is a white piece
                        if (self.board[(x, y)] <= 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break

                    # Diag II
                    x = key[0] - 1
                    y = key[1] + 1
                    while x > 0 and y < 9:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            x -= 1
                            y += 1
                            continue
                        
                        # if the piece in question is a white piece
                        if (self.board[(x, y)] <= 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                    
                    # Diag III
                    x = key[0] - 1
                    y = key[1] - 1
                    while x > 0 and y > 0:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()

                            x -= 1
                            y -= 1
                            continue
                        
                        # if the piece in question is a white piece
                        if (self.board[(x, y)] <= 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                    
                    # Diag IV
                    x = key[0] + 1
                    y = key[1] - 1
                    while x < 9 and y > 0:
                        if (x, y) not in self.board:                            
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                            
                            x += 1
                            y -= 1
                            continue
                        
                        # if the piece in question is a white piece
                        if (self.board[(x, y)] <= 5):
                            self.playMove(((key, (x, y)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y)), ""))
                            self.reverseMove()
                        break
                
                if self.board[key] == Piece.BlKn:
                    x = key[0]
                    y = key[1]
                    for knPosition in [(x+1, y+2), (x+2, y+1), (x-1, y+2), (x-2, y+1), (x-1, y-2), (x-2, y-1), (x+1, y-2), (x+2, y-1)]:
                        if knPosition not in self.board:
                            if 0 < knPosition[0] < 9 and 0 < knPosition[1] < 9:
                                self.playMove(((key, knPosition), ""))
                                if not self.checked():
                                    self.availableMoves[key].append(((key, knPosition), ""))
                                self.reverseMove()
                        
                        elif self.board[knPosition] <= 5:
                            self.playMove(((key, knPosition), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, knPosition), ""))
                            self.reverseMove()
                
                if self.board[key] == Piece.BlK:
                    # [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
                    x = key[0]
                    y = key[1]
                    for kPosition in [(x+1, y+0), (x+1, y+1), (x+0, y+1), (x-1, y+1), (x-1, y+0), (x-1, y-1), (x+0, y-1), (x+1, y-1)]:
                        if kPosition not in self.board and 0 < kPosition[0] < 9 and 0 < kPosition[1] < 9:
                            self.playMove(((key, kPosition), "BK"))
                            if not self.checked():
                                self.availableMoves[key].append(((key, kPosition), "BK"))
                            self.reverseMove()
                        elif 0 < kPosition[0] < 9 and 0 < kPosition[1] < 9 and self.board[kPosition] <= 5:
                            self.playMove(((key, kPosition), "BK"))
                            if not self.checked():
                                self.availableMoves[key].append(((key, kPosition), "BK"))
                            self.reverseMove()
                    
                    if not self.currChecked() and not self.currentConditions.hasBlackKingMoved and not self.currentConditions.hasBRookQMoved:
                        if (2, 8) not in self.board and (3, 8) not in self.board and (4, 8) not in self.board:
                            self.playMove(((key, (3, 8)), "BQC"))
                            self.board[(3, 8)] = Piece.BlK
                            self.board[(4, 8)] = Piece.BlK
                            if not self.checked():
                                self.availableMoves[key].append(((key, (3, 8)), "BQC"))
                            self.reverseMove()
                            
                    if not self.currChecked() and not self.currentConditions.hasBlackKingMoved and not self.currentConditions.hasBRookKMoved:
                        if (6, 8) not in self.board and (7, 8) not in self.board:
                            self.playMove(((key, (7, 8)), "BKC"))
                            self.board[(6, 8)] = Piece.BlK
                            if not self.checked():
                                self.availableMoves[key].append(((key, (7, 8)), "BKC"))
                            self.reverseMove()
                
                if self.board[key] == Piece.BlP:
                    x = key[0]
                    y = key[1]
                    # if pawn in starting position
                    if y == 7:
                        if (x, y-2) not in self.board and (x, y-1) not in self.board:
                            self.playMove(((key, (x, y-2)), ""))
                            if not self.checked():
                                self.availableMoves[key].append(((key, (x, y-2)), ""))
                            self.reverseMove()
                    
                    if (x, y-1) not in self.board:
                        self.playMove(((key, (x, y-1)), ""))
                        if not self.checked():
                            if y-1 > 1:
                                self.availableMoves[key].append(((key, (x, y-1)), ""))
                            else:
                                self.availableMoves[key].append(((key, (x, y-1)), "PPrQ"))
                                self.availableMoves[key].append(((key, (x, y-1)), "PPrR"))
                                self.availableMoves[key].append(((key, (x, y-1)), "PPrB"))
                                self.availableMoves[key].append(((key, (x, y-1)), "PPrKn"))
                        self.reverseMove()
                    
                    if (x+1, y-1) in self.board and self.board[(x+1, y-1)] <= 5:
                        self.playMove(((key, (x+1, y-1)), ""))
                        if not self.checked():
                            if y-1 > 1:
                                self.availableMoves[key].append(((key, (x+1, y-1)), ""))
                            else: 
                                self.availableMoves[key].append(((key, (x+1, y-1)), "PPrQ"))
                                self.availableMoves[key].append(((key, (x+1, y-1)), "PPrR"))
                                self.availableMoves[key].append(((key, (x+1, y-1)), "PPrB"))
                                self.availableMoves[key].append(((key, (x+1, y-1)), "PPrKn"))
                        self.reverseMove()
                    
                    if (x-1, y-1) in self.board and self.board[(x-1, y-1)] <= 5:
                        self.playMove(((key, (x-1, y-1)), ""))
                        if not self.checked():
                            if y-1 > 1:
                                self.availableMoves[key].append(((key, (x-1, y-1)), ""))
                            else:
                                self.availableMoves[key].append(((key, (x-1, y-1)), "PPrQ"))
                                self.availableMoves[key].append(((key, (x-1, y-1)), "PPrR"))
                                self.availableMoves[key].append(((key, (x-1, y-1)), "PPrB"))
                                self.availableMoves[key].append(((key, (x-1, y-1)), "PPrKn"))
                        self.reverseMove()

                    # if pawn eligible for en passant
                    if y == 4:
                        if (x-1, y) in self.board and self.board[(x-1, y)] == 0 and (x-1, y-1) not in self.board:
                            ((start, end), special) = self.previousMoves[len(self.previousMoves) - 1]
                            if start == (x-1, y-2) and end  == (x-1, y):
                                self.playMove(((key, (x-1, y-1)), "EP"))
                                if not self.checked():
                                    self.availableMoves[key].append(((key, (x-1, y-1)), "EP"))
                                self.reverseMove()
                        if (x+1, y) in self.board and self.board[(x+1, y)] == 0 and (x+1, y-1) not in self.board:
                            ((start, end), special) = self.previousMoves[len(self.previousMoves) - 1]
                            if start == (x+1, y-2) and end  == (x+1, y):
                                self.playMove(((key, (x+1, y-1)), "EP"))
                                if not self.checked():
                                    self.availableMoves[key].append(((key, (x+1, y-1)), "EP"))
                                self.reverseMove()
                    
                if len(self.availableMoves[key]) == 0:
                    self.availableMoves.pop(key)


game1 = game()
print(game1.hashBitBoard())
# if __name__ == '__main__':

#     crashed = False
#     pressed = False

#     # game loop
#     while not crashed:

#         ### UPDATE ###

#         if (game1.isGameOver())[0]:
#             print("game over!") #game1.isGameOver(), "game over!")
#             game1 = game()
#             _hash = {}

#         if True:
#             if not game1.currentConditions.whiteTurn:
#                 move = MCTS(game1.getCopy(), False, nodeLookUp)

#                 game1.playMove(move)
#                 _hash = game1.hashOnlyBoard()
#                 if _hash not in game1.previousMovesHashed:
#                     game1.previousMovesHashed[_hash] = 1
#                 else:
#                     game1.previousMovesHashed[_hash] += 1

#                 game1.addMoves()


