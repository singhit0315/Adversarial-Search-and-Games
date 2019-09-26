from random import randint
from BaseAI_3 import BaseAI
import time

class PlayerAI(BaseAI):
    # weights used to calculate the heuristic score of the grid
    weight = [[15,14,13,12],[8,9,10,11],[7,6,5,4],[0,1,2,3]]
    # time at which getMove() was called
    start_time = 0
    # maximum depth used for minimax
    maxdepth = 4

    def __init__(self):
        # initialize the weight matrix values
        for i in range(4):
            for j in range(4):
                self.weight[i][j] = pow(4,self.weight[i][j])

    def getMove(self, grid):
        # timestamp the time call is made to this method
        self.start_time = time.clock()
        # get all possible moves
        moves = grid.getAvailableMoves()
        # move that generates the max score for agent
        maxMove = None
        # max score for the Agent
        maxScore = -float('inf')

        # process all moves
        for move in moves:
            # clone the current grid
            gridNext = grid.clone()
            # apply the move to the current grid clone
            if gridNext.move(move):       
                # recursively call minimax with Computer being the player         
                (timeout,score) = self.minimax(gridNext, 'computer', -float('inf'), float('inf'), 1)
                # update max score
                if score > maxScore:
                    maxScore = score
                    maxMove = move 
                # if timed out then return the current max move
                if timeout:
                    return maxMove
        return maxMove

    # The MiniMax algorithm with alpha beta pruning
    def minimax(self, grid, player, alpha, beta, depth):
        # return the evaluated grid if there is timeout, or max depth reached 
        if (time.clock() - self.start_time ) >= 0.15 or depth >= self.maxdepth:
            return (True,self.heuristic_eval(grid))

        # get the available moves on current grid
        moves = grid.getAvailableMoves()
        # return evaluated current grid as score if there are no moves available
        if len(moves) == 0:
            return (False,self.heuristic_eval(grid))

        # maximize score if player is Agent
        if player == 'agent':
            maxScore = -float('inf')
            for move in moves:
                gridNext = grid.clone()
                if gridNext.move(move):
                    (timeout,score) = self.minimax(gridNext, 'computer', alpha, beta, depth+1)
                    if score > maxScore:
                        maxScore = score
                    if timeout:
                        return (True,maxScore)
                    if maxScore >= beta:
                        return (False,maxScore)
                    if maxScore > alpha:
                        alpha = maxScore
            return maxScore
        # minimize score if player is Computer
        else:
            minScore = float('inf')
            for move in moves:
                gridNext = grid.clone()
                if gridNext.move(move):
                    (timeout,score) = self.minimax(gridNext, 'agent', alpha, beta, depth+1)
                    if score < minScore:
                        minScore = score
                    if timeout:
                        return (True,minScore)
                    if minScore <= alpha:
                        return (False,minScore)
                    if minScore < beta:
                        beta = minScore
            return minScore
    	
    # Heuristic function to evaluate score of a given grid
    # Adds up the grid cell values to the weight matrix
    def heuristic_eval(self, grid):
    	score = 0
    	for i in range(4):
    		for j in range(4):
    			pos = [i,j]
    			score += self.weight[i][j] + grid.getCellValue(pos)
    	return score


    