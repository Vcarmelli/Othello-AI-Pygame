import copy
from pygame.locals import *
from states.othello import Othello
from states.gametree import GameTree
        

class AlphaBeta:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.othello = Othello(display, gameStateManager)

        self.expandLayer = 5
        self.root = GameTree(self.othello.board)
        self.expandTree()
        self.scores = {}


    def run(self):
        while self.othello.RUNNING and not self.othello.check_game_over():
            self.othello.input()
            self.othello.update()
            self.othello.render()
            if self.othello.current_player == -1:
                #print("AI SHOULD MOVE: ", self.othello.current_player)
                row, col = self.findBestMove(self.othello.current_player)
                while True:
                    print("=============================================AI MOVE:", row, col)
                    
                    self.othello.drop_piece(row, col)
                    self.othello.flip_pieces(row, col)
                    self.othello.switch_player()
                    self.othello.game_over = self.othello.check_game_over()
                    self.scores.pop((row, col))
                    row, col = max(self.scores, key=self.scores.get)
                # else:
                #     print("CURR PLAYER inside: ", self.othello.current_player)
                #     print("invalid move")
                #     self.othello.switch_player()
                continue
            print("CURR PLAYER: ", self.othello.current_player)

    def setPiece(self, board, move, player):
        row, col = move
        board_copy = copy.deepcopy(board)
        board_copy[row][col] = player
        return board_copy

    
    def expandTree(self):
        node = self.root
        # expand the first layer
        available_moves = self.othello.get_valid_moves(self.othello.board, self.othello.current_player)
        print("available moves:", available_moves)
        for i, j in available_moves:
            print("(i, j):", (i, j))
            if (i, j) not in node.kids:
                board_new = self.setPiece(self.othello.board, (i, j), self.othello.current_player)
                node_new = GameTree(board_new)
                node.kids[(i, j)] = node_new
                node_new.parent = node
                #node.print_details()
                

    def findBestMove(self, player):
        alpha = -6400
        beta = 6400
        # for key in self.root.kids:
        #     score = self.MaxMin(self.root.kids[key], player,
        #                         self.expandLayer - 1, alpha)
        #     self.scores.update({key: score})
        #     print("scores:", self.scores)
        #     if alpha < score:
        #         alpha = score
        # if not self.scores:
        #     return (-1, -1)
        # max_key = max(self.scores, key=self.scores.get)
        # min_key = min(self.scores, key=self.scores.get)
        # print(self.scores[min_key], self.scores[max_key])

        score, move = self.MaxMin(self.root, player, self.expandLayer, alpha, beta)
        print("findBestMove:", score, "move:", move)
        return move
    


    def MaxMin(self, node, player, layer, alpha, beta):
            valid_moves = self.othello.get_valid_moves(node.board, player)
            if layer == 0 or not valid_moves:
                return node.getScore(), None

            if self.othello.current_player == player:
                # Min layer (opponent's move)
                min_eval = 6400
                for move in valid_moves:
                    if move in node.kids:
                        score, _ = self.MaxMin(node.kids[move], -player, layer - 1, alpha, beta)
                    else:
                        board_new = self.setPiece(node.board, move, player)
                        node_new = GameTree(board_new)
                        node.kids[move] = node_new
                        node_new.parent = node
                        score, _ = self.MaxMin(node_new, -player, layer - 1, alpha, beta)

                    min_eval = min(min_eval, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
                return min_eval
            else:
                # Max layer (AI's move)
                max_eval = -6400
                best_move = None
                for move in valid_moves:
                    if move in node.kids:
                        score, _ = self.MaxMin(node.kids[move], -player, layer - 1, alpha, beta)
                    else:
                        board_new = self.setPiece(node.board, move, player)
                        node_new = GameTree(board_new)
                        node.kids[move] = node_new
                        node_new.parent = node
                        score, _ = self.MaxMin(node_new, -player, layer - 1, alpha, beta)

                    if score > max_eval:
                        max_eval = score
                        best_move = move
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
                return max_eval, best_move


                


        

        


        
