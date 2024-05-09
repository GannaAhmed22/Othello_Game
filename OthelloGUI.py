import tkinter as tk
from AlphaBetaAlgorithm import *
from PossibleMovesIndicator import *

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = (screen_width - width) // 2
    y_coordinate = (screen_height - height) // 2 - 40

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


class OthelloGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Othello")
        self.master.geometry("700x675")  # Fixed window size
        self.master.resizable(False, False)
        self.master.configure(bg="#2E4053")  # Background color
        center_window(self.master, 700, 675)
        self.player_counts = {1: 2, 2: 2}  # Initial counts (2 for each player)
        self.player_pieces = {1: 32, 2: 32}
        self.no_possible_moves = False
        self.start_window()
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

    def start_window(self):
        self.start_frame = tk.Frame(self.master, bg="#2E4053")
        self.start_frame.pack(pady=100)

        game_title = tk.Label(self.start_frame, text="Othello",
                              bg="#2E4053", fg="#EAECEE", font=("Helvetica", 36, "bold"))
        game_title.grid(row=0, columnspan=4, padx=10, pady=20)

        tk.Label(self.start_frame, text="Select Difficulty Level", bg="#2E4053", fg="white", font=(
            "Helvetica", 14)).grid(row=1, column=0, columnspan=4, padx=10, pady=5)

        levels = ["easy", "medium", "hard"]
        for i, level in enumerate(levels):
            level_button = tk.Button(self.start_frame, text=level, command=lambda level=level: self.set_level(
                level), bg="#3498DB", fg="white", font=("Helvetica", 12))
            level_button.grid(row=2, column=i, padx=20, pady=5)

        tk.Label(self.start_frame, text="Select Your Color", bg="#2E4053", fg="white", font=(
            "Helvetica", 14)).grid(row=3, column=0, columnspan=4, padx=10, pady=5)

        user_color_frame = tk.Frame(self.start_frame, bg="#2E4053")
        user_color_frame.grid(row=4, columnspan=4)

        tk.Button(user_color_frame, width=4, height=2,
                  bg="black", fg="white", font=("Helvetica", 12, "bold"), command=lambda color=1:
                  self.set_color(color)).pack(side=tk.LEFT, padx=5)
        tk.Button(user_color_frame, width=4, height=2,
                  bg="white", fg="white", font=("Helvetica", 12, "bold"), command=lambda color=2:
                  self.set_color(color)).pack(side=tk.LEFT, padx=5)

        start_game_button = tk.Button(self.start_frame, text="Start Game", command=lambda: self.start_game(
            self.level, self.user_color), bg="#27AE60", fg="white", font=("Helvetica", 12))
        start_game_button.grid(row=5, column=0, columnspan=4, pady=10)

    def start_game(self, level, user_color):
        self.start_frame.destroy()
        self.user_color = user_color
        ai_color = 2 if self.user_color == 1 else 1
        # Pass the difficulty to AI algorithms to perform next move
        self.ai = AlphaBetaAI(level, ai_color)
        self.create_board()
        self.create_return_button()
        self.print_board() 

        # make AI start if it was black
        if self.ai.color == 1:
            move = self.ai.get_next_move(self.initial_state) 
            self.update_board(move[0], move[1])

    def create_board(self):
        self.board_frame = tk.Frame(self.master, bg="#2E4053")
        self.board_frame.pack(pady=50)

        # Create a frame to contain the board and player info
        board_container = tk.Frame(self.board_frame, bg="#2E4053")
        board_container.pack()

        self.board_size = 8
        self.buttons = [
            [None] * self.board_size for _ in range(self.board_size)]
        self.current_player = 1 # black plays first
        # Black and white colors for players
        self.player_colors = {1: "#000000", 2: "#FFFFFF", 3: "#C3EFC3"}
        # Add possible moves to the initial state
        self.initial_state = mark_possible_moves(self.initial_state, self.current_player)
        # print(self.initial_state)

        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.player_colors.get(
                    self.initial_state[row][col], "#45B39D")
                button = tk.Button(board_container, width=4, height=2,
                                   bg=color, fg="white", font=("Helvetica", 12, "bold"))
                button.grid(row=row, column=col)
                # Attach click event to each button
                button.config(command=lambda r=row,
                              c=col: self.button_click(r, c))
                self.buttons[row][col] = button
                # Only the possible moves are clickable
                if self.initial_state[row][col] != 3:
                    button.config(state="disabled")

        # Create a frame for player info
        self.player_info_frame = tk.Frame(board_container, bg="#2E4053")
        self.player_info_frame.grid(
            row=self.board_size + 1, columnspan=self.board_size, pady=(0, 10))

        # Create circles for player indicators
        player1_circle = tk.Canvas(
            self.player_info_frame, width=30, height=30, bg="#2E4053", highlightthickness=0)
        player1_circle.create_oval(5, 5, 25, 25, fill="#000000")
        player1_circle.grid(row=0, column=self.board_size // 2 - 1, pady=10)

        player2_circle = tk.Canvas(
            self.player_info_frame, width=30, height=30, bg="#2E4053", highlightthickness=0)
        player2_circle.create_oval(5, 5, 25, 25, fill="#FFFFFF")
        player2_circle.grid(row=0, column=self.board_size // 2, pady=10)

        # Create labels for player numbers
        self.player1_label = tk.Label(self.player_info_frame,
                                      bg="#2E4053", fg="#EAECEE", font=("Helvetica", 12))
        self.player1_label.grid(row=1, column=self.board_size // 2 - 1, pady=5)

        self.player2_label = tk.Label(self.player_info_frame,
                                      bg="#2E4053", fg="#EAECEE", font=("Helvetica", 12))
        self.player2_label.grid(row=1, column=self.board_size // 2, pady=5)

        self.update_player_counts()
        self.update_player_labels()
    
    def button_click(self, row, col):
        # Set user move to the board
        self.update_board(row, col)
       
        # Get AI move and set it to board
        if self.current_player == self.ai.color:
           move = self.ai.get_next_move(self.initial_state) 
           self.update_board(move[0], move[1])

    def update_board(self, row, col):
        color = self.player_colors[self.current_player]
        self.buttons[row][col].config(bg=color, state="disabled")
        self.initial_state[row][col] = self.current_player
        self.player_pieces[self.current_player] -= 1
        
        print("after move: ", self.current_player) 

        # Flip opponent's disks
        self.flip_disks(row, col)

        self.update_player_counts()
        self.update_player_labels()

        winner = self.check_winner()
        if winner :
            print(winner)
            self.display_winner_window(winner)
            return
        else:
            # Switch to the next player
            self.current_player = 2 if self.current_player == 1 else 1

            # mark board with possible moves 
            self.initial_state = mark_possible_moves(self.initial_state, self.current_player)
            print("Possible moves for: ", self.current_player)
            self.print_board()

            if not self.check_possible_moves():
                # in case no possible moves for current player then switch to the next player
                self.current_player = 2 if self.current_player == 1 else 1
                # mark board with possible moves
                self.initial_state = mark_possible_moves(self.initial_state, self.current_player)
                if not self.check_possible_moves():
                    # in case no possible moves for both palyers game is over
                    if self.current_player == self.user_color:
                        self.update_gui()  # Update possible moves for Human in GUI
                    self.no_possible_moves = True
                    winner = self.check_winner()
                    if winner:
                      print(winner)
                      self.display_winner_window(winner)
                      return

                if self.current_player == self.ai.color:
                   move = self.ai.get_next_move(self.initial_state)  
                   self.update_board(move[0], move[1])
            
            # Update possible moves for Human in GUI
            if self.current_player == self.user_color:
                self.update_gui()

    def update_gui(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                current_cell = self.initial_state[row][col]
                color = self.player_colors.get(current_cell, "#45B39D")
                self.buttons[row][col].config(state='normal', bg=color)
                if current_cell != 3:
                    self.buttons[row][col].config(state="disabled")

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
        self.print_board()

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
                   
    def create_return_button(self):
        return_button = tk.Button(self.board_frame, text="Return to Main Menu",
                                  command=self.return_to_main, bg="#C0392B", fg="white", font=("Helvetica", 12))
        return_button.pack(side=tk.BOTTOM, pady=10)

    def return_to_main(self):
        if hasattr(self, "player_info_frame"):
            self.player_info_frame.destroy()  # Destroy the player info frame if it exists
        self.board_frame.destroy()
        self.start_window()

    def update_player_counts(self):
        # Reset counts
        self.player_counts = {1: 0, 2: 0}

        # Count the number of discs of each color on the board
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = self.initial_state[row][col]
                if color == 1:
                    self.player_counts[1] += 1
                elif color == 2:
                    self.player_counts[2] += 1

    def update_player_labels(self):
        # Update player 1 label
        self.player1_label.config(text=f"{self.player_counts[1]}")

        # Update player 2 label
        self.player2_label.config(text=f"{self.player_counts[2]}")

    def check_winner(self): 
        if self.no_possible_moves or self.player_pieces[1] == 0 or self.player_pieces[1] == 0 or sum(self.player_counts.values()) == self.board_size ** 2:
            if self.player_counts[1] > self.player_counts[2]:
                return "Player 1 wins!"
            elif self.player_counts[1] < self.player_counts[2]:
                return "Player 2 wins!"
            else:
                return "It's a tie"
        return None

    def display_winner_window(self, winner):
        winner_window = tk.Toplevel(self.master)
        winner_window.title("Winner")
        winner_window.geometry("300x200")
        winner_window.configure(bg="#2E4053")
        center_window(winner_window, 300, 200)
        winner_window.resizable(False, False)

        winner_label = tk.Label(winner_window, text=f"{winner}",
                                bg="#2E4053", fg="#EAECEE", font=("Helvetica", 20))
        winner_label.pack(pady=20)

        play_again_button = tk.Button(winner_window, text="Play Again",
                                      command=self.play_again, bg="#3498DB", fg="white", font=("Helvetica", 12))
        play_again_button.pack(pady=10)

        exit_button = tk.Button(winner_window, text="Exit",
                                command=self.exit_game, bg="#C0392B", fg="white", font=("Helvetica", 12))
        exit_button.pack(pady=10)

    def play_again(self):
        self.master.destroy()
        main()

    def exit_game(self):
        self.master.destroy()
    
    # only for debug
    def print_board(self):
        for row in self.initial_state:
            print(row)
        print()

def main():
    root = tk.Tk()
    app = OthelloGUI(root)
    root.mainloop()
