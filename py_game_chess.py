import pygame
from pygame.locals import *
from main import *
import os

FPS = 60
pygame.init()
WIDTH = 800
HEIGHT = 800
pygame.display.set_caption("Chess Test")
window = pygame.display.set_mode((WIDTH, HEIGHT))
bg_img = pygame.transform.scale(pygame.image.load(f"{CURRENT_PATH}\pictures\\background.jpg"), (WIDTH, HEIGHT))
chess_board = create_chess_board()
moving, selected_target, running = False, False, True
BLUE = (0, 0, 255)
player = 1
SIZE_R = HEIGHT // 8
SIZE_C = WIDTH // 8


def make_new_queen_pic(row, col, player):
    color = {7: "b", 0: "w"}
    chess_board[row][col] = Queen(f"Queen - made", color[row], (row, col))
    chess_board[row][col].display = (
        pygame.transform.scale(pygame.image.load(os.path.join(chess_board[row][col].picture)),
                               (SIZE_C, SIZE_R)))
    return player + 1


def draw_pawns(scale=False):
    for row in range(CHESS_BOARD_SIZE):
        for col in range(CHESS_BOARD_SIZE):
            if not isinstance(chess_board[row][col], str):
                if scale:
                    chess_board[row][col].display = (
                        pygame.transform.scale(pygame.image.load(os.path.join(chess_board[row][col].picture)),
                                               (SIZE_C, SIZE_R)))
                else:
                    window.blit(chess_board[row][col].display, (col * SIZE_C, row * SIZE_R))


draw_pawns(True)

while running:
    window.blit(bg_img, (0, 0))
    draw_pawns()
    pygame.time.Clock().tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_col, m_row = [int(x // size) for x, size in zip(pygame.mouse.get_pos(), [SIZE_C, SIZE_R])]
            m_left_click, _, m_right_click = pygame.mouse.get_pressed()
            try:
                selected_figure = chess_board[m_row][m_col]
                print(m_row, m_col, selected_figure)
            except IndexError:
                continue
            if m_left_click and not isinstance(selected_figure, str):
                if selected_figure.color == "w" and player % 2 != 0 or \
                        selected_figure.color == "b" and player % 2 == 0:

                    move_target, chess_board[m_row][m_col] = selected_figure, f"{chr(97 + m_col)}{abs(m_row - 8)}"
                    row_pos, col_pos = [(x * 100) + 50 for x in move_target.position]
                    rect = move_target.display.get_rect(center=(col_pos, row_pos))
                    move_target.check_right_move(chess_board)
                    print(len(move_target.available_moves), move_target.available_moves)
                    if "Rook" in move_target.name:
                        move_target.castling = []
                        move_target.check_castling(chess_board)
                    selected_target = True

        if event.type == MOUSEBUTTONDOWN and selected_target:
            if rect.collidepoint(event.pos):
                moving = True

        elif event.type == MOUSEBUTTONUP and selected_target:
            moving = False

        elif event.type == MOUSEMOTION and moving and selected_target:

            rect.move_ip(event.rel)

        if event.type == MOUSEBUTTONUP and selected_target:
            p_col, p_row = [x // size for x, size in zip(pygame.mouse.get_pos(), [SIZE_C, SIZE_R])]
            print(f"drop point {p_row} {p_col}")
            if [p_row, p_col] in move_target.available_moves:
                if any(x in move_target.name for x in ("Pawn", "Rook", "King")):
                    move_target.first_move = False
                chess_board[p_row][p_col] = move_target
                move_target.position = (p_row, p_col)
                move_target.row, move_target.col = p_row, p_col
                player += 1
            else:
                if "Pawn" in move_target.name and move_target.make_queen:
                    player = make_new_queen_pic(m_row, m_col, player)
                else:
                    chess_board[m_row][m_col] = move_target
                    move_target.position = (m_row, m_col)
            selected_target = False
            move_target.available_moves = []

    if selected_target:
        window.blit(move_target.display, rect)
        pygame.draw.rect(window, BLUE, rect, 5)

    pygame.display.update()
pygame.quit()
