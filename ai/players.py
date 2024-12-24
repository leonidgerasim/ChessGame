import chess
import chess.engine
from chess import copy
from gui_components.boards import ChessBoard
import numpy as np
import math
import random


piece_score = {'K': 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1, 'k': 0, "q": 9, "r": 5, "b": 3, "n": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {'N': knight_scores,
                         'n': knight_scores[::-1],
                         'B': bishop_scores,
                         'b': bishop_scores[::-1],
                         'Q': queen_scores,
                         'q': queen_scores[::-1],
                         'R': rook_scores,
                         'r': rook_scores[::-1],
                         'P': pawn_scores,
                         'p': pawn_scores[::-1]}


class AIPlayer:
    def __init__(self, board: chess.Board, color: str) -> None:
        self.board = board
        self.color = color
        self.count = 0

    def get_legal_moves(self, board: chess.Board = None) -> list:
        if not board:
            board = self.board

        return list(board.legal_moves)

    def false_move(self, move: chess.Move = None, board: chess.Board = None) -> chess.Board:
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
        # make a move an ChessBoard object
        move = find_best_move(self.board, 3)
        chess_board._play(move=move)
        self.count += 1


def scoreBoard(board):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    score = 0
    for r in range(8):
        for c in range(8):
            piece = board.piece_at(chess.square(r, c))
            if piece != None:
                piece_position_score = 0
                if piece.symbol() not in "Kk":
                    piece_position_score = piece_position_scores[piece.symbol()][r][c]
                if piece.symbol() in "KNBQRP":
                    score += piece_score[piece.symbol()] + piece_position_score
                else:
                    score -= piece_score[piece.symbol()] + piece_position_score

    return score


# Алгоритм минимакс с альфа-бета отсечением
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return maximizing_player*scoreBoard(board)

    legal_moves = list(board.legal_moves)

    max_eval = -float('inf')
    for move in legal_moves:
        tboard = board.copy()
        tboard.push(move)
        eval = minimax(tboard, depth - 1, -beta, -alpha, -maximizing_player)
        max_eval = max(max_eval, eval)
        alpha = max(alpha, eval)
        if beta <= alpha:
            break  # Альфа-бета отсечение
    return -max_eval


# Функция для поиска лучшего хода
def find_best_move(board, depth):
    best_move = None
    best_value = -float('inf')

    legal_moves = list(board.legal_moves)

    for move in legal_moves:
        tboard = board.copy()
        tboard.push(move)
        move_value = minimax(tboard, depth - 1, -float('inf'), float('inf'), -1)
        print(move_value, move)

        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move
