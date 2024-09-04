import chess
from chess import copy
from gui_components.boards import ChessBoard
import numpy as np
import keras
from train_model.dataoperate import bitboard


class AIPlayer:
    def __init__(self, board: chess.Board, color: str) -> None:
        self.board = board
        self.color = color
        self.count = 0

    def get_legal_moves(self, board: chess.Board=None) -> list:
        if not board:
            board = self.board

        return list(board.legal_moves)

    def choose_move(self, board: chess.Board=None):
        legal_moves = self.get_legal_moves()
        model = keras.saving.load_model("train_model/models/model"+str(self.count)+".keras")

        max_estimation = 0
        i = 0

        if len(legal_moves) != 0 and not board:
            board = self.board
            for index in range(len(legal_moves)):
                tboard = board.copy()
                tboard.push_san(str(legal_moves[index]))
                x = np.array([bitboard(tboard), ])
                if model(x) > max_estimation:
                    max_estimation = model(x)
                    i = index
            chosen_move = legal_moves[i]
        else:
            chosen_move = None

        # for move in legal_moves:
        #     evaluation_before = self.evaluate_board()
        #     fake_board = self.false_move(move)
        #     evaluation_after = self.evaluate_board(fake_board)
        #
        #     if chosen_move is None:
        #         chosen_move = move
        #     else:
        #         # if the player is white and the move results in a higher material for white
        #         if evaluation_after > evaluation_before and self.color == "w":
        #             chosen_move = move
        #         # if the player is black and the move results in higher material for black
        #         elif evaluation_before > evaluation_after and self.color == "b":
        #             chosen_move = move

        return chosen_move


    def false_move(self, move: chess.Move=None, board: chess.Board=None) -> chess.Board:
        # make a move without affecting the game's current state

        # make a copy of the board for move testing
        if not board:
            board_copy = copy.deepcopy(self.board)
        else:
            board_copy = board

        if not move:
            move = self.play(board_copy)

        board_copy.push(move)

        return board_copy


    def make_move(self, chess_board: ChessBoard):
        # make a move an a ChessBoard object
        move = self.choose_move()
        chess_board._play(move=move)
        self.count += 1

