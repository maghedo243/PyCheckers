class CPUPlayer:
    """
    The CPU move decision engine.
    """

    def __init__(self,board,color):
        self.board = board
        self.color = color
        self.moveValues = dict()

    def chooseMove(self):
        self.moveAppraise()

    def moveAppraise(self):
        self.moveValues.clear()
        moveDict = dict()
        for checker in [piece for row in self.board.checkerLocations for piece in row if (piece is not None and piece.color == self.color)]:
            checker.calculateMoves()
            moveDict.update(dict.fromkeys(checker.possibleMoves, checker))

        print(moveDict)
        for move, checker in moveDict.items():
            val = 0
            val += (move.moveSquare.getY()/350)
            val += 0.3 if move.moveType == "capture" else 0
            val += 0.1 if ((0.4 < (move.moveSquare.getY()/350) < 0.6) and (0.4 < (move.moveSquare.getY()/350) < 0.6)) else 0
            val += 0.15 if move.parentMove is not None else 0
            print(move, val)

