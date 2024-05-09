from PossibleMovesIndicator import mark_possible_moves


class AlphaBetaAI:

    def __init__(self, difficulty, color):
        self.difficulty = difficulty
        self.color = color

    def get_next_move(self, board):
        if self.difficulty == "easy":
            return self.easy_mode(board)
        elif self.difficulty == "medium":
            return self.medium_mode(board)
        elif self.difficulty == "hard":
            return self.hard_mode(board)
        else:
            print("Invalid difficulty level")

    def easy_mode(self, board):
        print("Easy")
        print(self.color)
        print(board)
        pass

    def medium_mode(self, board):
        print("Medium")
        print(self.color)
        print(board)
        pass

    def hard_mode(self, board):
        print("Hard")
        print(self.color)
        print(board)
        pass
