import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.is_ai = True  # Set to True to play against AI
        self.score_x = 0
        self.score_o = 0

        # Create buttons for the board
        self.buttons = [tk.Button(master, text=" ", font='Arial 20', width=5, height=2,
                                   bg="lightblue", command=lambda i=i: self.player_move(i)) for i in range(9)]
        self.create_board()

        # Add a reset button
        self.reset_button = tk.Button(master, text="Reiniciar Juego", font='Arial 14', command=self.reset_game)
        self.reset_button.grid(row=3, columnspan=3)

        # Score labels
        self.score_label = tk.Label(master, text=f"X: {self.score_x}  O: {self.score_o}", font='Arial 14')
        self.score_label.grid(row=4, columnspan=3)

    def create_board(self):
        """Create the game board layout."""
        for i, button in enumerate(self.buttons):
            button.grid(row=i // 3, column=i % 3)

    def player_move(self, index):
        """Handle player's move."""
        if self.board[index] == " ":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner(self.current_player):
                messagebox.showinfo("Ganador", f"¡El jugador {self.current_player} ha ganado!")
                if self.current_player == "X":
                    self.score_x += 1
                else:
                    self.score_o += 1
                self.update_score()
                self.reset_game()
            elif " " not in self.board:
                messagebox.showinfo("Empate", "¡Es un empate!")
                self.reset_game()
            else:
                # If AI mode is enabled, make AI move
                if self.is_ai and self.current_player == "X":
                    self.current_player = "O"
                    self.ai_move()

    def ai_move(self):
        """AI makes a move using the minimax algorithm."""
        index = self.minimax(self.board, "O")["index"]
        if index is not None:
            self.board[index] = "O"
            self.buttons[index].config(text="O")
            if self.check_winner("O"):
                messagebox.showinfo("Ganador", "¡La IA ha ganado!")
                self.score_o += 1
                self.update_score()
                self.reset_game()
            elif " " not in self.board:
                messagebox.showinfo("Empate", "¡Es un empate!")
                self.reset_game()
            else:
                # Switch back to player X after AI move
                self.current_player = "X"

    def check_winner(self, player):
        """Check if the given player has won."""
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        return any(all(self.board[i] == player for i in combo) for combo in winning_combinations)

    def minimax(self, board, player):
        """Minimax algorithm to determine the best move for the AI."""
        if self.check_winner("O"):
            return {"score": 1}
        elif self.check_winner("X"):
            return {"score": -1}
        elif " " not in board:
            return {"score": 0}

        moves = []
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score = self.minimax(board, "X" if player == "O" else "O")["score"]
                board[i] = " "
                moves.append({"index": i, "score": score})

        best_move = max(moves, key=lambda x: x["score"]) if player == "O" else min(moves, key=lambda x: x["score"])
        
        return best_move

    def reset_game(self):
        """Reset the game board."""
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ")
        # Reset current player to X after reset
        self.current_player = "X"

    def update_score(self):
        """Update the score display."""
        self.score_label.config(text=f"X: {self.score_x}  O: {self.score_o}")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()