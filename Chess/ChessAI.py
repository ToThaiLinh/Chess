import random

pieceScore = {"K" : 0, "Q" : 10, "R" : 5, "B" : 3, "N" : 3, "p" : 1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    turnMutiplier = 1 if gs.whiteToMove else -1
    opponentMiniMaxScore = CHECKMATE
    bestAIMove = None
    random.shuffle(validMoves)
    for playMove in validMoves:
        gs.makeMove(playMove)
        oppoinentMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for move in oppoinentMoves:
            gs.makeMove(move)
            if gs.checkMate:
                score = -turnMutiplier * CHECKMATE
            elif gs.staleMate:
                score = STALEMATE
            else :
                score = -turnMutiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMiniMaxScore:
            opponentMiniMaxScore = opponentMaxScore
            bestAIMove = playMove
        gs.undoMove()
    return bestAIMove


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]
    return score