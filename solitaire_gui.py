# solitaire_gui.py
import tkinter as tk
from tkinter import messagebox
from board import Board, PEG, EMPTY, INVALID

class SolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.root.geometry("600x700")
        
        self.board = None
        self.selected_cell = None  # (row, col) of selected peg
        self.cell_size = 60  # Size of each cell in pixels
        
        self._create_controls()
        self._create_board_canvas()
    

    def _create_controls(self):
        """Create the control panel (top of window)."""
        control_frame = tk.Frame(self.root, bg="#2c3e50", pady=15)
        control_frame.pack(fill=tk.X)
        
        # Board size
        tk.Label(control_frame, text="Board size:", bg="#2c3e50", fg="white", 
                font=("Arial", 11)).pack(side=tk.LEFT, padx=10)
        self.size_var = tk.StringVar(value="7")
        size_entry = tk.Entry(control_frame, textvariable=self.size_var, width=5,
                            font=("Arial", 11))
        size_entry.pack(side=tk.LEFT, padx=5)
        
        # Board type
        tk.Label(control_frame, text="Board Type:", bg="#2c3e50", fg="white",
                font=("Arial", 11)).pack(side=tk.LEFT, padx=20)
        self.board_type_var = tk.StringVar(value="English")
        
        tk.Radiobutton(control_frame, text="English", variable=self.board_type_var, 
                    value="English", bg="#2c3e50", fg="white", 
                    selectcolor="#34495e", font=("Arial", 10)).pack(side=tk.LEFT, padx=3)
        tk.Radiobutton(control_frame, text="Hexagon", variable=self.board_type_var, 
                    value="Hexagon", bg="#2c3e50", fg="white",
                    selectcolor="#34495e", font=("Arial", 10)).pack(side=tk.LEFT, padx=3)
        tk.Radiobutton(control_frame, text="Diamond", variable=self.board_type_var, 
                    value="Diamond", bg="#2c3e50", fg="white",
                    selectcolor="#34495e", font=("Arial", 10)).pack(side=tk.LEFT, padx=3)
        
        # New Game button - much more visible
        tk.Button(control_frame, text="New Game", command=self.new_game,
                bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                padx=15, pady=5, relief=tk.RAISED, bd=3).pack(side=tk.LEFT, padx=20)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Click 'New Game' to start", 
                                    font=("Arial", 12, "bold"), fg="#2980b9", bg="white")
        self.status_label.pack(pady=10)
        
    def _create_board_canvas(self):
        """Create the canvas for drawing the board."""
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack(pady=20)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
    def new_game(self):
        """Start a new game with selected settings."""
        try:
            size = int(self.size_var.get())
            if size < 5 or size > 11:
                messagebox.showerror("Invalid Size", "Board size must be between 5 and 11")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for board size")
            return
        
        board_type = self.board_type_var.get()
        
        # Check if board type is implemented
        if board_type != "English":
            messagebox.showinfo("Not Implemented", 
                              f"{board_type} board is not yet implemented. Using English board.")
            board_type = "English"
            self.board_type_var.set("English")
        
        # Create the board
        self.board = Board(size=size, board_type=board_type)
        self.selected_cell = None
        self.status_label.config(text=f"Game started! Pegs remaining: {self.board.count_pegs()}")
        
        # Draw the board
        self.draw_board()
        
    def draw_board(self):
        """Draw the current board state on canvas."""
        self.canvas.delete("all")  # Clear canvas
        
        if self.board is None:
            return
        
        size = self.board.size
        offset = 50  # Margin from canvas edge
        
        for row in range(size):
            for col in range(size):
                x = offset + col * self.cell_size
                y = offset + row * self.cell_size
                
                cell_state = self.board.grid[row][col]
                
                if cell_state == INVALID:
                    # Don't draw anything for invalid positions
                    continue
                elif cell_state == EMPTY:
                    # Draw empty hole (light gray circle)
                    self.canvas.create_oval(x + 10, y + 10, x + 50, y + 50, 
                                           fill="lightgray", outline="gray", width=2)
                elif cell_state == PEG:
                    # Draw peg (brown circle)
                    color = "orange" if self.selected_cell == (row, col) else "brown"
                    self.canvas.create_oval(x + 10, y + 10, x + 50, y + 50, 
                                           fill=color, outline="black", width=2)
    
    def on_canvas_click(self, event):
        """Handle mouse click on canvas."""
        if self.board is None:
            return
        
        # Convert click coordinates to board position
        offset = 50
        col = (event.x - offset) // self.cell_size
        row = (event.y - offset) // self.cell_size
        
        # Check if click is within board bounds
        if not (0 <= row < self.board.size and 0 <= col < self.board.size):
            return
        
        # Check if position is valid
        if self.board.grid[row][col] == INVALID:
            return
        
        # Handle click
        if self.selected_cell is None:
            # First click - select a peg
            if self.board.grid[row][col] == PEG:
                self.selected_cell = (row, col)
                self.status_label.config(text=f"Peg selected at ({row}, {col}). Click destination.")
                self.draw_board()  # Redraw to highlight selected peg
        else:
            # Second click - try to move
            src_row, src_col = self.selected_cell
            
            if (row, col) == self.selected_cell:
                # Clicked same peg - deselect
                self.selected_cell = None
                self.status_label.config(text=f"Peg deselected. Pegs remaining: {self.board.count_pegs()}")
                self.draw_board()
            elif self.board.is_valid_move(src_row, src_col, row, col):
                # Valid move - execute it
                self.board.apply_move(src_row, src_col, row, col)
                self.selected_cell = None
                
                pegs = self.board.count_pegs()
                self.status_label.config(text=f"Move successful! Pegs remaining: {pegs}")
                self.draw_board()
                
                # Check if game is over
                if self.board.is_game_over():
                    self.show_game_over()
            else:
                # Invalid move
                self.status_label.config(text="Invalid move! Try again.", fg="red")
                self.selected_cell = None
                self.draw_b

if __name__ == "__main__":
    print("Starting Solitaire GUI...")
    root = tk.Tk()
    print("Window created")
    app = SolitaireGUI(root)
    print("App initialized")
    root.mainloop()
    print("App closed")