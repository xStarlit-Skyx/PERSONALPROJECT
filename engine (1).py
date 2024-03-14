import pygame as p

class GameState():
    def __init__(self):
        self.board = [
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.whiteToMove = True
        self.moveLog = []

    def ap(self, piece, row, col):
        self.board[row-1][col-1] = piece
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

class Move():
    #transformed into chess notation
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"0":8}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}



def load_images():
    pieces = ["bp", "bN", "bB", "bR", "bQ", "bK", "wp", "wN", "wB", "wR", "wQ", "wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("assets/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    clock = p.time.Clock()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    gs = GameState()
    screen.fill(p.Color("White"))
    load_images()
    running = True
    sqSelected = ()
    playerClicks = []
    sqValid = {}
    LEVEL = "0.1"
    while running:
        # LEVEL DESIGNING
        if LEVEL == "0.1":
            gs.ap("wK", 8, 5)
            gs.ap("wQ", 8, 4)
            gs.ap("bK", 1, 5)
            LEVEL = "LOADED"
            print(gs.board)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row,col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #appends two click coords
                    if len(playerClicks) == 2: #and gs.board[row][col] != "--":
                        move = Move(playerClicks[0],playerClicks[1], gs.board)
                        gs.makeMove(move)
                        print(gs.board)
                        sqSelected = ()
                        playerClicks = []

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()





def draw_board(screen):
    WHITE = (255, 255, 255)
    GREEN = (118, 150, 86)
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = WHITE if (row + col) % 2 == 0 else GREEN
            p.draw.rect(screen, color, (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)
main()

