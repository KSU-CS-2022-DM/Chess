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
            cgf = open('cleaned_games_' + year + '.pgn', 'a')

            game = chess.pgn.read_game(pgn)
            while game != None:
                gamestr = str(game.mainline_moves())
                if 'checkmated' in gamestr or 'resigns' in gamestr:
                    print(gamestr, file=cgf, end='\n\n')
                game = chess.pgn.read_game(pgn)

            cgf.close()


if __name__ == '__main__':
    main()