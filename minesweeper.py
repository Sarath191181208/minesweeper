import pygame
import random


pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption('minesweeper')
FPS = 20

WHITE = (215, 215, 215)
GREAY = (70, 70, 70)
BLACK = (0, 0, 0)
BLUE = (10, 40, 100)
RED = (220, 40, 30)
checksClr = BLUE
boardClr = WHITE
txtClr = GREAY

translationFactor = 0


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


class Grid():
    def __init__(self, rows: int = 4, cols: int = 4, width: int = 400, height: int = 400, noOfMines=10):
        self.rows = cols
        self.cols = rows
        self.cubes = [
            [Cube(0, i, j, width, height, self.cols, self.rows)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.mineLocations = None
        self.width = width
        self.height = height
        self.noOfMines = noOfMines

    def create_board(self) -> None:
        self.mineLocations = {}
        minesPlaced = 0
        while(minesPlaced < self.noOfMines):
            x = random.randint(0, self.rows-1)
            y = random.randint(0, self.cols-1)
            if self.cubes[x][y].value == 0:
                self.mineLocations[str(x)+str(y)] = (x, y)
                self.cubes[x][y].value = -1
                minesPlaced += 1
        for pos in self.mineLocations:
            x, y = self.mineLocations[pos]
            for i in range(max(0, x-1), min(self.rows, x+2)):
                for j in range(max(0, y-1), min(self.cols, y+2)):
                    if x == i and y == j:
                        continue
                    if self.cubes[i][j].value != -1:
                        self.cubes[i][j].value += 1

    def __str__(self) -> str:
        string = ""
        for i in range(self.rows):
            for j in range(self.cols):
                string += str(self.cubes[i][j].value) + (" ")
            string += "\n"
        return string
# TODO : must add drawing logic

    def draw(self, win=None) -> None:
        if win == None:
            win = WIN

        win.fill(boardClr)
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)
        thick = 1
        # pygame.draw.line(win, (0, 0, 0), (i * rowGap, 0),i * rowGap, self.height), thick)
        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, i*rowGap),
                             (self.height, rowGap*i), thick)
        for i in range(self.cols+1):
            pygame.draw.line(win, BLACK, (i*colGap, 0), (colGap*i, self.width))
        pygame.display.update()
    # TODO mouse click

    def dig(self, x, y, depth=6):
        if depth == 0:
            return False
        if self.cubes[x][y].value == -1:
            # todo : colour the mine
            return False
        if self.cubes[x][y].value == 0:
            self.cubes[x][y].show = True
        if self.cubes[x][y].value > 0:
            self.cubes[x][y].show = True
            return True
        for i in range(max(0, x-1), min(self.rows, x+2)):
            for j in range(max(0, y-1), min(self.cols, y+2)):
                if self.dig(i, j, depth - 1):
                    self.cubes[i][j].show = True
                    break

    def clicked(self, pos):
        x, y = pos
        if x >= self.rows or y >= self.cols or x < 0:
            return -1
        self.cubes[x][y].show = True
        if self.cubes[x][y].value == -1:
            self.cubes[x][y].colour = RED
            return 0
        self.dig(x, y)
        self.draw()


class Cube():
    def __init__(self, value, row, col, width, height, cols, rows):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.centerFactor = 10
        self.show = False
        self.colour = checksClr

    def draw(self, win):
        # fnt = pygame.font.SysFont('comicsans', 40)
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        # todo drawing
        # if (self.col % 2) == (self.row % 2):
        #     pygame.draw.rect(win, checksClr, pygame.Rect(x, y, colGap, rowGap))
        if self.show:
            pygame.draw.rect(win, self.colour,
                             pygame.Rect(x, y, colGap, rowGap))
            if (self.value != 0) and self.value != -1:
                # newImg = pygame.transform.scale(queenImg, (int(colGap-self.centerFactor), int(rowGap-self.centerFactor)))
                # win.blit(newImg, (x+self.centerFactor/2, y+self.centerFactor/2))
                text = PYtxt(str(self.value))
                win.blit(text, (x + (colGap/2 - text.get_width()/2),
                                y + (rowGap/2 - text.get_height()/2)))
            elif self.value == -1:
                text = PYtxt("*")
                win.blit(text, (x + (colGap/2 - text.get_width()/2),
                                y + (rowGap/2 - text.get_height()/4)))

                # WIN.blit(PYtxt('Solved'), (20, 560) -> position)
                # pygame.display.update()
                # win.blit(text, (x + (colGap/2 - text.get_width()/2),
                #                 y + (rowGap/2 - text.get_height()/2)))


board = Grid(20, 20, WIN.get_width(), WIN.get_width(), 10)
board.create_board()
board.draw()

run = True
mousePause = False
while run:
    clock.tick(FPS)
    if pygame.mouse.get_pressed()[0] and not mousePause:
        x, y = pygame.mouse.get_pos()
        y //= board.width // board.cols
        x //= board.width // board.rows
        y -= translationFactor
        if board.clicked((y, x)) == 0:
            for i in board.mineLocations:
                (x, y) = board.mineLocations[i]
                board.cubes[x][y].show = True
            board.draw()
            mousePause = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()
