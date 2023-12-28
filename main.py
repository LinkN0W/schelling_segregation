import pygame
import sys
import os
import random
pygame.init()

dis = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game of Life")

WINW, WINH = dis.get_size()

BOXW = 20
BOXH = 20

assert WINW % BOXW == 0 and WINH % BOXH == 0

BOARDW = WINW//BOXW
BOARDH = WINH//BOXH

white = (255, 255, 255)
black = (0, 0, 0)

white_num = 1
black_num = 2
empty_num = 0

lines_colour = (198, 195, 181)
empty_color = (0, 128, 0)

vector_empty = []               #(w, h)

f = 0.5
def make_new_board(w, h):
    board = []
    for i in range(h):
        row = []
        for j in range(w):
            value = random.randint(0, 2)
            row.append(value)
            if value == empty_num:
                vector_empty.append([i, j])
        board.append(row)

    return board



def check(board, x, y):
    m = 0
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not(i == j == 0) and (0 <= i+y < BOARDH) and (0 <= j+x < BOARDW):
                if board[i+y][j+x] == board[y][x]:
                    m += 1
                count +=1
    return m/count


def move(board, x, y):
    rand_num = random.randint(0, len(vector_empty)-1)
    empty_x = vector_empty[rand_num][1]
    empty_y = vector_empty[rand_num][0]
    if check(board, x, y) < check(board, empty_x, empty_y) and check(board, x, y) < f:
        board[empty_y][empty_x] = board[y][x]
        board[y][x] = empty_num
        vector_empty[rand_num] = [y, x]
    return board




def update_board(board):
    board_update = board
    for _ in range(0, len(vector_empty)):
        x = random.randint(0, BOARDW-1)
        y = random.randint(0, BOARDH-1)
        print(BOARDW-1," ", BOARDH-1)
        if board_update[y][x] == 0:
            continue
        board_update = move(board_update, x, y)
    return board_update



def draw_cells(win, board):
    for i in range(BOARDH):
        for j in range(BOARDW):
            if board[i][j] == white_num:
                pygame.draw.rect(win, white, (j*BOXW, i*BOXH, BOXW, BOXH))
            elif board[i][j] == black_num:
                pygame.draw.rect(win, black,
                                 (j*BOXW, i*BOXH, BOXW, BOXH))
            else:
                pygame.draw.rect(win, empty_color,
                                 (j * BOXW, i * BOXH, BOXW, BOXH))


def draw_lines(win):
    for i in range(BOARDH + 1):
        pygame.draw.line(win, lines_colour, (0, i * BOXW + 0.5), (BOXW * BOARDW, i * BOXW + 0.5))
    for i in range(BOARDW + 1):
        pygame.draw.line(win, lines_colour, (i * BOXH + 0.5, 0), (i * BOXH + 0.5, BOXH * BOARDH))


board = make_new_board(BOARDW, BOARDH)
updating = False
lines_enabled = True

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RIGHT:
                print("Right")
                board = update_board(board)

    draw_cells(dis, board)
    if lines_enabled:
        draw_lines(dis)
    pygame.display.update()
