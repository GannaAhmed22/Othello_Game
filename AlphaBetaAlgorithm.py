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
        possible_moves_board = mark_possible_moves(board, self.color)  # Get marked possible moves
        if self.color == 1:  # Black player starts first
            return self.alpha_beta_search(possible_moves_board, self.depth, self.color)
        else:  # White player's turn
            return self.alpha_beta_search(possible_moves_board, self.depth, self.color)

    def alpha_beta_search(self, board, depth, color):
        def max_value(alpha, beta, depth, color,clone):
            if depth == 0 or is_game_over(clone):
                return utility_function(clone, color)
            value = -math.inf
            clone = mark_possible_moves(clone, color)
            print("1")
            print("_______________")
            print("depth")
            print( depth)
            for move in get_valid_moves(clone, color):
                clone = clone_board(clone)
                for row in clone:
                    print(row)
                print(".....")
                make_move(clone, move[0], move[1], color)
                value = max(value, min_value(alpha, beta, depth - 1, 3-color,clone))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        def min_value(alpha, beta, depth, color,clone):
            if depth == 0 or is_game_over(clone):
                return utility_function(clone, color)
            value = math.inf
            clone = mark_possible_moves(clone,color)
            print("2")
            print("_______________")
            print("depth")
            print( depth)
            for move in get_valid_moves(clone, color):
                clone = clone_board(clone)
                for row in clone:
                    print(row)
                print(".....")
                make_move(clone, move[0], move[1],  color)
                value = min(value, max_value(alpha, beta, depth - 1,3- color,clone))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

        def clone_board(board):
            return [row[:] for row in board]

        def get_valid_moves(board, color):
            moves = []
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if board[i][j] == 3:
                        moves.append((i, j))
            return moves

        def make_move(board, row, col, color):
            board[row][col] = color
            opposite_color = 2 if color == 1 else 1
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opposite_color:
                    to_flip = []
                    while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == opposite_color:
                        to_flip.append((r, c))
                        r += dr
                        c += dc
                        if not (0 <= r < len(board) and 0 <= c < len(board[0])):
                            break
                    if 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == color:
                        for flip_r, flip_c in to_flip:
                            board[flip_r][flip_c] = color
        #utility function -> calculate the value of a terminal state.
        def utility_function(board, color):
            score = 0 
            for row in board:
                for cell in row:
                    if cell == color:
                        score += 1
                    elif cell == 3 - color:
                        score -= 1
            return score

        def is_game_over(board):
            return not any(get_valid_moves(board, 1)) and not any(get_valid_moves(board, 2))

        best_move = None
        alpha = -math.inf
        beta = math.inf
        value = -math.inf
        print("---------------------")
        print("3")

        for move in get_valid_moves(board, color):
            clone = clone_board(board)
            for row in clone:

                print(row)
            make_move(clone, move[0], move[1], color)
            new_value = max_value(alpha, beta, depth , color,clone)
            if new_value > value:
                value = new_value
                best_move = move
        return best_move


