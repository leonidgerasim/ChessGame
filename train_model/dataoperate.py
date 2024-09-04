import chess
import pandas as pd
import numpy as np
import time
import os
import tensorflow as tf
import keras


path_data = 'train_model/games.csv'
df = pd.read_csv(path_data)


def bitboard(game):
    bitboard = np.array([], dtype=np.int8)
    for k in range(2):
        for i in range(6):
            piece = list(game.pieces(i + 1, 1 - k))
            piece_bits = np.zeros(64, dtype=np.int8)
            for pos in piece:
                piece_bits[pos] = 1
            bitboard = np.append(bitboard, piece_bits)
    return bitboard


def combination_code(board, flag):
    c = []
    PIECE_SYMBOLS_NEW = ['.', 'P', 'R', 'N', 'B', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    def peace(cell): return '.' if board.piece_at(cell) == None else str(board.piece_at(cell))
    for cell in range(64):
        c.append(PIECE_SYMBOLS_NEW.index(peace(cell)))
    c.append(flag)
    return tuple(c)


class Dataset:
    def __init__(self, size):
        self.dataset = {}
        self.count = 0
        self.histories = []
        self.create_histories()
        for i, hist in enumerate(self.histories):
            board = chess.Board()
            if df.winner[i] == 'white':
                result = True
            else:
                result = False
            for index in range(min(size, len(hist))):
                flag = index % 2 == 0
                board.push_san(hist[index])
                result = result and flag
                b = bitboard(board)
                # rboard = board.copy()
                # p = bitboard(board)
                # legals = [str(move) for move in rboard.legal_moves]
                # ri = np.random.random_integers(0, len(legals)-1)
                # while legals[ri] == hist[index]:
                #     ri = np.random.random_integers(0, len(legals)-1)
                # board.push_san(hist[index])
                # rboard.push_san(legals[ri])
                # q = bitboard(board)
                # r = bitboard(rboard)
                # key = hash(combination_code(board, flag))

                self.add(index, b, result)

    def add(self, index, b, result):
        key = hash(tuple(b))
        if self.dataset.get(index) is None:
            self.dataset[index] = {key: [b, 1, int(result), int(result)]}
            self.count += 1
            if self.count % 1000 == 0:
                print(self.count, ' - уникальных комбинаций')
        else:
            if self.dataset[index].get(key) is None:
                self.dataset[index][key] = [b, 1, int(result), int(result)]
            else:
                self.dataset[index][key][1] += 1
                self.dataset[index][key][2] += int(result)
                self.dataset[index][key][3] = self.dataset[index][key][2]/self.dataset[index][key][1]

    def values(self):
        return self.dataset.values()

    def items(self):
        return self.dataset.items()

    def print(self):
        dataf = pd.DataFrame({'keys': self.dataset.keys(), 'values': self.dataset.values()})
        for i in self.dataset:
            print(len(self.dataset[i]))

    def create_histories(self):
        for moves in df.moves:
            self.histories.append(moves.split())


def create_y_train(p, model):
    yp_train = model.predict(p, batch_size=len(p))
    return yp_train



