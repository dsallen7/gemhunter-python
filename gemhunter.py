import pygame
from pygame import *
import os, sys
from pygame.locals import *
import random
from types import *

clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 500))

RED = (255,0,0)
GREEN = (0,192,0)
YELLOW = (0,0,255)

BLACK = (0,0,0)

COLORS = ['r','g','b']

#NSWE
CARDINALS = [ (0,-1), (0,1), (-1,0), (1,0) ]

DIM = 20

class Board():
    
    def __init__(self):
        #20x20 board
        #20x20 pieces
        self.grid = []
        for i in range(DIM):
            row = []
            for j in range(DIM):
                row += [ COLORS[ random.randrange(3) ] ]
            self.grid += [ row ]
        
        self.board = pygame.Surface( (400,400) )
        self.highmark = DIM
        self.visited = []
    
    def getGridEntry(self,y,x):
        if ( x in range(DIM) and y in range(DIM) ):
            return self.grid[x][y]
        else:
            return 'x'
    
    def setGridEntry(self,y,x,e):
        if ( x in range(DIM) and y in range(DIM) ):
            self.grid[x] = self.grid[x][:y] + [e] + self.grid[x][y+1:]
        else:
            print 'out of bounds'
    
    def redraw(self):
        self.board.fill( BLACK )
        for i in range(DIM):
            for j in range(DIM):
                entry = self.getGridEntry(i,j)
                if entry == 'r':
                    pygame.draw.circle(self.board, RED, ( i*20 + 10, j*20 + 10 ), 10, 0 )
                if entry == 'g':
                    pygame.draw.circle(self.board, GREEN, ( i*20 + 10, j*20 + 10 ), 10, 0 )
                if entry == 'b':
                    pygame.draw.circle(self.board, YELLOW, ( i*20 + 10, j*20 + 10 ), 10, 0 )
        screen.blit(self.board, (0,0) )
    
    def flatten(self, x):
        result = []
        for el in x:
            if hasattr(el, "__iter__") and not isinstance(el, basestring) and type(el) is not TupleType and type(el) is not NoneType:
                result.extend(self.flatten(el))
            elif type(el) is TupleType:
                result.append(el)
        return result
    
    def searchBoardBFS(self,pieceLocation):
        if (pieceLocation == None):
            return
        (x,y) = pieceLocation
        piecesList = []
        for (Cx,Cy) in CARDINALS:
            if (self.getGridEntry(x,y) == self.getGridEntry(x+Cx,y+Cy) and (x+Cx,y+Cy) not in self.visited ):
                piecesList += [ (x+Cx,y+Cy) ]
                self.visited += [ (x+Cx,y+Cy) ]
            else:
                piecesList += [ None ]
        if ( piecesList == [None,None,None,None] ):
            return (x,y)
        else:
            return [ (x,y) ] + [self.searchBoardBFS(piecesList[0])] + [self.searchBoardBFS(piecesList[1])] + [self.searchBoardBFS(piecesList[2])] + [self.searchBoardBFS(piecesList[3])]
    
    def getCurrentMove(self,x,y):
        if ( self.getGridEntry(x,y) == 'o' ):
            return []
        self.visited = []
        move = self.searchBoardBFS( (x,y) )
        move = self.flatten(move)
        return list( set(move) )
    
    def deleteCol(self,x):
        for i in range(DIM):
            self.grid[i] = self.grid[i][:x] + self.grid[i][x+1:] + ['o']
        self.highmark -= 1
    
    def getCol(self,x):
        col = ''
        for j in range(DIM):
            col += self.getGridEntry(x,j)
        return col
        
    def printGrid(self):
        for i in range(DIM):
            print self.getCol(i)
    
    def updateGrid(self):
        #cascading downward of pieces
        for i in range(DIM):
            col = self.getCol(i)
            z = 0
            while col == 'o'*DIM and i < self.highmark:
                #collapsing
                self.deleteCol(i)
                col = self.getCol(i)
            if 'o' in col:
                for idx in range( len(col) ):
                    if col[idx] == 'o':
                        col = 'o' + col[:idx] + col[idx+1:]
                for idx in range( len(col) ):
                    self.setGridEntry(i, idx, col[idx] )

class Game():
    
    def __init__(self):
        self.currentMove = []
        self.currentPoints = 0
        self.score = 0
        self.X = 0
        self.Y = 0
        self.piecesLeft = DIM*DIM
    
    def makeMove(self):
        self.piecesLeft -= len(self.currentMove)
        self.score += self.currentPoints
        for (x,y) in self.currentMove:
            myBoard.setGridEntry(x,y,'o')
        
        myBoard.updateGrid()
    
    def EventHandler(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.makeMove()
    
    def displayText(self):
        textbox = pygame.Surface( (500,100) )
        textline = range(4)
        text1 = 'Current move: ' + str( len(self.currentMove) )
        text2 = 'Color: ' + myBoard.getGridEntry(self.X,self.Y)
        text3 = 'Pieces left: ' + str(self.piecesLeft)
        text4 = 'Current points: ' + str(self.currentPoints)
        text5 = 'Score: ' + str(self.score)
        if pygame.font:
            font = pygame.font.Font(None, 36)
            text = font.render(text1, 1, (255, 255, 255))
            textbox.blit(text, (0,0) )
            text = font.render(text2, 1, (255, 255, 255))
            textbox.blit(text, (200,0) )
            text = font.render(text3, 1, (255, 255, 255))
            textbox.blit(text, (0,50) )
            text = font.render(text4, 1, (255, 255, 255))
            textbox.blit(text, (200,50) )
            text = font.render(text5, 1, (255, 255, 255))
            textbox.blit(text, (300,0) )
        textpos = (0,400)
        screen.blit(textbox, textpos)
        
    def updateMouse(self):
        pos = pygame.mouse.get_pos()
        
        (x,y) = pos
        
        self.X = x/20
        self.Y = y/20
        
        
        
        if ( x in range(DIM*20) and y in range(DIM*20) ):
            currentMove = myBoard.getCurrentMove(x/20,y/20)
            self.currentMove = currentMove
            moveBox = pygame.Surface( (20,20) )
            
            self.currentPoints = len(self.currentMove)**2
            
            moveBox.fill( (255,255,255) )
            for pos in currentMove:
                (x,y) = pos
                screen.blit(moveBox, (x*20,y*20) )
        else:
            self.currentPoints = 0

myGame = Game()

myBoard = Board()

def main():
    pygame.init()
    while True:
        clock.tick(60)
        for e in event.get():
            if e.type == pygame.QUIT: #if EXIT clicked
                os.sys.exit(0) #close cleanly
            else:
                myGame.EventHandler(e)
        myBoard.redraw()
        myGame.updateMouse()
        myGame.displayText()
        pygame.display.flip()
main()