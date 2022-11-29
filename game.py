import pygame
import os
import time
import piece
from board import Board

board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")), (750, 750))
rect = (113,113,525,525)

pygame.font.init()
    
def redraw_gameWindow(win, bo, p1, p2):
    win.blit(board, (0, 0))
    bo.draw(win)

    formatTime1 = str(int(p1//60)) + ":" + str(int(p1%60))
    formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
    if p1%60 == 0:
        formatTime1 += "0"
    if p2%60 == 0:
        formatTime2 += "0"

    font = pygame.font.SysFont("comicsans", 30)
    txt = font.render("Player 2 Time: " + str(formatTime2), 1, (255, 255, 255))
    txt2 = font.render("Player 1 Time: " + str(formatTime1), 1, (255,255,255))
    win.blit(txt, (520,10))
    win.blit(txt2, (520, 700))

    pygame.display.update()


def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    txt = font.render(text,1, (255,0,0))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False


def click(pos):
    """
    :return: pos (x, y) in range 0-7 0-7
    """
    x = pos[0]
    y = pos[1]
    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]:
            divX = x - rect[0]
            divY = y - rect[1]
            i = int(divX / (rect[2]/8))
            j = int(divY / (rect[3]/8))
            return i, j

    return -1, -1

def main():
    p1Time = 900
    p2Time = 900

    turn = "w"
    count = 0
    bo = Board(8, 8)
    bo.update_moves()
    clock = pygame.time.Clock()
    run = True
    startTime = time.time()
    while run:
        clock.tick(15)
        
        if turn == "w":
            p1Time -= (time.time() - startTime)
            if p1Time <= 0:
                end_screen(win, "Black Wins")
        else:
            p2Time -=  (time.time() - startTime)
            if p2Time <= 0:
                end_screen(win, "White Wins")

        startTime = time.time()
        
        redraw_gameWindow(win, bo, int(p1Time), int(p2Time))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                bo.update_moves()
                i, j = click(pos)
                change = bo.select(i,j, turn)

                if change == True:
                    startTime = time.time()
                    count +=1
                    if turn == "w":
                        turn = "b"
                    else:
                        turn = "w"

width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
main()