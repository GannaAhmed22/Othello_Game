import tkinter as tk
from AlphaBetaAlgorithm import *


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
        self.start_window()
        self.ai = AlphaBetaAI("", 0)
        self.initial_state = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
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

    def create_board(self):
        self.board_frame = tk.Frame(self.master, bg="#2E4053")
        self.board_frame.pack(pady=50)

        # Create a frame to contain the board and player info
        board_container = tk.Frame(self.board_frame, bg="#2E4053")
        board_container.pack()

        self.board_size = 8
        self.buttons = [
            [None] * self.board_size for _ in range(self.board_size)]
        self.current_player = 1 if self.user_color == 1 else 2
        # Black and white colors for players
        self.player_colors = {1: "#000000", 2: "#FFFFFF"}

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
                if self.initial_state[row][col] != 0:
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
        # Update the color of the square based on the current player
        color = self.player_colors[self.current_player]
        self.buttons[row][col].config(bg=color, state="disabled")
        self.initial_state[row][col] = self.current_player

        # Update player counts
        self.update_player_counts()

        # Check for a winner
        winner = self.check_winner()
        if winner:
            self.display_winner_window(winner)
        else:
            # Switch to the next player
            self.current_player = 2 if self.current_player == 1 else 1

            # Update player labels with the new counts
            self.update_player_labels()

        # Get the next computer move based on the current state
        self.ai.get_next_move(self.initial_state)

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
                color = self.buttons[row][col].cget('bg')
                if color == self.player_colors[1]:
                    self.player_counts[1] += 1
                elif color == self.player_colors[2]:
                    self.player_counts[2] += 1

    def update_player_labels(self):
        # Update player 1 label
        self.player1_label.config(text=f"{self.player_counts[1]}")

        # Update player 2 label
        self.player2_label.config(text=f"{self.player_counts[2]}")

    def check_winner(self):
        if sum(self.player_counts.values()) == self.board_size ** 2:
            if self.player_counts[1] > self.player_counts[2]:
                return "Player 1"
            elif self.player_counts[1] < self.player_counts[2]:
                return "Player 2"
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

        winner_label = tk.Label(winner_window, text=f"{winner} wins!",
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


def main():
    root = tk.Tk()
    app = OthelloGUI(root)
    root.mainloop()
