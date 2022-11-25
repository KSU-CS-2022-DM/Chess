####################################################
## Brian Behnke
## 11/20/2022
## Data Mining Techniques - CS 43105
## Takes .pgn files from the FICS games database and prints the mainline moves of games where a player either
## resigned or was checkmated into a new file.
##
## Usage: python pruneData.py <ficsgamesdb pgn file 1> ... <ficsgamesdb pgn file n>
####################################################

import chess.pgn
import sys


def main():
    for i in sys.argv[1:]:
        with open(i, 'r') as pgn:
            # Gets year from ficsgamesdb filename
            year = i[12:16:1]
            black_wins = open('cleaned_games_' + year + '_black_wins.pgn', 'a')
            white_wins = open('cleaned_games_' + year + '_white_wins.pgn', 'a')

            game = chess.pgn.read_game(pgn)
            while game != None:
                gamestr = str(game.mainline_moves())
                if 'checkmated' in gamestr or 'resigns' in gamestr:
                    if 'White' in gamestr:
                        print(gamestr, file=black_wins, end='\n\n')
                    else:
                        print(gamestr, file=white_wins, end='\n\n')
                game = chess.pgn.read_game(pgn)

            black_wins.close()
            white_wins.close()


if __name__ == '__main__':
    main()