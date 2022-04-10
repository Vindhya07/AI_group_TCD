from BaseGame import BaseGame
from abc import ABC
import copy
from Utils import simulate_board, get_parameters_PD
from Model import PIECES, BOARDWIDTH, PIECES_COLORS, TEMPLATEWIDTH
import random
from operator import itemgetter
from NetworkX import TreePlot
from sidePanel import *
import csv
#https://github.com/yanyongyu/python-tetris

#  A new istance of TreePlot for plotting
PierreDellacheriePlot = TreePlot()


class PierreDellacherie(BaseGame, ABC):
    """
        Main class for MonteCarloTreeSearch algorithm (one object = one move), it implements abstract move() function of BaseGame
        Attributes
        ----------
                        None
        Methods
        -------
        get_expected_score(test_board)
            Calculate score of test_board
        get_move(board, piece, NextPiece)
            Execute Blind Bandit Monte Carlo Tree Search
        MonteCarlo_MCTS(board, piece, NextPiece)
            Execute
        MonteCarlo_MCTS_stepx(board, deep, piece, fatherName)
            Execute recursive MCTS function to go deep in the tree of moves
        get_expected_score(test_board)
            Calculate score of test_board
    """

    def __init__(self, r_p, gdSidePanel, mode):
        """
            Parameters
            ----------
            r_p : str
                type of the piece used in base game ('r' = random, 'p' = pi)
            mode : str
                type of function to use (randomScan or fullScan)
        """
        super().__init__(r_p, gdSidePanel, title=titleMCTS, description=descriptionMCTS)
        self.mode = mode
        self.action = ""
        self.deepLimit = 3

    def get_move(self):
        """
            Return the main function to use (MonteCarlo_MCTS)
        """
        return self.PierreDellacherie_PD(self.board, self.falling_piece, self.next_piece)

    def get_expected_score(self, test_board, heights_old, parent_board):
        """
            Calculate score of test_board with fixed weights
            Parameters
            ----------
                  test_board : Matrix (lists of lists) of strings
        """
        # Calcola lo score sulla board di test passando il vettore dei pesi di ogni metrica
        fullLines, heights, rows_cleared, board_row_transition, board_column_transition , board_buried_holes, board_wells = get_parameters_PD(test_board)
        landing_height = 0
        for index in range(0, len(heights_old)):
            if heights_old[index] != heights[index]:
                if heights[index] > landing_height:
                   landing_height = heights[index]
        #find the now of pieces contributed to clear the rows
        no_of_pieces_contib = 0
        for cleared_index in range(0, len(rows_cleared)):
            row = rows_cleared[cleared_index]
            for position in range(0, BOARDWIDTH):
                if parent_board[position][row] != test_board[position][row]:
                    no_of_pieces_contib = no_of_pieces_contib + 1
        eroded_piece_cells_metric = fullLines * no_of_pieces_contib
        
        test_score = (landing_height * -4.500158825082766 + 
        eroded_piece_cells_metric * 3.4181268101392694 + 
        board_row_transition * -3.2178882868487753 + 
        board_column_transition * -3.2178882868487753 + 
        board_buried_holes * -7.899265427351652 + 
        board_wells * -3.3855972247263626)
        return test_score

    # MonteCarlo Step 1 (DFS BASED)
    def PierreDellacherie_PD(self, board, piece, NextPiece):
        """
            Main Scanning function for Deep LV1
            Parameters
            ----------
            board : str
                Matrix (lists of lists) of strings
            piece : Object
                conteining 'shape', 'rotation', 'x', 'y', 'color'
            NextPiece : Object
                conteining 'shape', 'rotation', 'x', 'y', 'color'
        """
        deep = 1
        numIter = 0
        print("Branch Deep :", deep, " Real piece: ", piece['shape'])
        self.action = str(piece['shape'])
        topStrategies = list()
        strategy = None
        for rot in range(0, len(PIECES[piece['shape']])):
            for sideways in range(-5, 6):
                numIter = numIter + 1
                # print("<<< Into branch: n° ", numIter)
                move = [rot, sideways]
                fullLines, heights_old, rows_cleared, board_row_transition, board_column_transition , board_buried_holes, board_wells = get_parameters_PD(board)
                test_board = copy.deepcopy(board)
                test_piece = copy.deepcopy(piece)
                test_board = simulate_board(test_board, test_piece, move)

                fatherName = str(piece['shape'] + ":" + str(sideways) + ":" + str(0))
                PierreDellacheriePlot.addedge(PierreDellacheriePlot.ROOTZERO, fatherName)

                if test_board is not None:
                    test_score = self.get_expected_score(test_board, heights_old, board)
                    NextScore = 0
                    selfAction = ""
                    #  print("Tested branch : [ rot= ", rot, "/sideway=", sideways, "] : scored = ", round(test_score, 3))
                    if self.deepLimit > 1:
                        NextScore, selfAction = self.PierreDellacherie_PD_stepx(board, deep + 1, NextPiece, fatherName)
                        print("Dreamed action : ", self.action)
                        selfAction = self.action
                        self.action = str(piece['shape'])
                    NextScore = test_score#NextScore + test_score

                    if not strategy or strategy[2] < NextScore:
                        strategy = (rot, sideways, NextScore, selfAction)
                        topStrategies.append(strategy)

        PierreDellacheriePlot.Graph.clear()

        print("--->> TOP STRATEGIES <<---")
        topStrategies = sorted(topStrategies, key=itemgetter(2), reverse=True)
        for x in range(len(topStrategies)):
            print(topStrategies[x])

        print("---X>> Winner STRATEGY <<X---", topStrategies[0])

        return [topStrategies[0][0], topStrategies[0][1]]

    def PierreDellacherie_PD_stepx(self, board, deep, piece, fatherName):
        """
            Recursive Scanning of Virtual Branches on Deep > 2
            Parameters
            ----------
            board : str
                type of piece used ('r' = random, 'p' = pi)
            deep : str
                type of function to use (randomScan or fullScan)
            piece : Object
                conteining 'shape', 'rotation', 'x', 'y', 'color'
            fatherName : str
                str used to have trace of the fatherName to print Tree Graphs
        """
        if len(self.action.strip('-')) <= self.deepLimit:
            self.action = self.action + "-" + piece['shape']
        strategy = None

        sidewaysIndex = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]  # 11  Sideways

        # if mode is random, BBMCTS remove a random number of sideways from the Tree Search
        if self.mode == 'random':
            if deep > 2:
                toRemove = random.randint(0, 5)
                # print("------------------- toKill ", toRemove)
                for z in range(toRemove):
                    deathindex = random.randint(0, len(sidewaysIndex) - 1)
                    sidewaysIndex.pop(deathindex)

        for rot in range(0, len(PIECES[piece['shape']])):
            for sideways in sidewaysIndex:
                move = [rot, sideways]
                fullLines, heights_old, rows_cleared, board_row_transition, board_column_transition , board_buried_holes, board_wells = get_parameters_PD(board)
                test_board = copy.deepcopy(board)
                test_piece = copy.deepcopy(piece)
                test_board = simulate_board(test_board, test_piece, move)

                NameNode = str(piece['shape'] + ":" + str(sideways) + ":" + str(deep))
                PierreDellacheriePlot.addedge(fatherName, fatherName + "_" + NameNode)

                if test_board is not None:
                    test_score = self.get_expected_score(test_board, heights_old, board)
                    #  print("Tested branch : [ rot= ",rot ,"/sideway=",sideways," // deep= ",deep,"] : scored = ",round(test_score,3))

                    # print("yyyy: ", deep, " ",self.deepLimit)
                    if deep < self.deepLimit:
                        # print("dxxxxx: ", deep)
                        RandPiece = self.__random()
                        deepScore, pieceType = self.PierreDellacherie_PD_stepx(board, deep + 1, RandPiece,
                                                                          fatherName + "_" + NameNode)
                        test_score = test_score + deepScore

                    if not strategy or strategy[2] < test_score:
                        strategy = (rot, sideways, test_score)
        return strategy[2], self.action

    def __random(self):
        """
            Generate one of 7 random pieces
        """
        shape = random.choice(list(PIECES.keys()))
        new_piece = {
            'shape': shape,
            'rotation': random.randint(0, len(PIECES[shape]) - 1),
            'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
            'y': -2,  # start it above the board (i.e. less than 0)
            # 'color': random.randint(1,len(COLORS) - 1)
            'color': PIECES_COLORS[shape]
        }
        return new_piece


def pd_main(r_p, mode, numOfRun, gdSidePanel):
    #  loop to run  the game with AI for numOfRun executions
    numOfRun = int(numOfRun)
    AVG_runs = 0
    for x in range(numOfRun):
        mc = PierreDellacherie(r_p, gdSidePanel, mode)
        newScore, weights, tot_time, n_tetr, avg_move_time, tetr_s, final_score, lines_removed, time_array, score_array, lines_array = mc.run()
        AVG_runs = AVG_runs + newScore
        print("Game achieved a score of: ", newScore)
        print("weights: ", weights)
        print("tot run time: ", tot_time)
        print("#moves:  ", n_tetr)
        print("avg time per move: ", avg_move_time)
        print("moves/sec:  ", tetr_s)
        print("Final Score:", final_score)
        print("Lines Removed: ", lines_removed)

        f = open('pd_values.csv', 'w')
        writer = csv.writer(f)
        writer.writerow("PD Values CSV")
        writer.writerow(time_array)
        writer.writerow(score_array)
        writer.writerow(lines_array)
        f.close()

    AVG_runs = AVG_runs / numOfRun
    if numOfRun > 1:
        print("AVGScore after ", numOfRun, " Runs : ", AVG_runs)


if __name__ == "__main__":
    pd_main('r', 'full', 1,'no')



