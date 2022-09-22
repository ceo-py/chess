CHESS_BOARD_SIZE = 8

chess_board = []
chess_board_labels = {}

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
        self.first_move = True
        self.picture = f"{self.color}_{self.name.split(' - ')[0].lower()}.png"
        self.display = None

    def check_board(self, row, col):
        return 0 <= row < CHESS_BOARD_SIZE and 0 <= col < CHESS_BOARD_SIZE

    def movement(self, row, col, direction):
        return row + directions[direction][0], col + directions[direction][1]


class Pawn(Figure):

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

    def check_right_move(self, matrix):
        for direction in list(directions.keys())[:4]:
            row, col = self.row, self.col
            for step in range(CHESS_BOARD_SIZE):
                row, col = self.movement(row, col, direction)
                if self.check_board(row, col):
                    print(f"{row}, {col} - rook")
                    figure = matrix[row][col]
                if self.check_board(row, col) and isinstance(figure, str) or \
                        self.check_board(row, col) and not isinstance(figure, str) and figure.color \
                        != self.color:
                    self.available_moves.append([row, col])
                else:
                    break


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
        for direction in list(directions.keys())[4:-1]:
            row, col = self.row, self.col
            for step in range(CHESS_BOARD_SIZE):
                row, col = self.movement(row, col, direction)
                if self.check_board(row, col):
                    print(f"{row}, {col} - rook")
                    figure = matrix[row][col]
                if self.check_board(row, col) and isinstance(figure, str) or \
                        self.check_board(row, col) and not isinstance(figure, str) and figure.color \
                        != self.color:
                    self.available_moves.append([row, col])
                else:
                    break


class Queen(Figure):

    def check_right_move(self, matrix):
        for direction in list(directions.keys())[:-1]:
            row, col = self.row, self.col
            for step in range(CHESS_BOARD_SIZE):
                row, col = self.movement(row, col, direction)
                if self.check_board(row, col):
                    print(f"{row}, {col} - rook")
                    figure = matrix[row][col]
                if self.check_board(row, col) and isinstance(figure, str) or \
                        self.check_board(row, col) and not isinstance(figure, str) and figure.color \
                        != self.color:
                    self.available_moves.append([row, col])
                else:
                    break


class King(Figure):

    def check_right_move(self, matrix):
        for direction in list(directions.keys())[:-1]:
            row, col = self.row, self.col
            for step in range(1):
                row, col = self.movement(row, col, direction)
                if self.check_board(row, col):
                    print(f"{row}, {col} - rook")
                    figure = matrix[row][col]
                if self.check_board(row, col) and isinstance(figure, str) or \
                        self.check_board(row, col) and not isinstance(figure, str) and figure.color \
                        != self.color:
                    self.available_moves.append([row, col])
                else:
                    break


def create_chess_board():
    for row in range(CHESS_BOARD_SIZE):
        chess_board.append([])
        for col in range(CHESS_BOARD_SIZE):
            pos = f"{chr(97 + col)}{abs(row - 8)}"

            if row == 6:
                chess_board[row].append(Pawn(f"Pawn - {pos}", "w", (row, col)))
            elif row == 1:
                chess_board[row].append(Pawn(f"Pawn - {pos}", "b", (row, col)))

            elif row == 7 and any(col == x for x in (0, 7)):
                chess_board[row].append(Rook(f"Rook - {pos}", "w", (row, col)))
            elif row == 0 and any(col == x for x in (0, 7)):
                chess_board[row].append(Rook(f"Rook - {pos}", "b", (row, col)))

            elif row == 7 and any(col == x for x in (1, 6)):
                chess_board[row].append(Knight(f"Knight - {pos}", "w", (row, col)))
            elif row == 0 and any(col == x for x in (1, 6)):
                chess_board[row].append(Knight(f"Knight - {pos}", "b", (row, col)))

            elif row == 7 and any(col == x for x in (2, 5)):
                chess_board[row].append(Bishop(f"Bishop - {pos}", "w", (row, col)))
            elif row == 0 and any(col == x for x in (2, 5)):
                chess_board[row].append(Bishop(f"Bishop - {pos}", "b", (row, col)))

            elif row == 7 and col == 3:
                chess_board[row].append(Queen(f"Queen - {pos}", "w", (row, col)))
            elif row == 0 and col == 3:
                chess_board[row].append(Queen(f"Queen - {pos}", "b", (row, col)))

            elif row == 7 and col == 4:
                chess_board[row].append(King(f"King - {pos}", "w", (row, col)))
            elif row == 0 and col == 4:
                chess_board[row].append(King(f"King - {pos}", "b", (row, col)))

            else:
                chess_board[row].append(f"{chr(97 + col)}{abs(row - 8)}")

    return chess_board