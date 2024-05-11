import tkinter as tk
from OthelloGame import *


class OthelloGUI:
    def __init__(self, master):
        self.game = OthelloGame(self)
        self.master = master
        self.master.title("Othello")
        self.master.geometry("700x675")  # Fixed window size
        self.master.resizable(False, False)
        # Background color
        self.start_window()
        self.master.configure(bg="#2E4053")
        self.center_window(self.master, 700, 675)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x_coordinate = (screen_width - width) // 2
        y_coordinate = (screen_height - height) // 2 - 40

        window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

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
            level_button = tk.Button(self.start_frame, text=level, command=lambda level=level: self.game.set_level(
                level), bg="#3498DB", fg="white", font=("Helvetica", 12))
            level_button.grid(row=2, column=i, padx=20, pady=5)

        tk.Label(self.start_frame, text="Select Your Color", bg="#2E4053", fg="white", font=(
            "Helvetica", 14)).grid(row=3, column=0, columnspan=4, padx=10, pady=5)

        user_color_frame = tk.Frame(self.start_frame, bg="#2E4053")
        user_color_frame.grid(row=4, columnspan=4)

        tk.Button(user_color_frame, width=4, height=2,
                  bg="black", fg="white", font=("Helvetica", 12, "bold"), command=lambda color=1:
                  self.game.set_color(color)).pack(side=tk.LEFT, padx=5)
        tk.Button(user_color_frame, width=4, height=2,
                  bg="white", fg="white", font=("Helvetica", 12, "bold"), command=lambda color=2:
                  self.game.set_color(color)).pack(side=tk.LEFT, padx=5)

        start_game_button = tk.Button(self.start_frame, text="Start Game",
                                      command=lambda: self.start_game_gui(), bg="#27AE60", fg="white", font=("Helvetica", 12))
        start_game_button.grid(row=5, column=0, columnspan=4, pady=10)

    def start_game_gui(self):
        self.start_frame.destroy()
        self.create_board()
        self.create_return_button()
        self.game.start_game()

    def create_board(self):
        self.board_frame = tk.Frame(self.master, bg="#2E4053")
        self.board_frame.pack(pady=50)

        # Create a frame to contain the board and player info
        self.board_container = tk.Frame(self.board_frame, bg="#2E4053")
        self.board_container.pack()

        self.buttons = [
            [None] * self.game.board_size for _ in range(self.game.board_size)]

        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                color = self.game.player_colors.get(
                    self.game.initial_state[row][col], "#45B39D")
                button = tk.Button(self.board_container, width=4, height=2,
                                   bg=color, fg="white", font=("Helvetica", 12, "bold"))
                button.grid(row=row, column=col)
                button.config(command=lambda r=row,
                              c=col: self.game.button_click(r, c))
                self.buttons[row][col] = button

        self.create_player_labels()

        self.game.update_player_counts()
        self.update_player_labels()

    def create_player_labels(self):
        # Create a frame for player info
        self.player_info_frame = tk.Frame(self.board_container, bg="#2E4053")
        self.player_info_frame.grid(
            row=self.game.board_size + 1, columnspan=self.game.board_size, pady=(0, 10))

        # Create circles for player indicators
        player1_circle = tk.Canvas(
            self.player_info_frame, width=30, height=30, bg="#2E4053", highlightthickness=0)
        player1_circle.create_oval(5, 5, 25, 25, fill="#000000")
        player1_circle.grid(
            row=0, column=self.game.board_size // 2 - 1, pady=10, padx=20)

        player2_circle = tk.Canvas(
            self.player_info_frame, width=30, height=30, bg="#2E4053", highlightthickness=0)
        player2_circle.create_oval(5, 5, 25, 25, fill="#FFFFFF")
        player2_circle.grid(
            row=0, column=self.game.board_size // 2, pady=10, padx=20)

        # Create labels for player numbers
        self.player1_label = tk.Label(self.player_info_frame,
                                      bg="#2E4053", fg="#EAECEE", font=("Helvetica", 12))
        self.player1_label.grid(
            row=1, column=self.game.board_size // 2 - 1, pady=5, padx=10)

        self.player2_label = tk.Label(self.player_info_frame,
                                      bg="#2E4053", fg="#EAECEE", font=("Helvetica", 12))
        self.player2_label.grid(
            row=1, column=self.game.board_size // 2, pady=5, padx=10)

    def update_board_gui(self):
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                current_cell = self.game.initial_state[row][col]
                color = self.game.player_colors.get(current_cell, "#45B39D")
                self.buttons[row][col].config(state='normal', bg=color)
                if current_cell != 3:
                    self.buttons[row][col].config(state="disabled")

    def update_player_labels(self):
        self.black_player = "You" if self.game.user_color == 1 else "A.I."
        self.white_player = "You" if self.game.user_color == 2 else "A.I."
        # Update player 1 label
        self.player1_label.config(
            text=f"{self.black_player}: {self.game.player_counts[1]}")

        # Update player 2 label
        self.player2_label.config(
            text=f"{self.white_player}: {self.game.player_counts[2]}")

    def create_return_button(self):
        return_button = tk.Button(self.board_frame, text="Return to Main Menu",
                                  command=self.return_to_main, bg="#C0392B", fg="white", font=("Helvetica", 12))
        return_button.pack(side=tk.BOTTOM, pady=10)

    def return_to_main(self):
        self.game.reset_game()
        if hasattr(self, "player_info_frame"):
            self.player_info_frame.destroy()  # Destroy the player info frame if it exists
        self.board_frame.destroy()
        self.start_window()

    def display_winner_window(self, winner):
        winner_window = tk.Toplevel(self.master)
        winner_window.title("Winner")
        winner_window.geometry("300x200")
        winner_window.configure(bg="#2E4053")
        self.center_window(winner_window, 300, 200)
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
        self.game.reset_game()
        self.master.destroy()
        main()

    def exit_game(self):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = OthelloGUI(root)
    root.mainloop()
