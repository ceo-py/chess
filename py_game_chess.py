import pygame
from pygame.locals import *
from main import *
import os

FPS = 60
pygame.init()
width = 800
height = 800
pygame.display.set_caption("Chess Test")
window = pygame.display.set_mode((width, height))
bg_img = pygame.image.load('background.jpg')
bg_img = pygame.transform.scale(bg_img, (width, height))
chess_board = create_chess_board()
moving = False
selected_target = False
BLUE = (0, 0, 255)
player = 1

for row in range(8):
    for col in range(8):
        if not isinstance(chess_board[row][col], str):
            chess_board[row][col].display = (
                pygame.transform.scale(pygame.image.load(os.path.join(chess_board[row][col].picture)),
                                       (100, 100)))


def draw_pawns():
    for row in range(8):
        for col in range(8):
            if not isinstance(chess_board[row][col], str):
                row_pos, col_pos = [x * 100 for x in chess_board[row][col].position]
                chess_board[row][col].mouse_pos = ((range(col_pos, col_pos + 100)), (range(row_pos, row_pos + 100)))
                window.blit(chess_board[row][col].display, (col_pos, row_pos))


def get_figure_pos_to_put(row, col):
    if col <= 100:
        col = 0
    else:
        if int(str(col)[1:]) >= 50:
            col = int(str(col)[0]) + 1
        else:
            col = int(str(col)[0])

    if row <= 100:
        row = 0
    else:
        if int(str(row)[1:]) >= 50:
            row = int(str(row)[0]) + 1
        else:
            row = int(str(row)[0])

    return row, col


running = True
while running:
    window.blit(bg_img, (0, 0))
    draw_pawns()
    pygame.time.Clock().tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                print("Left Mouse key was clicked")
                mouse_pos_test = pygame.mouse.get_pos()
                print(mouse_pos_test)
                for row in range(8):
                    for col in range(8):
                        if not isinstance(chess_board[row][col], str):
                            if mouse_pos_test[0] in chess_board[row][col].mouse_pos[0] and \
                                    mouse_pos_test[1] in chess_board[row][col].mouse_pos[1]:
                                if chess_board[row][col].color == "w" and player % 2 != 0 or \
                                        chess_board[row][col].color == "b" and player % 2 == 0:
                                    move_target, chess_board[row][col] = chess_board[row][col], "None"
                                    row_pos, col_pos = [(x * 100) + 50 for x in move_target.position]
                                    rect = move_target.display.get_rect(center=(col_pos, row_pos))
                                    move_target.check_right_move(chess_board)
                                    print(move_target.position)
                                    selected_target = True


        if event.type == MOUSEBUTTONDOWN and selected_target:
            if rect.collidepoint(event.pos):
                moving = True

        elif event.type == MOUSEBUTTONUP and selected_target:
            moving = False

        elif event.type == MOUSEMOTION and moving and selected_target:

            rect.move_ip(event.rel)

        if event.type == MOUSEBUTTONUP and selected_target:
            last_row, last_col = move_target.position
            col, row = get_figure_pos_to_put(rect[0], rect[1])

            print(move_target.position)
            print(move_target.available_moves)
            if [row, col] in move_target.available_moves:
                if "Pawn" in move_target.name:
                    move_target.first_move = False
                chess_board[row][col] = move_target
                move_target.position = (row, col)
                move_target.row, move_target.col = row, col
                player += 1
            else:
                chess_board[last_row][last_col] = move_target
                move_target.position = (last_row, last_col)
            selected_target = False
            move_target.available_moves = []

    if selected_target:
        window.blit(move_target.display, rect)
        pygame.draw.rect(window, BLUE, rect, 2)

    pygame.display.update()
pygame.quit()