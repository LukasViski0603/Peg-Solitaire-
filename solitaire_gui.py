import tkinter as tk
from tkinter import messagebox
from board import EnglishBoard, HexagonBoard, ManualGame, AutomatedGame, GameRecorder, PEG, EMPTY, INVALID

class SolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.root.geometry("600x750")

        self.game = None
        self.selected_cell = None
        self.cell_size = 60
        self.autoplay_active = False
        self.replay_events = []
        self.replay_index = 0

        self._create_controls()
        self._create_board_canvas()

    def _create_controls(self):
        control_frame = tk.Frame(self.root, bg="#2c3e50", pady=15)
        control_frame.pack(fill=tk.X)

        tk.Label(control_frame, text="Board size:", bg="#2c3e50", fg="white",
                 font=("Arial", 11)).pack(side=tk.LEFT, padx=10)
        self.size_var = tk.StringVar(value="7")
        tk.Entry(control_frame, textvariable=self.size_var, width=5,
                 font=("Arial", 11)).pack(side=tk.LEFT, padx=5)

        tk.Label(control_frame, text="Board Type:", bg="#2c3e50", fg="white",
                 font=("Arial", 11)).pack(side=tk.LEFT, padx=10)
        self.board_type_var = tk.StringVar(value="English")
        tk.Radiobutton(control_frame, text="English", variable=self.board_type_var,
                       value="English", bg="#2c3e50", fg="white",
                       selectcolor="#34495e", font=("Arial", 10)).pack(side=tk.LEFT, padx=3)
        tk.Radiobutton(control_frame, text="Hexagon", variable=self.board_type_var,
                       value="Hexagon", bg="#2c3e50", fg="white",
                       selectcolor="#34495e", font=("Arial", 10)).pack(side=tk.LEFT, padx=3)

        tk.Button(control_frame, text="New Game", command=self.new_game,
                  bg="white", fg="black", font=("Arial", 12, "bold"),
                  padx=15, pady=5, relief=tk.RAISED, bd=3).pack(side=tk.LEFT, padx=20)

        self.record_var = tk.BooleanVar(value=False)
        tk.Checkbutton(control_frame, text="Record game", variable=self.record_var,
                       bg="#2c3e50", fg="white", selectcolor="#34495e",
                       font=("Arial", 10)).pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(self.root, text="Click 'New Game' to start",
                                     font=("Arial", 12, "bold"), fg="#2980b9", bg="white")
        self.status_label.pack(pady=5)

        btn_frame = tk.Frame(self.root, bg="white")
        btn_frame.pack()

        self.autoplay_btn = tk.Button(btn_frame, text="Autoplay", command=self.toggle_autoplay,
                                      bg="white", fg="black", font=("Arial", 11, "bold"),
                                      padx=10, pady=5, relief=tk.RAISED, bd=2)
        self.autoplay_btn.pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Randomize", command=self.randomize_board,
                  bg="white", fg="black", font=("Arial", 11, "bold"),
                  padx=10, pady=5, relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Replay", command=self.start_replay,
                  bg="white", fg="black", font=("Arial", 11, "bold"),
                  padx=10, pady=5, relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=10)

    def _create_board_canvas(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def new_game(self):
        self.autoplay_active = False
        self.autoplay_btn.config(text="Autoplay")

        try:
            size = int(self.size_var.get())
            if size < 5 or size > 11:
                messagebox.showerror("Invalid Size", "Board size must be between 5 and 11")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid number")
            return

        board_type = self.board_type_var.get()
        board = EnglishBoard(size) if board_type == "English" else HexagonBoard(size)
        self.game = ManualGame(board)
        self.selected_cell = None

        if self.record_var.get():
            recorder = GameRecorder()
            recorder.record_header(board_type, size)
            self.game.set_recorder(recorder)
            self.status_label.config(text=f"Recording! Pegs: {self.game.count_pegs()}", fg="red")
        else:
            self.status_label.config(text=f"Game started! Pegs: {self.game.count_pegs()}", fg="#2980b9")

        self.draw_board()

    def toggle_autoplay(self):
        if self.game is None:
            return

        if self.autoplay_active:
            self.autoplay_active = False
            self.autoplay_btn.config(text="Autoplay")
            return

        self.autoplay_active = True
        self.autoplay_btn.config(text="Stop")

        recorder = self.game.recorder if self.game else None
        self.game = AutomatedGame(self.game.board)
        if recorder:
            self.game.set_recorder(recorder)

        self._autoplay_step()

    def _autoplay_step(self):
        if not self.autoplay_active or self.game is None:
            return

        if self.game.is_over():
            self.autoplay_active = False
            self.autoplay_btn.config(text="Autoplay")
            self.draw_board()
            self.show_game_over()
            return

        self.game.make_move()
        self.draw_board()
        self.status_label.config(text=f"Autoplay... Pegs: {self.game.count_pegs()}", fg="#8e44ad")
        self.root.after(500, self._autoplay_step)

    def randomize_board(self):
        if self.game is None or not isinstance(self.game, ManualGame):
            return
        self.game.randomize()
        self.selected_cell = None
        self.status_label.config(text=f"Randomized! Pegs: {self.game.count_pegs()}", fg="#e67e22")
        self.draw_board()

    def start_replay(self):
        try:
            recorder = GameRecorder()
            board_type, size, events = recorder.load()
        except FileNotFoundError:
            messagebox.showerror("No Recording", "No recorded game found. Record a game first.")
            return

        board = EnglishBoard(size) if board_type == "English" else HexagonBoard(size)
        self.game = ManualGame(board)
        self.selected_cell = None
        self.autoplay_active = False
        self.replay_events = events
        self.replay_index = 0
        self.draw_board()
        self.status_label.config(text="Replaying...", fg="#27ae60")
        self.root.after(600, self._replay_step)

    def _replay_step(self):
        if self.replay_index >= len(self.replay_events):
            self.status_label.config(text=f"Replay done! Pegs: {self.game.count_pegs()}", fg="#27ae60")
            self.show_game_over()
            return

        event = self.replay_events[self.replay_index]
        self.replay_index += 1

        if event[0] == "MOVE":
            _, src_row, src_col, dst_row, dst_col = event
            self.game.board.apply_move(src_row, src_col, dst_row, dst_col)
        elif event[0] == "RANDOMIZE":
            cells = event[1]
            idx = 0
            for row in range(self.game.board.size):
                for col in range(self.game.board.size):
                    self.game.board.set_cell(row, col, cells[idx])
                    idx += 1

        self.draw_board()
        self.status_label.config(text=f"Replaying... Pegs: {self.game.count_pegs()}", fg="#27ae60")
        self.root.after(600, self._replay_step)

    def draw_board(self):
        self.canvas.delete("all")
        if self.game is None:
            return

        board = self.game.board
        size = board.size
        offset = 50

        for row in range(size):
            for col in range(size):
                x = offset + col * self.cell_size
                y = offset + row * self.cell_size
                cell = board.get_cell(row, col)

                if cell == INVALID:
                    continue
                elif cell == EMPTY:
                    self.canvas.create_oval(x + 10, y + 10, x + 50, y + 50,
                                            fill="lightgray", outline="gray", width=2)
                elif cell == PEG:
                    color = "orange" if self.selected_cell == (row, col) else "brown"
                    self.canvas.create_oval(x + 10, y + 10, x + 50, y + 50,
                                            fill=color, outline="black", width=2)

    def on_canvas_click(self, event):
        if self.game is None or self.autoplay_active:
            return
        if not isinstance(self.game, ManualGame):
            return

        offset = 50
        col = (event.x - offset) // self.cell_size
        row = (event.y - offset) // self.cell_size

        board = self.game.board
        if not (0 <= row < board.size and 0 <= col < board.size):
            return
        if board.get_cell(row, col) == INVALID:
            return

        if self.selected_cell is None:
            if board.get_cell(row, col) == PEG:
                self.selected_cell = (row, col)
                self.draw_board()
        else:
            src_row, src_col = self.selected_cell
            if (row, col) == self.selected_cell:
                self.selected_cell = None
                self.draw_board()
            elif self.game.make_move(src_row, src_col, row, col):
                self.selected_cell = None
                pegs = self.game.count_pegs()
                self.status_label.config(text=f"Move made! Pegs: {pegs}", fg="#2980b9")
                self.draw_board()
                if self.game.is_over():
                    self.show_game_over()
            else:
                self.status_label.config(text="Invalid move! Try again.", fg="red")
                self.selected_cell = None
                self.draw_board()

    def show_game_over(self):
        rating = self.game.get_rating()
        pegs = self.game.count_pegs()
        messagebox.showinfo("Game Over", f"Game over!\nPegs remaining: {pegs}\nRating: {rating}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireGUI(root)
    root.mainloop()