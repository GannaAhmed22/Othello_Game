from AlphaBetaAlgorithm import *
from PossibleMovesIndicator import *


class OthelloGame:
    def __init__(self, gui):
        self.gui = gui
        self.board_size = 8
        self.current_player = 1
        self.player_colors = {1: "#000000", 2: "#FFFFFF", 3: "#C3EFC3"}
        self.player_counts = {1: 2, 2: 2}
        self.player_pieces = {1: 30, 2: 30}
        self.no_possible_moves = False
        self.ai = AlphaBetaAI("", 0)
        self.initial_state = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.user_color = None
        self.level = None

    def set_level(self, level):
        self.level = level

    def set_color(self, color):
        self.user_color = color

    def start_game(self):
        ai_color = 2 if self.user_color == 1 else 1
        self.ai = AlphaBetaAI(self.level, ai_color)
        self.initial_state = mark_possible_moves(self.initial_state, self.current_player)
        # make AI start if it was black
        if self.ai.color == 1:
            self.current_player = self.ai.color
            move = self.ai.get_next_move(self.initial_state)
            self.update_board(move[0], move[1])

        self.gui.update_board_gui()

    def check_winner(self):

        if sum(self.player_counts.values()) == self.board_size ** 2 or self.player_pieces[self.current_player] == 0 or self.no_possible_moves:
            if self.player_counts[1] > self.player_counts[2]:
                return f"{self.gui.black_player} won!"
            elif self.player_counts[1] < self.player_counts[2]:
                return f"{self.gui.white_player} won!"
            else:
                return "It's a tie"
        return None
     
    def update_player_counts(self):
        self.player_counts = {1: 0, 2: 0}
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.initial_state[row][col]
                if color == 1:
                    self.player_counts[1] += 1
                elif color == 2:
                    self.player_counts[2] += 1

    def update_board(self, row, col):
        color = self.player_colors[self.current_player]
        self.gui.buttons[row][col].config(bg=color, state="disabled")
        self.initial_state[row][col] = self.current_player
        self.player_pieces[self.current_player] -= 1

        print("after move: ", self.current_player)

        # Flip opponent's disks
        self.flip_disks(row, col)

        self.update_player_counts()
        self.gui.update_player_labels()

        winner = self.check_winner()
        if winner:
            print(winner)
            self.gui.display_winner_window(winner)
            return
        else:
            # Switch to the next player
            self.current_player = 2 if self.current_player == 1 else 1

            # mark board with possible moves
            self.initial_state = mark_possible_moves(
                self.initial_state, self.current_player)


            if not self.check_possible_moves():
                # in case no possible moves for current player then switch to the next player
                self.current_player = 2 if self.current_player == 1 else 1
                # mark board with possible moves
                self.initial_state = mark_possible_moves(
                    self.initial_state, self.current_player)


                if not self.check_possible_moves():
                    # in case no possible moves for both palyers game is over
                    if self.current_player == self.user_color:
                        self.gui.update_board_gui()  # Update possible moves for Human in GUI
                    self.no_possible_moves = True
                    winner = self.check_winner()
                    if winner:
                        print(winner)
                        self.gui.display_winner_window(winner)
                        return

            # Update possible moves for Human in GUI
            if self.current_player == self.user_color:
                self.gui.update_board_gui()

    def check_possible_moves(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.initial_state[row][col] == 3:
                    return True
        return False

    def flip_disks(self, row, col):
        # up
        if row != 0 and self.initial_state[row-1][col] != self.current_player:
            self.__flip(row, col, -1, False)
        # down
        if row != self.board_size-1 and self.initial_state[row+1][col] != self.current_player:
            self.__flip(row, col, 1, False)
        # right
        if col != self.board_size-1 and self.initial_state[row][col+1] != self.current_player:
            self.__flip(row, col, 1)
        # left
        if col != 0 and self.initial_state[row][col-1] != self.current_player:
            self.__flip(row, col, -1)
       

    def __flip(self, row, col, step, is_horizontal=True):
        is_outflank = False
        j = None
        start = col + step if is_horizontal else row + step
        end = self.board_size if step == 1 else -1
        
        for j in range(start, end, step):
            if is_horizontal:
                current_cell = self.initial_state[row][j]
            else:
                current_cell = self.initial_state[j][col]

            if current_cell == 0 or current_cell == 3:
                break
            if current_cell == self.current_player:
                is_outflank = True
                break

        end = col if is_horizontal else row
        if is_outflank:
            for i in range(j - step, end, -step):
                if is_horizontal:
                    self.initial_state[row][i] = self.current_player
                else:
                    self.initial_state[i][col] = self.current_player

    def button_click(self, row, col):
        # Set user move to the board
        self.update_board(row, col)


        while self.current_player == self.ai.color:
            move = self.ai.get_next_move(self.initial_state)
            if (move is None) or self.no_possible_moves or (self.check_winner() is not None):
                break
            self.update_board(move[0], move[1])

    def reset_game(self):
        self.board_size = 8
        self.current_player = 1
        self.player_colors = {1: "#000000", 2: "#FFFFFF", 3: "#C3EFC3"}
        self.player_counts = {1: 2, 2: 2}
        self.player_pieces = {1: 30, 2: 30}
        self.no_possible_moves = False
        self.ai = AlphaBetaAI("", 0)
        self.initial_state = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.user_color = None
        self.level = None
        self.gui.update_player_labels()

    def print_board(self):
        for row in self.initial_state:
            print(row)
        print()
