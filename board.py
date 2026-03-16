# board.py

# Constants for cell states
PEG = 1
EMPTY = 0
INVALID = -1

class Board:
    def __init__(self, size=7, board_type="English"):

        self.size = size
        self.board_type = board_type
        self.grid = self._create_grid()
    
    def _create_grid(self):
        """Create board grid based on board type."""
        if self.board_type == "English":
            return self._create_english_board()
        else:
            # Placeholder
            raise NotImplementedError(f"{self.board_type} board not yet implemented")
    
    def _create_english_board(self):
        """Create English (cross-shaped) board.
        
            X X O O O X X
            X X O O O X X
            O O O O O O O
            O O O E O O O 
            O O O O O O O
            X X O O O X X
            X X O O O X X
        """
        grid = []
        
        for row in range(self.size):
            grid.append([])
            for col in range(self.size):
                # Determine if position is on the board (valid)
                if self._is_valid_position(row, col):
                    grid[row].append(PEG)
                else:
                    grid[row].append(INVALID)
        
        # Set center to empty
        center = self.size // 2
        grid[center][center] = EMPTY
        
        return grid
    
    def _is_valid_position(self, row, col):
        """Check if a position is on the English board (not in corners)."""
        # For 7x7 English board, corners are invalid
        # Top-left and top-right corners (rows 0-1)
        if row < 2 and (col < 2 or col >= self.size - 2):
            return False
        # Bottom-left and bottom-right corners (rows 5-6)
        if row >= self.size - 2 and (col < 2 or col >= self.size - 2):
            return False
        return True
    
    def is_valid_move(self, src_row, src_col, dst_row, dst_col):
        """Check if a move from src to dst is valid."""
        # Check bounds
        if not (0 <= src_row < self.size and 0 <= src_col < self.size):
            return False
        if not (0 <= dst_row < self.size and 0 <= dst_col < self.size):
            return False
        
        # Check positions are on the board
        if self.grid[src_row][src_col] == INVALID:
            return False
        if self.grid[dst_row][dst_col] == INVALID:
            return False
        
        # Source must have a peg
        if self.grid[src_row][src_col] != PEG:
            return False
        
        # Destination must be empty
        if self.grid[dst_row][dst_col] != EMPTY:
            return False
        
        # Calculate distance
        row_diff = dst_row - src_row
        col_diff = dst_col - src_col
        
        # Must move exactly 2 spaces (orthogonal only for English board)
        if abs(row_diff) == 2 and col_diff == 0:  # vertical
            mid_row = src_row + row_diff // 2
            mid_col = src_col
        elif abs(col_diff) == 2 and row_diff == 0:  # horizontal
            mid_row = src_row
            mid_col = src_col + col_diff // 2
        else:
            return False  # not a valid distance/direction
        
        # Middle position must have a peg to jump over
        if self.grid[mid_row][mid_col] != PEG:
            return False
        
        return True
    
    def apply_move(self, src_row, src_col, dst_row, dst_col):
        """Execute a move: remove jumped peg, move the source peg."""
        if not self.is_valid_move(src_row, src_col, dst_row, dst_col):
            return False
        
        # Calculate middle position
        mid_row = (src_row + dst_row) // 2
        mid_col = (src_col + dst_col) // 2
        
        # Execute the move
        self.grid[src_row][src_col] = EMPTY
        self.grid[mid_row][mid_col] = EMPTY
        self.grid[dst_row][dst_col] = PEG
        
        return True
    
    def count_pegs(self):
        """Count remaining pegs on the board."""
        count = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == PEG:
                    count += 1
        return count
    
    def is_game_over(self):
        """Check if no more valid moves are possible."""
        # Try every possible move
        for src_row in range(self.size):
            for src_col in range(self.size):
                if self.grid[src_row][src_col] == PEG:
                    # Try all 4 directions (up, down, left, right)
                    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
                    for dr, dc in directions:
                        dst_row = src_row + dr
                        dst_col = src_col + dc
                        if self.is_valid_move(src_row, src_col, dst_row, dst_col):
                            return False  # Found a valid move
        return True  # No valid moves found
    
    def get_rating(self):
        """Get rating based on number of pegs remaining."""
        pegs = self.count_pegs()
        if pegs == 1:
            return "Outstanding"
        elif pegs == 2:
            return "Very Good"
        elif pegs == 3:
            return "Good"
        else:
            return "Average"