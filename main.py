import os

CHESS_BOARD_SIZE, CURRENT_PATH = 8, os.getcwd()
chess_board = []
directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1),
              "top left diagonal": (-1, -1), "top right diagonal": (-1, 1),
              "bottom left diagonal": (1, -1), "bottom right diagonal": (1, 1), "knight": {
        "up left": (-2, -1), "up right": (-2, 1), "down left": (2, -1), "down right": (2, 1),
        "left up": (-1, -2), "left down": (1, -2), "right up": (-1, 2), "right down": (1, 2),
    }
              }


class Figure:
    def __init__(self, name: str, color: str, position: tuple):
        self.row, self.col = position
        self.available_moves = []
        self.name = name
        self.position = position
        self.mouse_pos = None
        self.color = color
        self.picture = f"{CURRENT_PATH}\pictures\{self.color}_{self.name.split(' - ')[0].lower()}.png"
        self.display = None

    @staticmethod
    def check_board(row, col):
        return 0 <= row < CHESS_BOARD_SIZE and 0 <= col < CHESS_BOARD_SIZE

    @staticmethod
    def movement(row, col, direction):
        return row + directions[direction][0], col + directions[direction][1]

    def general_move(self, matrix, steps, move_directions, castling=False):
        for direction in move_directions:
            row, col = self.row, self.col
            for step in range(steps):
                row, col = self.movement(row, col, direction)
                if self.check_board(row, col):
                    print(f"{row}, {col} - rook")
                    figure = matrix[row][col]
                if self.check_board(row, col) and isinstance(figure, str) or \
                        self.check_board(row, col) and not isinstance(figure, str) and figure.color \
                        != self.color:
                    if castling:
                        self.castling.append([row, col])
                    else:
                        self.available_moves.append([row, col])
                else:
                    break


class Pawn(Figure):
    def __init__(self, name: str, color: str, position: tuple):
        super(Pawn, self).__init__(name, color, position)
        self.castling = None
        self.first_move = True

    def check_right_move(self, matrix):
        color_ = {
            "w": ["up", "top left diagonal", "top right diagonal"],
            "b": ["down", "bottom left diagonal", "bottom right diagonal"]

        }
        step = 1
        row, col = self.row, self.col
        if self.first_move:
            step = 2
        if not self.available_moves:
            for steps in range(step):
                row, col = self.movement(row, col, color_[self.color][0])
                figure = matrix[row][col]
                if self.check_board(row, col) and isinstance(figure, str):
                    self.available_moves.append([row, col])

            for pos in range(1, 3):
                row, col = self.movement(self.row, self.col, color_[self.color][pos])
                if self.check_board(row, col) and not isinstance(matrix[row][col], str) and matrix[row][col].color \
                        != self.color:
                    self.available_moves.append([row, col])

    def make_queen(self):
        pass


class Rook(Figure):
    def __init__(self, name: str, color: str, position: tuple):
        super(Rook, self).__init__(name, color, position)
        self.castling = None
        self.first_move = True

    def check_right_move(self, matrix):
        self.general_move(matrix, CHESS_BOARD_SIZE, list(directions.keys())[:4])

    def check_castling(self, matrix):
        if self.first_move and not isinstance(matrix[self.row][4], str) \
                and "King" in matrix[self.row][4].name and matrix[self.row][4].first_move:

            if all([isinstance(x, str) for x in matrix[self.row][1:4]]) or \
                    all([isinstance(x, str) for x in matrix[self.row][5:7]]):
                self.castling = []
                self.general_move(matrix, CHESS_BOARD_SIZE, list(directions.keys())[:-1], True)
                print(f"{self.castling} list castling")


class Knight(Figure):

    def check_right_move(self, matrix):
        for row, col in directions["knight"].values():
            row, col = row + self.row, self.col + col
            if self.check_board(row, col):
                print(f"{row}, {col} - rook")
                figure = matrix[row][col]
            if self.check_board(row, col) and isinstance(figure, str) or \
                    self.check_board(row, col) and not isinstance(figure, str) and figure.color \
                    != self.color:
                self.available_moves.append([row, col])


class Bishop(Figure):

    def check_right_move(self, matrix):
        self.general_move(matrix, CHESS_BOARD_SIZE, list(directions.keys())[4:-1])


class Queen(Figure):

    def check_right_move(self, matrix):
        self.general_move(matrix, CHESS_BOARD_SIZE, list(directions.keys())[:-1])


class King(Figure):
    def __init__(self, name: str, color: str, position: tuple):
        super(King, self).__init__(name, color, position)
        self.castling = None
        self.first_move = True

    def check_right_move(self, matrix):
        self.general_move(matrix, 1, list(directions.keys())[:-1])


def create_chess_board():
    colors = {
        6: "w",
        1: "b",
        7: "w",
        0: "b"

    }

    for row in range(CHESS_BOARD_SIZE):
        chess_board.append([])
        for col in range(CHESS_BOARD_SIZE):
            pos = f"{chr(97 + col)}{abs(row - 8)}"

            if row in (6, 1):
                chess_board[row].append(Pawn(f"Pawn - {pos}", colors[row], (row, col)))

            elif row not in (7, 0):
                chess_board[row].append(f"{chr(97 + col)}{abs(row - 8)}")
                continue

            elif col in (0, 7):
                chess_board[row].append(Rook(f"Rook - {pos}", colors[row], (row, col)))

            elif col in (1, 6):
                chess_board[row].append(Knight(f"Knight - {pos}", colors[row], (row, col)))

            elif col in (2, 5):
                chess_board[row].append(Bishop(f"Bishop - {pos}", colors[row], (row, col)))

            elif col == 3:
                chess_board[row].append(Queen(f"Queen - {pos}", colors[row], (row, col)))

            elif col == 4:
                chess_board[row].append(King(f"King - {pos}", colors[row], (row, col)))

    return chess_board
