# board.py

# Constants for cell states
PEG = 1
EMPTY = 0
INVALID = -1

class Board:
    def __init__(self, size=5):
        """Initialize square board for testing."""
        self.size = size
        self.grid = self._create_grid()
    
    def _create_grid(self):
        """Create 5x5 board with center empty."""
        grid = []
        for row in range(self.size):
            grid.append([PEG] * self.size)
        
        # Make center empty (starting position)
        center = self.size // 2
        grid[center][center] = EMPTY
        
        return grid
    
    def is_valid_move(self, src_row, src_col, dst_row, dst_col):
        """Check if a move from src to dst is valid."""
        # Check bounds
        if not (0 <= src_row < self.size and 0 <= src_col < self.size):
            return False
        if not (0 <= dst_row < self.size and 0 <= dst_col < self.size):
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
        
        # Must move exactly 2 spaces (orthogonal or diagonal)
        if abs(row_diff) == 2 and col_diff == 0:  # vertical
            mid_row = src_row + row_diff // 2
            mid_col = src_col
        elif abs(col_diff) == 2 and row_diff == 0:  # horizontal
            mid_row = src_row
            mid_col = src_col + col_diff // 2
        elif abs(row_diff) == 2 and abs(col_diff) == 2:  # diagonal
            mid_row = src_row + row_diff // 2
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