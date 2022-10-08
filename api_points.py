from flask import *
from main import *
import json

app = Flask(__name__)
web_pos = {}


def create_dic_web_pos():
    counter = 0
    for row in range(len(chess_board)):
        for col in range(len(chess_board[row])):
            counter += 1
            web_pos[f"{row} {col}"] = web_pos.get(f"{row} {col}", counter)


def getting_legal_moves_ouput(symbol):
    try:
        symbol.available_moves = []
        symbol.check_right_move(chess_board)
        result = []
        for a_row, a_col in symbol.available_moves:
            result.append({"position": web_pos[f"{a_row} {a_col}"], "row": a_row, "col": a_col})
        if result:
            return result
        return 0
    except AttributeError:
        return 0


def matrix_current_pos(chess_board):
    result = []
    for row in range(len(chess_board)):
        for col in range(len(chess_board[row])):
            symbol_matrix = chess_board[row][col]
            if isinstance(symbol_matrix, str):
                result.append({"position": web_pos[f"{row} {col}"], "type": 0, "color": 0, "row": row, "col": col,
                               "moves": 0})

            else:
                result.append({"position": web_pos[f"{row} {col}"], "type": symbol_matrix.name.split("-")[0][:-1].lower(),
                               "color": symbol_matrix.color, "row": row, "col": col,
                               "moves": getting_legal_moves_ouput(symbol_matrix)})
    return json.dumps(result, indent=9)


@app.route("/new_game", methods=["GET"])
def main_game():
    global chess_board
    chess_board = create_chess_board()
    create_dic_web_pos()
    return matrix_current_pos(chess_board)


@app.route("/", methods=["GET"])
def show_board():
    return matrix_current_pos(chess_board)


@app.route("/moves/<string:info>", methods=["POST"])
def ask_for_available_pos(info):
    c_row, c_col, m_row, m_col = [int(x) for x in info]
    target = chess_board[c_row][c_col]
    try:
        target.available_moves = []
        target.check_right_move(chess_board)
        if [m_row, m_col] in target.available_moves:
            target.position = (m_row, m_col)
            chess_board[m_row][m_col], chess_board[c_row][c_col] = target, f"{chr(97 + c_row)}{abs(c_col - 9)}"
            target.row, target.col = m_row, m_col
    except AttributeError:
        pass
    return matrix_current_pos(chess_board)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # app.run(port=7777)
    # app.run(port=7777)
