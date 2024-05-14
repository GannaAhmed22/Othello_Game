import math

from PossibleMovesIndicator import mark_possible_moves


class AlphaBetaAI:
    def __init__(self, difficulty, color):
        self.difficulty = difficulty
        self.color = color
        self.depth = self.set_depth(difficulty)
        print(self.depth)

    def set_depth(self, difficulty):
        if difficulty == "easy":
            return 1
        elif difficulty == "medium":
            return 3
        elif difficulty == "hard":
            return 5

    def get_next_move(self, board):
        possible_moves_board = mark_possible_moves(
            board, self.color)  # Get marked possible moves
        if self.color == 1:  # Black player starts first
            return self.alpha_beta_search(possible_moves_board, self.depth, self.color, -math.inf, math.inf)
        else:  # White player's turn
            return self.alpha_beta_search(possible_moves_board, self.depth, self.color, -math.inf, math.inf)



    def max_value(self,board, depth, alpha, beta, color):
            if depth == 0 or self.is_game_over(board):
                return self.utility_function(board, color)
            value = -math.inf
            clone = mark_possible_moves(board, color)
            # print(depth)
            # print("max before move")
            # for row in clone:
            #     print(row)
            # print()
            for move in self.get_valid_moves(clone, color):
                clone = self.make_move(clone, move[0], move[1], color)
                # print("max after move")
                # for row in clone:
                #     print(row)
                # print()

                value = max(value, self.min_value(clone, depth - 1, alpha, beta, 3 - color))
                if value==0:break

                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value



    def min_value(self,board, depth, alpha, beta, color):
            if depth == 0 or self.is_game_over(board):
                return self.utility_function(board, color)
            value = math.inf
            clone = mark_possible_moves(board, color)
            # print(depth)
            # print("min before move")
            # for row in clone:
            #     print(row)
            # print()
            for move in self.get_valid_moves(clone, 3 - color):
                clone = self.make_move(clone, move[0], move[1], color)
                # print("min after move")
                # for row in clone:
                #     print(row)
                # print()
                value = min(value, self.max_value(
                    clone, depth - 1, alpha, beta, 3 - color))
                if value == 0: break
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def get_valid_moves(self,board, color):
        moves = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 3:
                    moves.append((i, j))
        return moves

    def make_move(self,board, row, col, color):
        # Create a new board to avoid modifying the original
        clone = [row[:] for row in board]
        clone[row][col] = color
        opposite_color = 2 if color == 1 else 1
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < len(clone) and 0 <= c < len(clone[0]) and clone[r][c] == opposite_color:
                to_flip = []
                while 0 <= r < len(clone) and 0 <= c < len(clone[0]) and clone[r][c] == opposite_color:
                    to_flip.append((r, c))
                    r += dr
                    c += dc
                    if not (0 <= r < len(clone) and 0 <= c < len(clone[0])):
                        break
                if 0 <= r < len(clone) and 0 <= c < len(clone[0]) and clone[r][c] == color:
                    for flip_r, flip_c in to_flip:
                        clone[flip_r][flip_c] = color
        return clone

    def utility_function(self,board,color):
            score_Current_player = 0
            score_opponent_player = 0
            for row in board:
                for cell in row:
                    if cell == color:
                        score_Current_player += 1
                    elif cell == 3 - color:
                        score_opponent_player += 1

            result=score_Current_player-score_opponent_player
            return result

    def is_game_over(self,board):
        return not any(self.get_valid_moves(board, 1)) and not any(self.get_valid_moves(board, 2))

    def alpha_beta_search(self, board, depth, color, alpha, beta):

        best_move = None
        value = -math.inf if color == self.color else math.inf
        for move in self.get_valid_moves(board, color):

            clone = self.make_move(board, move[0], move[1], color)
            # print("first clone")
            # for row in clone:
            #     print(row)
            # print()
            new_value = self.min_value(clone, depth-1, alpha, beta, 3 - color)
            if color == self.color and new_value > value:
                value = new_value
                best_move = move
                alpha = max(alpha, value)
            elif color != self.color and new_value < value:
                value = new_value
                beta = min(beta, value)
            if alpha >= beta:
                break
        return best_move
