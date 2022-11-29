####################################################
## Christabel Akhigbe
## 11/27/2022
## Data Mining Techniques - CS 43105
## minMax Algorithm (with AlphaBeta pruning)
## 
## References Thomas Hale's "sunfish" script; https://github.com/thomasahle/sunfish
####################################################

import chess
import sys
import math
import random
#import scripts

#coordinates pulled from sunfish

def eval(board):
    i = 0
    eval = 0
    x = True
    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x
    while i < 63:
        i += 1
        eval = eval + (getValue(str(board.piece_at(i))) if x else -getValue(str(board.piece_at(i))))
    return eval

def getValue(piece): #return the value of a piece
    #if (ai_white):
    #    sign_white = -1
    #    sign_black = 1
    #else:
    #    sign_white = 1
    #    sign_black = -1
    #useful for play game, not implemented yet?
    if(piece == None):
        return 0
    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == 'K' or piece == 'k':
        value = 900
    return value

def minMax(depth, board, alpha, beta, isMax):
    if(depth == 0):
        return -eval(board)
    realMoves = board.legal_moves
    
    if(isMax):
        bestMove = -9999
        for x in realMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = max(bestMove,minMax(depth - 1, board, alpha, beta, not (isMax)))
            board.pop()
            alpha = max(alpha, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for x in realMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = min(bestMove, minMax(depth - 1, board, alpha, beta, not isMax))
            board.pop()
            beta = min(beta, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove

def root(depth, board, isMax):
    realMoves = board.legal_moves
    bestMove = -9999
    nextBest = -9999
    bestMoveFinal = None
    for x in realMoves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(bestMove, minMax(depth - 1, board, -10000, 10000, not isMax))
        board.pop()
        if( value > bestMove):
            print("Best score: " ,str(bestMove))
            print("Best move: ",str(bestMoveFinal))
            print("Next best: ", str(nextBest))
            nextBest = bestMove
            bestMove = value
            bestMoveFinal = move
    return bestMoveFinal

#######################################
#######################################

def main():
    board = chess.Board()
    n = 0
    print(board)
    #some random assignment of white/black to ai
    while n < 100:
        if n%2 == 0:
            move = input("Enter move: ")
            move = chess.Move.from_uci(str(move))
            board.push(move)
        else:
            print("Computers Turn:")
            move = root(3,board,True)
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)
        n += 1

if __name__ == "__main__":
    main()
    
    
################################################
################################################