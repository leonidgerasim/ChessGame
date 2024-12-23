import chess
import chess.engine
from chess import copy
from gui_components.boards import ChessBoard
import numpy as np
import math
from train_model.dataoperate import bitboard
import random


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
        engine = load_engine_from_cmd('./sunfish.py')
        limit = chess.engine.Limit(
            white_clock=30, black_clock=30, white_inc=1, black_inc=1
        )
        game_id = random.random()
        chosen_move = self.board.san(get_engine_move(engine, self.board, limit, game_id, debug=False))

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


def load_engine_from_cmd(path, debug=False):
    engine = chess.engine.popen_uci(path)
    if hasattr(engine, "debug"):
        engine.debug(debug)
    return engine


async def get_engine_move(engine, board, limit, game_id, multipv=1, debug=False):
    if isinstance(engine, chess.engine.XBoardProtocol):
        play_result = await engine.play(board, limit, game=game_id)
        return play_result.move

    multipv = min(multipv, board.legal_moves.count())
    with await engine.analysis(
        board, limit, game=game_id, info=chess.engine.INFO_ALL, multipv=multipv or None
    ) as analysis:

        infos = [None for _ in range(multipv)]
        first = True
        async for new_info in analysis:
            # If multipv = 0 it means we don't want them at all,
            # but uci requires MultiPV to be at least 1.
            if multipv and "multipv" in new_info:
                infos[new_info["multipv"] - 1] = new_info

            # Parse optional arguments into a dict
            if debug and "string" in new_info:
                print(new_info["string"])

            if not debug and all(infos) and "score" in analysis.info:
                if not first:
                    # print('\n'*(multipv+1), end='')
                    print(f"\u001b[1A\u001b[K" * (multipv + 1), end="")
                else:
                    first = False

                info = analysis.info
                score = info["score"].relative
                score = (
                    f"Score: {score.score()}"
                    if score.score() is not None
                    else f"Mate in {score.mate()}"
                )
                print(
                    f'{score}, nodes: {info.get("nodes", "N/A")}, nps: {info.get("nps", "N/A")},'
                    f' time: {float(info.get("time", 0)):.1f}',
                    end="",
                )
                print()

                for info in infos:
                    if "pv" in info:
                        variation = board.variation_san(info["pv"][:10])
                    else:
                        variation = ""

                    if "score" in info:
                        score = info["score"].relative
                        score = (
                            math.tanh(score.score() / 600)
                            if score.score() is not None
                            else score.mate()
                        )
                        key, *val = info.get("string", "").split()
                        if key == "pv_nodes":
                            nodes = int(val[0])
                            rel = nodes / analysis.info["nodes"]
                            score_rel = f"({score:.2f}, {rel*100:.0f}%)"
                        else:
                            score_rel = f"({score:.2f})"
                    else:
                        score_rel = ""

                    # Something about N
                    print(f'{info["multipv"]}: {score_rel} {variation}')

        return analysis.info["pv"][0]

