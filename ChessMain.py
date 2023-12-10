import pygame as p
import ChessEngine
import ChessAI

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
COLOR1 = p.Color("white")
COLOR2 = p.Color("grey")
colorPieceSelected = p.Color("blue")
colorPieceMove = p.Color("yellow")

def loadImages():
    pieces = ["wp", "bp", "bR", "bN", "bB", "bQ","bK", "wK", "wQ", "wB", "wN", "wR"]
    for piece in  pieces:
        IMAGES[piece] = p.transform.scale( p.image.load("images/" + piece + ".png"),(SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    p.display.set_caption("Chess")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False # flag animate if you should animate a move

    loadImages()
    running = True

    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True # if a human is playing white, then it wil be true. If an AI is playing, then it fasle
    playerTwo = False # same as about but for black
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else :
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:                      
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if event.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        
        #Ai move finder
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findBestMoveMinMax(gs, validMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()   
            moveMade = False 
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)  

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black win by checkmate")
            else:
                drawText(screen, "White win by checkmate")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "StaleMate")

        clock.tick(MAX_FPS)
        p.display.flip()

def highlightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"): #select a piece that can move
            #hightlight Square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(colorPieceSelected)
            screen.blit(s, (c * SQ_SIZE, r *SQ_SIZE))
            # highlight move from square
            s.fill(colorPieceMove)
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [COLOR1, COLOR2]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            p.draw.rect(screen , colors[(r + c) % 2], p.Rect(r * SQ_SIZE, c * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c *SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Animating a move
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #fram to move on square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + frame*dR/frameCount, move.startCol + frame * dC/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # earse the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw capture piece onto retangle
        if move.pieceCapture != "--":
            screen.blit(IMAGES[move.pieceCapture], endSquare)
        #draw piece move
        if move.pieceMoved != "--":
            screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE ))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color("red"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width() / 2, HEIGHT/2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation.move(2,2))

if __name__ == "__main__":
    main()
