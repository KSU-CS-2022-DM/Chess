####################################################
## Brian Behnke
## 11/25/2022
## Data Mining Techniques - CS 43105
## 
## Determines if a move at a given position is "good" based on past games
##
## Usage: python goodMoves.py <cleaned pgn file 1> ... <cleaned pgn file n>
## 
## Slightly modified version of a script written by Ethan Mai
## https://github.com/iAmEthanMai/chess-games-dataset/tree/main/Script
####################################################

import os
import sys
import pandas as pd
import numpy as np

import chess
import chess.pgn


def get_board_features(board):
    board_features = []
    for square in chess.SQUARES:
        board_features.append(str(board.piece_at(square)))

    return board_features


def get_move_features(move):
    from_square = np.zeros(64)
    to_square = np.zeros(64)

    from_square[move.from_square] = 1
    to_square[move.to_square] = 1

    return from_square, to_square


def play(board, nb_moves = 0):
    if(nb_moves == len(game_moves)):
        return

    # White won and is white's turn or black won and is black's turn, i.e. the move is considered "good."
    if white_won and board.turn or not white_won and not board.turn:
        legal_moves = list(board.legal_moves)
        good_move = game_moves[nb_moves]
        bad_moves = list(filter(lambda x: x != good_move, legal_moves))

        board_features = get_board_features(board)
        line = np.array([], dtype=object)

        # Append bad moves
        for move in bad_moves:
            from_square, to_square = get_move_features(move)
            line = np.concatenate((board_features, from_square, to_square, list([False])))
            data.append(line)

        # Append good move
        from_square, to_square = get_move_features(good_move)
        line = np.concatenate((board_features, from_square, to_square, list([True])))
        data.append(line)

    board.push(game_moves[nb_moves])
    return play(board, nb_moves + 1)


def process_game_data(filename):
    with open(filename, 'r') as pgn:
        game = chess.pgn.read_game(pgn)

        i = 1
        while game != None:
            global game_moves
            global data

            data = []

            game_moves = list(game.mainline_moves())
            board = game.board()

            play(board)

            board_feature_names = chess.SQUARE_NAMES
            move_from_feature_names = ['from_' + square for square in chess.SQUARE_NAMES]
            move_to_feature_names = ['to_' + square for square in chess.SQUARE_NAMES]

            columns = board_feature_names + move_from_feature_names + move_to_feature_names + list(['good_move'])

            df = pd.DataFrame(data=data, columns=columns)
            prefix = 'game_' + str(i)
            csv_filename = filename.replace('pgn', 'csv')
            csv_filename = prefix + '_' + csv_filename

            dirname = 'csv/'
            path = os.path.join(dirname, csv_filename)
            df.to_csv(path, index=False)
            game = chess.pgn.read_game(pgn)
            i += 1

    return


if __name__ == '__main__':
    global white_won
    for filename in sys.argv[1:]:
        if 'white' in filename:
            white_won = True
        else:
            white_won = False

        process_game_data(filename)