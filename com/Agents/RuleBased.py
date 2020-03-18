from com.Core.BaseGame import BaseGame
from com.Core.Model import BOARDHEIGHT, BOARDWIDTH, is_on_board
import sys
import copy
from com.Utils.Utils import simulate_board, get_parameters
from com.Core.Model import PIECES
from com.Menu import menu
import random
from pyswip import Prolog

prolog = Prolog()
# prolog.consult("C:/Users/matti/PyCharmProjects/DiscoTetris/com/Utils/Kb.pl");
prolog.consult("com/Utils/Kb.pl")


class RuleBased(BaseGame):
    def __init__(self, r_p):
        super().__init__(r_p)
        self.crest = [0] * BOARDWIDTH  # cresta relativa

    def get_move(self):
        # self.update_crest(self.get_heights(self.board))
        self.crest = self.get_heights(self.board)
        self.writePCrest(self.get_Pcrest())
        # return self.align(self.get_move_by_rule(self.falling_piece, self.get_Pcrest()), self.falling_piece)
        return self.get_move_by_rule(self.falling_piece)

    def simulate_move(self, move, piece):
        test_board = copy.deepcopy(self.board)
        test_piece = copy.deepcopy(piece)
        test_board = simulate_board(test_board, test_piece, move)
        if test_board is not None:
            test_score, _ = self.get_expected_score(test_board)
            return test_score
        else:
            return -99  # con questo punteggio una mossa non valida non verrà considerata

    def get_expected_score(self, test_board):
        ### Calcola lo score sulla board di test passando il vettore dei pesi di ogni metrica
        fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
        test_score = float(
            (fullLines * 2) - (vHoles) - (vBlocks * 0.5) - ((maxHeight ** 1.5) * 0.02) - (stdDY * 0.01) - (
                    absDy * 0.2) - (maxDy * 0.3))
        return test_score, fullLines

    def align(self, move, piece):
        rot = move[0]
        sideway = move[1]
        if piece['shape'] == 'S' or piece['shape'] == 'Z' or piece['shape'] == 'I':
            new_rot = abs(rot - piece['rotation'])
        elif piece['shape'] == 'J' or piece['shape'] == 'L' or piece['shape'] == 'T':
            if piece['rotation'] == 3:
                if rot == 3:
                    new_rot = 0
                elif rot == 2:
                    new_rot = 3
                elif rot == 1:
                    new_rot = 2
                else:
                    new_rot = 1
            if piece['rotation'] == 2:
                if rot == 3:
                    new_rot = 1
                elif rot == 2:
                    new_rot = 0
                elif rot == 1:
                    new_rot = 3
                else:
                    new_rot = 2
            if piece['rotation'] == 1:
                if rot == 3:
                    new_rot = 2
                elif rot == 2:
                    new_rot = 3
                elif rot == 1:
                    new_rot = 0
                else:
                    new_rot = 1
            else:
                new_rot = rot

        else:
            new_rot = 0

        # new_rot = abs(rot - piece['rotation'])
        if piece['shape'] == 'I':
            new_sideway = sideway - 5
        elif piece['shape'] == 'O' or piece['shape'] == 'Z' or piece['shape'] == 'S' or piece['shape'] == 'T' or piece[
            'shape'] == 'L' or piece['shape'] == 'J':
            new_sideway = sideway - 4
        else:
            new_sideway = sideway - 6
        return [new_rot, new_sideway]

    def get_move_by_rule(self, piece):
        iFlag = False
        query = list()
        if piece['shape'] == 'S':
            query.append('bestFit(s0, X0)')
            query.append('bestFit(s1, X1)')
        elif piece['shape'] == 'Z':
            query.append('bestFit(z0, X0)')
            query.append('bestFit(z1, X1)')
        elif piece['shape'] == 'J':
            query.append('bestFit(j0, X0)')
            query.append('bestFit(j1, X1)')
            query.append('bestFit(j2, X2)')
            query.append('bestFit(j3, X3)')
        elif piece['shape'] == 'L':
            query.append('bestFit(l0, X0)')
            query.append('bestFit(l1, X1)')
            query.append('bestFit(l2, X2)')
            query.append('bestFit(l3, X3)')
        elif piece['shape'] == 'I':
            query.append('bestFit(i0, X0)')
            query.append('bestFit(i1, X1)')
        elif piece['shape'] == 'O':
            query.append('bestFit(o0, X0)')
        elif piece['shape'] == 'T':
            query.append('bestFit(t0, X0)')
            query.append('bestFit(t1, X1)')
            query.append('bestFit(t2, X2)')
            query.append('bestFit(t3, X3)')

        scores = list()
        print('----------')
        for q in query:
            results = list(prolog.query(q))
            while len(results) > 0:
                X0 = 0
                X1 = 0
                X2 = 0
                X3 = 0
                posX0 = False
                posX1 = False
                posX2 = False
                posX3 = False
                result = results.pop(len(results) - 1)
                print(result)
                try:
                    X0 = result['X0']
                    posX0 = True
                except:
                    pass

                try:
                    X1 = result['X1']
                    posX1 = True
                except:
                    pass

                try:
                    X2 = result['X2']
                    posX2 = True
                except:
                    pass

                try:
                    X3 = result['X3']
                    posX3 = True
                except:
                    pass

                if posX0 != False:
                    # simula con X0 e salva il risultato
                    move = self.align([0, X0], piece)
                    scores.append((move, self.simulate_move(move, piece), self.crest[X0]))
                    print('altezza di ', str(X0), ' = ', str(self.crest[X0]))
                    iFlag = True
                elif posX1 != False:
                    # simula con X1
                    move = self.align([1, X1], piece)
                    scores.append((move, self.simulate_move(move, piece), self.crest[X1]))
                    print('altezza di ', str(X1), ' = ', str(self.crest[X1]))
                elif posX2 != False:
                    # simula con X2
                    move = self.align([2, X2], piece)
                    scores.append((move, self.simulate_move(move, piece), self.crest[X2]))
                    print('altezza di ', str(X2), ' = ', str(self.crest[X2]))
                elif posX3 != False:
                    # simula con X3
                    move = self.align([3, X3], piece)
                    scores.append((move, self.simulate_move(move, piece), self.crest[X3]))
                    print('altezza di ', str(X3), ' = ', str(self.crest[X3]))

        # if piece['shape'] == 'I' and iFlag:
        # minh = 20
        # for x in scores:
        # move, score, h = x
        # print(score)
        # if h < minh:
        # minh = h
        # bestMove = move
        # print(bestMove)
        # return bestMove

        if len(scores) == 0:
            # return [random.randint(0, 1), random.randint(-5, 5)]        #mossa casuale
            # print('dfs')
            return self.get_DFS_move()
        else:
            # print('rule')
            maxScore = -999
            minh = 20
            print(scores)
            for x in scores:
                move, score, h = x
                # print(score)
                if h < minh or maxScore < score:
                    minh = h
                    maxScore = score
                    bestMove = move
            print(bestMove)
            return bestMove

    def get_DFS_move(self):
        best_rot = 0
        best_sideways = 0
        best_score = - 99

        NextScore = (0, 0, -99)  # rot,sideways, score

        # rot =  1-'O':    2-'I': 2-'Z':    4-'J': 4-'L': 4-'T'

        for rot in range(0, len(PIECES[self.falling_piece['shape']])):  # per le rotazioni possibili su lpezzo corrente
            for sideways in range(-5, 6):  # per i drop possibili sulla board
                move = [rot, sideways]  # salvo la coppia corrente
                test_board = copy.deepcopy(self.board)  # duplico la board corrente
                test_piece = copy.deepcopy(self.falling_piece)  # duplico il pezzo corrente
                test_board = simulate_board(test_board, test_piece, move)  # simulo il pezzo e la mossa sulla board test
                # Check NEXT
                if test_board is not None:  # se la simulazione è andata a buon fine
                    ## Chose the best after next                                # effettuo il calcolo con il pezzo successivo
                    for rot2 in range(0, len(PIECES[self.next_piece['shape']])):
                        for sideways2 in range(-5, 6):
                            move2 = [rot2, sideways2]
                            test_board2 = copy.deepcopy(test_board)
                            test_piece2 = copy.deepcopy(self.next_piece)
                            test_board2 = simulate_board(test_board2, test_piece2, move2)
                            if test_board2 is not None:
                                test_score2, nextLines = self.get_expected_score(test_board2)
                                if NextScore[2] < test_score2:
                                    NextScore = [rot2, sideways2, test_score2]  # aggiorno il best local score (LV2)
                    if best_score < NextScore[2]:  # confronto
                        best_score = NextScore[2]  # aggiorno il best local score (LV1+LV2)
                        best_sideways = sideways  # aggiorno il best sideway (LV1)
                        best_rot = rot  # aggiorno il best rot (LV1)

        # finish = time.perf_counter()
        # print(f'Finished in {round(finish - start, 2)} second(s) with full')

        return best_rot, best_sideways, best_score

    def get_heights(self, board):
        heights = [0] * BOARDWIDTH
        # Calculate all tougether to optimize calculation
        for i in range(0, BOARDWIDTH):  # Select a column
            Hflag = False
            for j in range(0, BOARDHEIGHT):  # Search down starting from the top of the board
                if int(board[i][j]) > 0:  # Is the cell occupied?
                    if not Hflag:
                        heights[i] = BOARDHEIGHT - j  # Store the height value
                        Hflag = True
        # print(heights)
        return heights

    def get_Pcrest(self):
        Pcrest = list()
        for x in range(int(len(self.crest))):  # 1
            Pcrest.append((x, [0]))
        for x in range(int(len(self.crest) - 1)):  # 2
            Pcrest.append((x, [0, self.crest[x + 1] - self.crest[x]]))
        for x in range(int(len(self.crest) - 2)):  # 3
            Pcrest.append((x, [0, self.crest[x + 1] - self.crest[x], self.crest[x + 2] - self.crest[x]]))
        for x in range(int(len(self.crest) - 3)):  # 4
            Pcrest.append((x, [0, self.crest[x + 1] - self.crest[x], self.crest[x + 2] - self.crest[x],
                               self.crest[x + 3] - self.crest[x]]))
        return Pcrest

    # get the aligned rotation
    def get_rot(self, rotation):
        pass

    # get the aligned sideway
    def get_sideway(self, x):
        pass

    # write assert on Kb for the crest encoding
    def writePCrest(self, Pcrest):
        self.deletePCrest()
        for elem in Pcrest:
            position, window = elem
            pre = "inCrest(crest, "
            sequence = self.encodeShadow(window)
            if sequence:  # memorizziamo solo le shadow che si possono incastrare con i pezzi
                assertion = pre + sequence + "," + str(position) + ")"
                prolog.assertz(assertion)

    def encodeShadow(self, window):
        str_ = 's'  # in prolog le variabili cominciano per lettera maiuscola o per underscore
        for x in range(len(window)):
            if window[x] == 0:
                str_ += '_0'
            elif window[x] == 1:
                str_ += '_1'
            elif window[x] == 2:
                str_ += '_2'
            elif window[x] == -1:
                str_ += '_m1'
            elif window[x] == -2:
                str_ += '_m2'
            else:
                return False
        return str_

    # delete the previus crest
    def deletePCrest(self):
        prolog.retractall('inCrest(crest, S, X)')


def rb_main(r_p, numOfRun):
    numOfRun = int(numOfRun)
    for x in range(numOfRun):
        rb = RuleBased(r_p)
        newScore, weights = rb.run()
        print("Game achieved a score of: ", newScore)
        print("weights ", weights)
    menu.main()

if __name__ == "__main__":
    # r_p = sys.argv[1]
    # numOfRun = int(sys.argv[2])
    r_p = 'p'
    numOfRun = 1
    for x in range(numOfRun):
        rb = RuleBased(r_p)
        newScore, weights = rb.run()
        print("Game achieved a score of: ", newScore)
        print("weights ", weights)
