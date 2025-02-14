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
        self.currentConditions = gameConditions(True, False, False, False, False, False, False)
        self.previousConditions = []
        
        # self.movesAdded = False

        self.numMoves = 0
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

    # check if current player's king is in check
    def checked(self):
        keys = list(self.board.keys())

        # check if white king is checked
        if not self.currentConditions.whiteTurn:
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
                
                # hypothetical
                if self.board[key] == Piece.BlK:
                    x = key[0]
                    y = key[1]
                    for kPosition in [(x+1, y+0), (x+1, y+1), (x+0, y+1), (x-1, y+1), (x-1, y+0), (x-1, y-1), (x+0, y-1), (x+1, y-1)]:
                        if kPosition not in self.board:
                            continue
                        if self.board[kPosition] == Piece.WhK:
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

                # hypothetical
                if self.board[key] == Piece.WhK:
                    x = key[0]
                    y = key[1]
                    for kPosition in [(x+1, y+0), (x+1, y+1), (x+0, y+1), (x-1, y+1), (x-1, y+0), (x-1, y-1), (x+0, y-1), (x+1, y-1)]:
                        if kPosition not in self.board:
                            continue
                        if self.board[kPosition] == Piece.BlK:
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
        if special == "PPrR":
            self.board[end] = Piece.WhR if self.currentConditions.whiteTurn else Piece.BlR
        if special == "PPrB":
            self.board[end] = Piece.WhB if self.currentConditions.whiteTurn else Piece.BlB
        if special == "PPrKn":
            self.board[end] = Piece.WhKn if self.currentConditions.whiteTurn else Piece.BlKn
        
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
            
    def isGameOver(self):
        self.addMoves()
        availableMoves = self.availableMoves
        availableKeys = list(availableMoves.keys())
        if len(availableKeys) == 0:
            if self.currChecked():
                if game1.currentConditions.whiteTurn:
                    # black victory
                    print("black wins")
                    return (True, "black")
                else:
                    # white victory
                    print("white wins")
                    return (True, "white")
            # draw
            else:
                print("draw")
                return (True, "draw")
        return (False, "ongoing")

    def staticEvaluation(self):
        gameover = self.isGameOver()
        if not gameover[0]:
            val = 0
            for i in self.previousTaken:
                if i == Piece.WhP:
                    val -= 1
                elif i == Piece.WhR:
                    val -= 5
                elif i == Piece.WhKn:
                    val -= 3
                elif i == Piece.WhB:
                    val -= 3
                elif i == Piece.WhQ:
                    val -= 6
                elif i == Piece.BlP:
                    val += 1
                elif i == Piece.BlR:
                    val += 5
                elif i == Piece.BlKn:
                    val += 3
                elif i == Piece.BlB:
                    val += 3
                elif i == Piece.BlQ:
                    val += 6
            return val
        else:
            if gameover[1] == "white":
                return float("inf")
            elif gameover[1] == "black":
                return float("-inf")
            elif gameover[1] == "draw":
                return 0



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

def minimax(game, depth, alpha, beta, maximizingPlayer):
    candidateMove = None
    game.addMoves()
    availableMoves = game.availableMoves
    # print(game.availableMoves)
    # print(depth)
    if depth == 0 or (game.isGameOver())[0]:
        return (game.staticEvaluation(), None)
    if maximizingPlayer:
        maxEval = float('-inf')
        
        breakAll = False
        for key in list(availableMoves.keys()):
            if breakAll:
                break
            for move in availableMoves[key]:
                game.playMove(move)
                eval = minimax(game, depth - 1, alpha, beta, False)[0]
                if eval >= maxEval:
                    candidateMove = move
                maxEval = max(maxEval, eval)
                game.reverseMove()
                alpha = max(alpha, eval)
                if beta <= alpha:
                    breakAll = True
                    break
                

        return (maxEval, candidateMove)
    else:
        minEval = float('inf')
        breakAll = False
        for key in list(availableMoves.keys()):
            if breakAll:
                break
            for move in availableMoves[key]:
                game.playMove(move)
                eval = minimax(game, depth - 1, alpha, beta, True)[0]
                if eval <= minEval:
                    candidateMove = move
                minEval = min(minEval, eval)
                game.reverseMove()
                beta = min(beta, eval)
                if beta <= alpha:
                    breakAll = True
                    break
                

                
        return (minEval, candidateMove)
        

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
game1.addMoves()

#input related variables
drag = None
drop = None
desiredMove = None

# offsets and other properties
xOffset = 160
yOffset = 60
width = 60
height = 60
blackTileRGB = (160, 84, 41)
whiteTileRGB = (225, 157, 119)

# load images onto a dictionary
keys = list(Piece.Names.keys())
pieceImages = {}
for i in keys:
    pieceImages[i] = pygame.transform.smoothscale(pygame.image.load("pieces/" + Piece.Names[i] + ".png"), (width, height))

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
    # print(game1.currentConditions.whiteTurn)
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                game1.reverseMove()
                game1.addMoves()
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
                    desiredMove[0] = (xCoordDrag + 1, yCoordDrag + 1)
            if xEdgeDrop != 0 and yEdgeDrop != 0:
                if 0 <= xCoordDrop < 8 and 0 <= yCoordDrop < 8:
                    desiredMove[1] = (xCoordDrop + 1, yCoordDrop + 1)

            drag = None
            drop = None

    ### UPDATE ###

    # availableMoves = game1.availableMoves
    # availableKeys = list(availableMoves.keys())
    # if len(availableKeys) == 0:
    #     if game1.currChecked():
    #         if game1.currentConditions.whiteTurn:
    #             # black victory
    #             print("black wins")
    #             break
    #         else:
    #             # white victory
    #             print("white wins")
    #             break
    #     # draw
    #     else:
    #         print("draw")
    #         break

    if (game1.isGameOver())[0]:
        print(game1.isGameOver())
        continue

    if not game1.currentConditions.whiteTurn:
        (eval, move) = minimax(game1, 4, float('-inf'), float('inf'), False)
        game1.playMove(move)
        # print(move)

    if desiredMove is not None:# and game1.currentConditions.whiteTurn: # and it is a valid move
        # play move
        promotionIntent = None
        if desiredMove[0] in game1.availableMoves:
            for move in game1.availableMoves[desiredMove[0]]:
                ((start, end), special) = move
                if desiredMove != None and desiredMove[1] == end:
                    if len(special) >= 3 and special[0:3] == "PPr":
                        if promotionIntent is None:
                            temp = input()
                            while not (temp == "Q" or temp == "R" or temp == "B" or temp == "Kn"):
                                temp = input()
                            promotionIntent = temp
                        if "PPr" + promotionIntent != special:
                            continue
                        
                    game1.playMove(move)
                    game1.addMoves()
                    desiredMove = None
    else:
        pass
    

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
        xCoord = math.floor((drag[0]-xOffset)/width) + 1
        yEdge = (drag[1]-yOffset) % height
        # y: 0 - 7
        yCoord = 7 - math.floor((drag[1]-yOffset)/height) + 1

        # print((xCoord, yCoord))

    for i in list(game1.board.keys()):
        if drag is None:
            gameDisplay.blit(pieceImages[game1.board[i]], (((i[0]-1) * width) + xOffset, -(i[1] * height) + (height*8+yOffset)))

        elif drag is not None and (xCoord, yCoord) in game1.board:
            if xCoord != i[0] or yCoord != i[1]:
                gameDisplay.blit(pieceImages[game1.board[i]], (((i[0]-1) * width) + xOffset, -(i[1] * height) + (height*8+yOffset)))
            
            temp = pygame.mouse.get_pos()
            gameDisplay.blit(pieceImages[game1.board[(xCoord, yCoord)]], (temp[0] - (width/2), temp[1] - (height/2)))

            # pygame.draw.circle(gameDisplay, (200,0,0), (((ord(k[0]) - 97) * 60) + 160 + 30, -(k[1] * 60) + 540 + 30), 10)
            if (xCoord, yCoord) in game1.availableMoves:
                for move in game1.availableMoves[(xCoord, yCoord)]:
                    ((start, end), special) = move
                    pygame.draw.circle(gameDisplay, (200,0,0), (((end[0]-1) * 60) + 160 + 30, -(end[1] * 60) + 540 + 30), 10)   

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()

