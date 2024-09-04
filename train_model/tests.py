import keras
import chess
import numpy as np
from dataoperate import bitboard, df

board = chess.Board()
print(board.fen())


# model = keras.saving.load_model("model.keras")
# board = chess.Board()
# legals = [str(move) for move in board.legal_moves]
# i = 0
# m = []
# if len(legals) != 0:
#     for index in range(len(legals)):
#         tboard = board.copy()
#         tboard.push_san(legals[index])
#         #print(tboard)
#         x = np.array([bitboard(tboard), ])
#         print(model(x))
#         if model(x) > -1:
#             max_estimation = model(x)
#             i = index
#
#
# board.push_san(legals[i])
# legals = [str(move) for move in board.legal_moves]
# board.push_san(legals[7])
# print(model.predict(np.array([bitboard(board),])))
# print(i)


