# simple_gui.py
import tkinter as tk
from tkinter import ttk

class SolitaireSettingsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire - Game Settings")
        self.root.geometry("400x400")
        
        # Title text
        title = tk.Label(root, text="Peg Solitaire Settings", 
                        font=("Arial", 18, "bold"))
        title.pack(pady=20)
        
        # Canvas with lines
        canvas = tk.Canvas(root, width=300, height=80, bg="white")
        canvas.pack(pady=10)
        canvas.create_line(20, 40, 280, 40, width=3, fill="blue")
        canvas.create_line(150, 10, 150, 70, width=3, fill="red")
        
        # Board type (radio buttons)
        tk.Label(root, text="Board Type:", font=("Arial", 12)).pack(pady=5)
        
        self.board_type = tk.StringVar(value="English")
        
        radio_frame = tk.Frame(root)
        radio_frame.pack(pady=5)
        
        tk.Radiobutton(radio_frame, text="English", variable=self.board_type, 
                      value="English").pack(anchor=tk.W)
        tk.Radiobutton(radio_frame, text="Hexagon", variable=self.board_type, 
                      value="Hexagon").pack(anchor=tk.W)
        tk.Radiobutton(radio_frame, text="Diamond", variable=self.board_type, 
                      value="Diamond").pack(anchor=tk.W)
        
        # Checkbox
        self.record_game = tk.BooleanVar()
        tk.Checkbutton(root, text="Record game moves", 
                      variable=self.record_game).pack(pady=10)
        
        # Button to show selection
        tk.Button(root, text="Start Game", command=self.show_selection,
                 bg="green", fg="white", font=("Arial", 12)).pack(pady=20)
        
        # Result label
        self.result_label = tk.Label(root, text="", font=("Arial", 10))
        self.result_label.pack(pady=10)
    
    def show_selection(self):
        """Display the selected options"""
        board = self.board_type.get()
        record = "Yes" if self.record_game.get() else "No"
        self.result_label.config(
            text=f"Board: {board} | Recording: {record}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = SolitaireSettingsGUI(root)
    root.mainloop()