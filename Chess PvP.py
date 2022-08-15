# citations:
## chess piece images: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent

class piece:
    def __init__(self, identity, x, y):
        self.identity = identity
        self.pos = (x, y)
        self.prevPos = (None, None)

        self.availableMoves = []
        self.specialMoves = []

class game:
    def __init__(self):
        self.ongoing = True
        self.checked = False
        self.win = False
        self.movesAdded = False

        self.previousMove = []
        self.whiteTurn = True

        self.numMoves = 0

        self.board = {}
        self.discard = []

        for i in range(8):
            self.board[chr(97 + i)] = {}
            for j in range(8):
                self.board[chr(97 + i)][j + 1] = None

        self.WhRQ = piece("white rook", 'a', 1)
        self.board[self.WhRQ.pos[0]][self.WhRQ.pos[1]] = self.WhRQ
        self.WhKnQ = piece("white knight", 'b', 1)
        self.board[self.WhKnQ.pos[0]][self.WhKnQ.pos[1]] = self.WhKnQ
        self.WhBQ = piece("white bishop", 'c', 1)
        self.board[self.WhBQ.pos[0]][self.WhBQ.pos[1]] = self.WhBQ
        self.WhQ = piece("white queen", 'd', 1)
        self.board[self.WhQ.pos[0]][self.WhQ.pos[1]] = self.WhQ
        self.WhK = piece("white king", 'e', 1)
        self.board[self.WhK.pos[0]][self.WhK.pos[1]] = self.WhK
        self.WhBK = piece("white bishop", 'f', 1)
        self.board[self.WhBK.pos[0]][self.WhBK.pos[1]] = self.WhBK
        self.WhKnK = piece("white knight", 'g', 1)
        self.board[self.WhKnK.pos[0]][self.WhKnK.pos[1]] = self.WhKnK
        self.WhRK = piece("white rook", 'h', 1)
        self.board[self.WhRK.pos[0]][self.WhRK.pos[1]] = self.WhRK

        self.WhPa = piece("white pawn", 'a', 2)
        self.board[self.WhPa.pos[0]][self.WhPa.pos[1]] = self.WhPa
        self.WhPb = piece("white pawn", 'b', 2)
        self.board[self.WhPb.pos[0]][self.WhPb.pos[1]] = self.WhPb
        self.WhPc = piece("white pawn", 'c', 2)
        self.board[self.WhPc.pos[0]][self.WhPc.pos[1]] = self.WhPc
        self.WhPd = piece("white pawn", 'd', 2)
        self.board[self.WhPd.pos[0]][self.WhPd.pos[1]] = self.WhPd
        self.WhPe = piece("white pawn", 'e', 2)
        self.board[self.WhPe.pos[0]][self.WhPe.pos[1]] = self.WhPe
        self.WhPf = piece("white pawn", 'f', 2)
        self.board[self.WhPf.pos[0]][self.WhPf.pos[1]] = self.WhPf
        self.WhPg = piece("white pawn", 'g', 2)
        self.board[self.WhPg.pos[0]][self.WhPg.pos[1]] = self.WhPg
        self.WhPh = piece("white pawn", 'h', 2)
        self.board[self.WhPh.pos[0]][self.WhPh.pos[1]] = self.WhPh

        self.BlPa = piece("black pawn", 'a', 7)
        self.board[self.BlPa.pos[0]][self.BlPa.pos[1]] = self.BlPa
        self.BlPb = piece("black pawn", 'b', 7)
        self.board[self.BlPb.pos[0]][self.BlPb.pos[1]] = self.BlPb
        self.BlPc = piece("black pawn", 'c', 7)
        self.board[self.BlPc.pos[0]][self.BlPc.pos[1]] = self.BlPc
        self.BlPd = piece("black pawn", 'd', 7)
        self.board[self.BlPd.pos[0]][self.BlPd.pos[1]] = self.BlPd
        self.BlPe = piece("black pawn", 'e', 7)
        self.board[self.BlPe.pos[0]][self.BlPe.pos[1]] = self.BlPe
        self.BlPf = piece("black pawn", 'f', 7)
        self.board[self.BlPf.pos[0]][self.BlPf.pos[1]] = self.BlPf
        self.BlPg = piece("black pawn", 'g', 7)
        self.board[self.BlPg.pos[0]][self.BlPg.pos[1]] = self.BlPg
        self.BlPh = piece("black pawn", 'h', 7)
        self.board[self.BlPh.pos[0]][self.BlPh.pos[1]] = self.BlPh

        self.BlRQ = piece("black rook", 'a', 8)
        self.board[self.BlRQ.pos[0]][self.BlRQ.pos[1]] = self.BlRQ
        self.BlKnQ = piece("black knight", 'b', 8)
        self.board[self.BlKnQ.pos[0]][self.BlKnQ.pos[1]] = self.BlKnQ
        self.BlBQ = piece("black bishop", 'c', 8)
        self.board[self.BlBQ.pos[0]][self.BlBQ.pos[1]] = self.BlBQ
        self.BlQ = piece("black queen", 'd', 8)
        self.board[self.BlQ.pos[0]][self.BlQ.pos[1]] = self.BlQ
        self.BlK = piece("black king", 'e', 8)
        self.board[self.BlK.pos[0]][self.BlK.pos[1]] = self.BlK
        self.BlBK = piece("black bishop", 'f', 8)
        self.board[self.BlBK.pos[0]][self.BlBK.pos[1]] = self.BlBK
        self.BlKnK = piece("black knight", 'g', 8)
        self.board[self.BlKnK.pos[0]][self.BlKnK.pos[1]] = self.BlKnK
        self.BlRK = piece("black rook", 'h', 8)
        self.board[self.BlRK.pos[0]][self.BlRK.pos[1]] = self.BlRK

    # takes current piece in consideration and returns itself if it is checking the opponent king
    def checks(self, handle):
        if handle.identity[0] == "b":
            checked = True
            # if the piece is a black rook, confirm whether it is checking the white king
            if handle.identity[6:] == "rook":
                if handle.pos[0] == self.WhK.pos[0]:
                    # check from top to bottom
                    if handle.pos[1] > self.WhK.pos[1]:
                        for k in range(self.WhK.pos[1] + 1, handle.pos[1]):
                            if self.board[handle.pos[0]][k] is not None:
                                checked = False
                                break
                    # check from bottom to top
                    else:
                        for k in range(handle.pos[1] + 1, self.WhK.pos[1]):
                            if self.board[handle.pos[0]][k] is not None:
                                checked = False
                                break
                elif handle.pos[1] == self.WhK.pos[1]:
                    # check from right to left
                    if ord(handle.pos[0]) > ord(self.WhK.pos[0]):
                        for k in range(ord(self.WhK.pos[0]) + 1, ord(handle.pos[0])):
                            if self.board[chr(k)][handle.pos[1]] is not None:
                                checked = False
                                break
                    # check from left to right
                    else:
                        for k in range(ord(handle.pos[0]) + 1, ord(self.WhK.pos[0])):
                            if self.board[chr(k)][handle.pos[1]] is not None:
                                checked = False
                                break
                else:
                    checked = False

            # if the piece is a black bishop, confirm whether it is checking the white king
            elif handle.identity[6:] == "bishop":
                if abs(ord(handle.pos[0]) - ord(self.WhK.pos[0])) == abs(handle.pos[1] - self.WhK.pos[1]):
                    signX = (ord(handle.pos[0]) - ord(self.WhK.pos[0])) / abs(ord(handle.pos[0]) - ord(self.WhK.pos[0]))
                    signY = (handle.pos[1] - self.WhK.pos[1]) / abs(handle.pos[1] - self.WhK.pos[1])
                    for k in range(1, abs(handle.pos[1] - self.WhK.pos[1])):
                        if self.board[chr((int(ord(self.WhK.pos[0]) + k * signX)))][self.WhK.pos[1] + k * signY] is not None:
                            checked = False
                            break
                else:
                    checked = False

            # if the piece is a black queen, confirm whether it is checking the white king
            elif handle.identity[6:] == "queen":
                if handle.pos[0] == self.WhK.pos[0]:
                    if handle.pos[1] > self.WhK.pos[1]:
                        for k in range(self.WhK.pos[1] + 1, handle.pos[1]):
                            if self.board[handle.pos[0]][k] is not None:
                                checked = False
                                break
                    else:
                        for k in range(handle.pos[1] + 1, self.WhK.pos[1]):
                            if self.board[handle.pos[0]][k] is not None:
                                checked = False
                                break
                elif handle.pos[1] == self.WhK.pos[1]:
                    if ord(handle.pos[0]) > ord(self.WhK.pos[0]):
                        for k in range(ord(self.WhK.pos[0]) + 1, ord(handle.pos[0])):
                            if self.board[chr(k)][handle.pos[1]] is not None:
                                checked = False
                                break
                    else:
                        for k in range(ord(handle.pos[0]) + 1, ord(self.WhK.pos[0])):
                            if self.board[chr(k)][handle.pos[1]] is not None:
                                checked = False
                                break
                elif abs(ord(handle.pos[0]) - ord(self.WhK.pos[0])) == abs(
                        handle.pos[1] - self.WhK.pos[1]):
                    signX = (ord(handle.pos[0]) - ord(self.WhK.pos[0])) / abs(
                        ord(handle.pos[0]) - ord(self.WhK.pos[0]))
                    signY = (handle.pos[1] - self.WhK.pos[1]) / abs(handle.pos[1] - self.WhK.pos[1])
                    for k in range(1, abs(handle.pos[1] - self.WhK.pos[1])):
                        if self.board[chr((int(ord(self.WhK.pos[0]) + k * signX)))][self.WhK.pos[1] + k * signY] is not None:
                            checked = False
                            break
                else:
                    checked = False

            # if the piece is a black knight, confirm whether it is checking the white king
            elif handle.identity[6:] == "knight":
                if (abs(ord(handle.pos[0]) - ord(self.WhK.pos[0])) == 2
                    and abs(handle.pos[1] - self.WhK.pos[1]) == 1) \
                        or (abs(ord(handle.pos[0]) - ord(self.WhK.pos[0])) == 1
                            and abs(handle.pos[1] - self.WhK.pos[1]) == 2):
                    pass
                else:
                    checked = False

            # if the piece is a black pawn, confirm whether it is checking the white king
            elif handle.identity[6:] == "pawn":
                if ((ord(handle.pos[0]) - ord(self.WhK.pos[0])) == 1
                    or (ord(handle.pos[0]) - ord(self.WhK.pos[0])) == -1) \
                        and handle.pos[1] - self.WhK.pos[1] == 1:
                    pass
                else:
                    checked = False

            # if black piece is the king (hypothetical)
            else:
                if ((ord(handle.pos[0]) - ord(self.WhK.pos[0])), (handle.pos[1] - self.WhK.pos[1])) in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                    pass
                else:
                    checked = False

            if checked:
                return handle
            else:
                return None

        elif handle.identity[0] == "w":
            checked = True
            # if the piece is a white rook, confirm whether it is checking the black king
            if handle.identity[6:] == "rook":
                if handle.pos[0] == self.BlK.pos[0]:
                    # check from top to bottom
                    if handle.pos[1] > self.BlK.pos[1]:
                        for k in range(self.BlK.pos[1] + 1, handle.pos[1]):
                            if self.board[handle.pos[0]][k] is not None:
                                checked = False
                                break
                    # check from bottom to top
                    else:
                        for k in range(handle.pos[1] + 1, self.BlK.pos[1]):
                            if self.board[handle.pos[0]][k] is not None:
                                checked = False
                                break
                elif handle.pos[1] == self.BlK.pos[1]:
                    # check from right to left
                    if ord(handle.pos[0]) > ord(self.BlK.pos[0]):
                        for k in range(ord(self.BlK.pos[0]) + 1, ord(handle.pos[0])):
                            if self.board[chr(k)][handle.pos[1]] is not None:
                                checked = False
                                break
                    # check from left to right
                    else:
                        for k in range(ord(handle.pos[0]) + 1, ord(self.BlK.pos[0])):
                            if self.board[chr(k)][handle.pos[1]] is not None:
                                checked = False
                                break
                else:
                    checked = False

            # if the piece is a white bishop, confirm whether it is checking the black king
            elif handle.identity[6:] == "bishop":
                if abs(ord(handle.pos[0]) - ord(self.BlK.pos[0])) == abs(handle.pos[1] - self.BlK.pos[1]):
                    signX = (ord(handle.pos[0]) - ord(self.BlK.pos[0])) / abs(ord(handle.pos[0]) - ord(self.BlK.pos[0]))
                    signY = (handle.pos[1] - self.BlK.pos[1]) / abs(handle.pos[1] - self.BlK.pos[1])
                    for k in range(1, abs(handle.pos[1] - self.BlK.pos[1])):
                        if self.board[chr((int(ord(self.BlK.pos[0]) + k * signX)))][self.BlK.pos[1] + k * signY] is not None:
                            checked = False
                            break
                else:
                    checked = False

            # if the piece is a white queen, confirm whether it is checking the black king
            elif handle.identity[6:] == "queen":
                if handle.pos[0] == self.BlK.pos[0]:
                    if handle.pos[1] > self.BlK.pos[1]:
                        for k in range(self.BlK.pos[1] + 1, handle.pos[1]):
                            if self.board[handle.pos[0]][k] is not None:
                                checked = False
                                break
                    else:
                        for k in range(handle.pos[1] + 1, self.BlK.pos[1]):
                            if self.board[handle.pos[0]][k] is not None:
                                checked = False
                                break
                elif handle.pos[1] == self.BlK.pos[1]:
                    if ord(handle.pos[0]) > ord(self.BlK.pos[0]):
                        for k in range(ord(self.BlK.pos[0]) + 1, ord(handle.pos[0])):
                            if self.board[chr(k)][handle.pos[1]] is not None:
                                checked = False
                                break
                    else:
                        for k in range(ord(handle.pos[0]) + 1, ord(self.BlK.pos[0])):
                            if self.board[chr(k)][handle.pos[1]] is not None:
                                checked = False
                                break
                elif abs(ord(handle.pos[0]) - ord(self.BlK.pos[0])) == abs(
                        handle.pos[1] - self.BlK.pos[1]):
                    signX = (ord(handle.pos[0]) - ord(self.BlK.pos[0])) / abs(
                        ord(handle.pos[0]) - ord(self.BlK.pos[0]))
                    signY = (handle.pos[1] - self.BlK.pos[1]) / abs(handle.pos[1] - self.BlK.pos[1])
                    for k in range(1, abs(handle.pos[1] - self.BlK.pos[1])):
                        if self.board[chr((int(ord(self.BlK.pos[0]) + k * signX)))][self.BlK.pos[1] + k * signY] is not None:
                            checked = False
                            break
                else:
                    checked = False

            # if the piece is a white knight, confirm whether it is checking the black king
            elif handle.identity[6:] == "knight":
                if (abs(ord(handle.pos[0]) - ord(self.BlK.pos[0])) == 2
                    and abs(handle.pos[1] - self.BlK.pos[1]) == 1) \
                        or (abs(ord(handle.pos[0]) - ord(self.BlK.pos[0])) == 1
                            and abs(handle.pos[1] - self.BlK.pos[1]) == 2):
                    pass
                else:
                    checked = False

            # if the piece is a white pawn, confirm whether it is checking the black king
            elif handle.identity[6:] == "pawn":
                if ((ord(handle.pos[0]) - ord(self.BlK.pos[0])) == 1
                    or (ord(handle.pos[0]) - ord(self.BlK.pos[0])) == -1) \
                        and handle.pos[1] - self.BlK.pos[1] == -1:
                    pass
                else:
                    checked = False

            # if white piece is the king (hypothetical)
            else:
                if ((ord(handle.pos[0]) - ord(self.BlK.pos[0])), (handle.pos[1] - self.BlK.pos[1])) in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                    pass
                else:
                    checked = False

            if checked:
                return handle
            else:
                return None

    def newX(self, xPos, steps):
        return chr(int(ord(xPos) + steps))

    def addMoves(self):
        # regardless of legality, check for all available moves for white's turn
        if self.whiteTurn:
            for i in self.board:
                for j in self.board[i]:
                    if self.board[i][j] is not None:
                        handle = self.board[i][j]
                        if handle.identity[0] == "w":
                            if handle.identity[6:] == "rook":
                                handle.availableMoves = []
                                # horizontal+
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1]] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1]))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1]].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1]))
                                            break
                                    except Exception as e:
                                        break

                                #horizontal-
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1]] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1]))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1]].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1]))
                                            break
                                    except Exception as e:
                                        break

                                #vertical+
                                counter = 1
                                while True:
                                    try:
                                        if self.board[handle.pos[0]][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[handle.pos[0]][handle.pos[1] + counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                #vertical-
                                counter = 1
                                while True:
                                    try:
                                        if self.board[handle.pos[0]][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[handle.pos[0]][handle.pos[1] - counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                            elif handle.identity[6:] == "bishop":
                                handle.availableMoves = []
                                # diagonal I
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] + counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal II
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] + counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal III
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] - counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal IV
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] - counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                            elif handle.identity[6:] == "queen":
                                handle.availableMoves = []

                                # horizontal+
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1]] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1]))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1]].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1]))
                                            break
                                    except Exception as e:
                                        break

                                #horizontal-
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1]] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1]))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1]].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1]))
                                            break
                                    except Exception as e:
                                        break

                                #vertical+
                                counter = 1
                                while True:
                                    try:
                                        if self.board[handle.pos[0]][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[handle.pos[0]][handle.pos[1] + counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                #vertical-
                                counter = 1
                                while True:
                                    try:
                                        if self.board[handle.pos[0]][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[handle.pos[0]][handle.pos[1] - counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal I
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] + counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal II
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] + counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal III
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] - counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal IV
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] - counter].identity[0] == "w":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                            elif handle.identity[6:] == "knight":
                                handle.availableMoves = []
                                for k in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
                                    try:
                                        if self.board[chr(int(ord(handle.pos[0]) + k[0]))][handle.pos[1] + k[1]] is not None:
                                            if self.board[chr(int(ord(handle.pos[0])+k[0]))][handle.pos[1]+k[1]].identity[0] == "w":
                                                pass
                                            else:
                                                handle.availableMoves.append((chr(int(ord(handle.pos[0]) + k[0])), handle.pos[1] + k[1]))
                                        else:
                                            handle.availableMoves.append((chr(int(ord(handle.pos[0]) + k[0])), handle.pos[1] + k[1]))
                                    except:
                                        pass

                            elif handle.identity[6:] == "king":
                                handle.availableMoves = []
                                # normal moves
                                for k in [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]:
                                    try:
                                        if self.board[chr(int(ord(handle.pos[0]) + k[0]))][handle.pos[1] + k[1]] is not None:
                                            if self.board[chr(int(ord(handle.pos[0]) + k[0]))][handle.pos[1] + k[1]].identity[0] == "w":
                                                pass
                                            else:
                                                handle.availableMoves.append((chr(int(ord(handle.pos[0]) + k[0])), handle.pos[1] + k[1]))
                                        else:
                                            handle.availableMoves.append((chr(int(ord(handle.pos[0]) + k[0])), handle.pos[1] + k[1]))
                                    except Exception as e:
                                        pass

                                if self.WhRK not in self.discard:
                                    if self.WhK.prevPos[0] is None and self.WhRK.prevPos[0] is None:
                                        temp = True
                                        for k in [('f', 1), ('g', 1)]:
                                            if self.board[k[0]][k[1]] is not None:
                                                temp = False
                                        if temp:
                                            self.WhK.availableMoves.append("CK")
                                if self.WhRQ not in self.discard:
                                    # queen side castle
                                    if self.WhK.prevPos[0] is None and self.WhRQ.prevPos[0] is None:
                                        temp = True
                                        for k in [('b', 1), ('c', 1), ('d', 1)]:
                                            if self.board[k[0]][k[1]] is not None:
                                                temp = False
                                        if temp:
                                            self.WhK.availableMoves.append("CQ")

                            elif handle.identity[6:] == "pawn":
                                handle.availableMoves = []

                                # en passant
                                if handle.pos[1] == 5:
                                    try:
                                        if self.board[self.newX(handle.pos[0], 1)][handle.pos[1]] is not None:
                                            if self.board[self.newX(handle.pos[0], 1)][handle.pos[1]].identity == "black pawn":
                                                if self.board[self.newX(handle.pos[0], 1)][handle.pos[1]].prevPos[0] == (self.newX(handle.pos[0], 1), handle.pos[1] + 2):
                                                    if self.board[self.newX(handle.pos[0], 1)][handle.pos[1]].prevPos[1] == self.numMoves:
                                                        handle.availableMoves.append("EPI")
                                    except:
                                        pass

                                    try:
                                        if self.board[self.newX(handle.pos[0], -1)][handle.pos[1]] is not None:
                                            if self.board[self.newX(handle.pos[0], -1)][handle.pos[1]].identity == "black pawn":
                                                if self.board[self.newX(handle.pos[0], -1)][handle.pos[1]].prevPos[0] == (self.newX(handle.pos[0], -1), handle.pos[1] + 2):
                                                    if self.board[self.newX(handle.pos[0], -1)][handle.pos[1]].prevPos[1] == self.numMoves:
                                                        handle.availableMoves.append("EPII")
                                    except:
                                        pass
                                if handle.pos[1] < 7:
                                    # normal move
                                    if self.board[handle.pos[0]][handle.pos[1] + 1] is None:
                                        handle.availableMoves.append((handle.pos[0], handle.pos[1] + 1))
                                        if self.board[handle.pos[0]][handle.pos[1] + 2] is None and handle.prevPos[0] is None:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] + 2))
                                    # take
                                    try:
                                        if self.board[self.newX(handle.pos[0], 1)][handle.pos[1] + 1] is not None:
                                            if self.board[self.newX(handle.pos[0], 1)][handle.pos[1] + 1].identity[0] == "b":
                                                handle.availableMoves.append((self.newX(handle.pos[0], 1), handle.pos[1] + 1))
                                    except:
                                        pass

                                    try:
                                        if self.board[self.newX(handle.pos[0], -1)][handle.pos[1] + 1] is not None:
                                            if self.board[self.newX(handle.pos[0], -1)][handle.pos[1] + 1].identity[0] == "b":
                                                handle.availableMoves.append((self.newX(handle.pos[0], -1), handle.pos[1] + 1))
                                    except:
                                        pass
                                else:
                                    # pawn promotion
                                    if self.board[handle.pos[0]][handle.pos[1] + 1] is None:
                                        handle.availableMoves.append("PPr0")

                                    # take
                                    try:
                                        if self.board[self.newX(handle.pos[0], 1)][handle.pos[1] + 1] is not None:
                                            if self.board[self.newX(handle.pos[0], 1)][handle.pos[1] + 1].identity[0] == "b":
                                                handle.availableMoves.append("PPrI")
                                    except:
                                        pass

                                    try:
                                        if self.board[self.newX(handle.pos[0], -1)][handle.pos[1] + 1] is not None:
                                            if self.board[self.newX(handle.pos[0], -1)][handle.pos[1] + 1].identity[0] == "b":
                                                handle.availableMoves.append("PPrII")
                                    except:
                                        pass

                            else:
                                pass

        # regardless of legality, check for all available moves for black's turn
        else:
            for i in self.board:
                for j in self.board[i]:
                    if self.board[i][j] is not None:
                        handle = self.board[i][j]
                        if handle.identity[0] == "b":
                            if handle.identity[6:] == "rook":
                                handle.availableMoves = []
                                # horizontal+
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1]] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1]))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1]].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1]))
                                            break
                                    except Exception as e:
                                        break

                                # horizontal-
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1]] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1]))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1]].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1]))
                                            break
                                    except Exception as e:
                                        break

                                # vertical+
                                counter = 1
                                while True:
                                    try:
                                        if self.board[handle.pos[0]][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[handle.pos[0]][handle.pos[1] + counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                # vertical-
                                counter = 1
                                while True:
                                    try:
                                        if self.board[handle.pos[0]][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[handle.pos[0]][handle.pos[1] - counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                            elif handle.identity[6:] == "bishop":
                                handle.availableMoves = []
                                # diagonal I
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] + counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal II
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] + counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal III
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] - counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal IV
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] - counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                            elif handle.identity[6:] == "queen":
                                handle.availableMoves = []

                                # horizontal+
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1]] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1]))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1]].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1]))
                                            break
                                    except Exception as e:
                                        break

                                # horizontal-
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1]] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1]))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1]].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1]))
                                            break
                                    except Exception as e:
                                        break

                                # vertical+
                                counter = 1
                                while True:
                                    try:
                                        if self.board[handle.pos[0]][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[handle.pos[0]][handle.pos[1] + counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                # vertical-
                                counter = 1
                                while True:
                                    try:
                                        if self.board[handle.pos[0]][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[handle.pos[0]][handle.pos[1] - counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal I
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] + counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal II
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] + counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] + counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] + counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] + counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal III
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) - counter)][handle.pos[1] - counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) - counter), handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                                # diagonal IV
                                counter = 1
                                while True:
                                    try:
                                        if self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] - counter] is None:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] - counter))
                                            counter += 1
                                        elif self.board[chr(ord(handle.pos[0]) + counter)][handle.pos[1] - counter].identity[0] == "b":
                                            break
                                        else:
                                            handle.availableMoves.append((chr(ord(handle.pos[0]) + counter), handle.pos[1] - counter))
                                            break
                                    except Exception as e:
                                        break

                            elif handle.identity[6:] == "knight":
                                handle.availableMoves = []
                                for k in [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]:
                                    try:
                                        if self.board[chr(int(ord(handle.pos[0]) + k[0]))][handle.pos[1] + k[1]] is not None:
                                            if self.board[chr(int(ord(handle.pos[0]) + k[0]))][handle.pos[1] + k[1]].identity[0] == "b":
                                                pass
                                            else:
                                                handle.availableMoves.append((chr(int(ord(handle.pos[0]) + k[0])), handle.pos[1] + k[1]))
                                        else:
                                            handle.availableMoves.append((chr(int(ord(handle.pos[0]) + k[0])), handle.pos[1] + k[1]))
                                    except:
                                        pass

                            elif handle.identity[6:] == "king":
                                handle.availableMoves = []
                                # normal moves
                                for k in [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                                    try:
                                        if self.board[chr(int(ord(handle.pos[0]) + k[0]))][handle.pos[1] + k[1]] is not None:
                                            if self.board[chr(int(ord(handle.pos[0]) + k[0]))][handle.pos[1] + k[1]].identity[0] == "b":
                                                pass
                                            else:
                                                handle.availableMoves.append((chr(int(ord(handle.pos[0]) + k[0])), handle.pos[1] + k[1]))
                                        else:
                                            handle.availableMoves.append((chr(int(ord(handle.pos[0]) + k[0])), handle.pos[1] + k[1]))
                                    except Exception as e:
                                        pass

                                # king side castle
                                if self.BlRK not in self.discard:
                                    if self.BlK.prevPos[0] is None and self.BlRK.prevPos[0] is None:
                                        temp = True
                                        for k in [('f', 8), ('g', 8)]:
                                            if self.board[k[0]][k[1]] is not None:
                                                temp = False
                                        if temp:
                                            self.BlK.availableMoves.append("CK")

                                # queen side castle
                                if self.BlRQ not in self.discard:
                                    if self.BlK.prevPos[0] is None and self.BlRQ.prevPos[0] is None:
                                        temp = True
                                        for k in [('b', 8), ('c', 8), ('d', 8)]:
                                            if self.board[k[0]][k[1]] is not None:
                                                temp = False
                                        if temp:
                                            self.BlK.availableMoves.append("CQ")

                            elif handle.identity[6:] == "pawn":
                                handle.availableMoves = []

                                # en passant
                                if handle.pos[1] == 4:
                                    try:
                                        if self.board[self.newX(handle.pos[0], 1)][handle.pos[1]] is not None:
                                            if self.board[self.newX(handle.pos[0], 1)][handle.pos[1]].identity == "white pawn":
                                                if self.board[self.newX(handle.pos[0], 1)][handle.pos[1]].prevPos[0] == (self.newX(handle.pos[0], 1), handle.pos[1] - 2):
                                                    if self.board[self.newX(handle.pos[0], 1)][handle.pos[1]].prevPos[1] == self.numMoves:
                                                        handle.availableMoves.append("EPIV")
                                    except:
                                        pass

                                    try:
                                        if self.board[self.newX(handle.pos[0], -1)][handle.pos[1]] is not None:
                                            if self.board[self.newX(handle.pos[0], -1)][handle.pos[1]].identity == "white pawn":
                                                if self.board[self.newX(handle.pos[0], -1)][handle.pos[1]].prevPos[0] == (self.newX(handle.pos[0], -1), handle.pos[1] - 2):
                                                    if self.board[self.newX(handle.pos[0], -1)][handle.pos[1]].prevPos[1] == self.numMoves:
                                                        handle.availableMoves.append("EPIII")
                                    except Exception as e:
                                        pass

                                if handle.pos[1] > 2:
                                    # normal move
                                    if self.board[handle.pos[0]][handle.pos[1] - 1] is None:
                                        handle.availableMoves.append((handle.pos[0], handle.pos[1] - 1))
                                        if self.board[handle.pos[0]][handle.pos[1] - 2] is None and handle.prevPos[0] is None:
                                            handle.availableMoves.append((handle.pos[0], handle.pos[1] - 2))
                                    # take
                                    try:
                                        if self.board[self.newX(handle.pos[0], 1)][handle.pos[1] - 1] is not None:
                                            if self.board[self.newX(handle.pos[0], 1)][handle.pos[1] - 1].identity[0] == "w":
                                                handle.availableMoves.append((self.newX(handle.pos[0], 1), handle.pos[1] - 1))
                                    except:
                                        pass

                                    try:
                                        if self.board[self.newX(handle.pos[0], -1)][handle.pos[1] - 1] is not None:
                                            if self.board[self.newX(handle.pos[0], -1)][handle.pos[1] - 1].identity[0] == "w":
                                                handle.availableMoves.append((self.newX(handle.pos[0], -1), handle.pos[1] - 1))
                                    except Exception as e:
                                        pass
                                else:
                                    # pawn promotion
                                    if self.board[handle.pos[0]][handle.pos[1] - 1] is None:
                                        handle.availableMoves.append("PPr0")

                                    # take
                                    try:
                                        if self.board[self.newX(handle.pos[0], 1)][handle.pos[1] - 1] is not None:
                                            if self.board[self.newX(handle.pos[0], 1)][handle.pos[1] - 1].identity[0] == "w":
                                                handle.availableMoves.append("PPrIV")
                                    except:
                                        pass

                                    try:
                                        if self.board[self.newX(handle.pos[0], -1)][handle.pos[1] - 1] is not None:
                                            if self.board[self.newX(handle.pos[0], -1)][handle.pos[1] - 1].identity[0] == "w":
                                                handle.availableMoves.append("PPrIII")
                                    except:
                                        pass

                            else:
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

