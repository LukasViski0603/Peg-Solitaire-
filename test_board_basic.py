# test_board_basic.py
from board import Board, PEG, EMPTY, INVALID

def test_english_board_creation():
    """Test that English board is created with correct shape."""
    board = Board(size=7, board_type="English")
    
    # Check corners are invalid
    assert board.grid[0][0] == INVALID
    assert board.grid[0][6] == INVALID
    assert board.grid[6][0] == INVALID
    assert board.grid[6][6] == INVALID
    
    # Check center is empty
    assert board.grid[3][3] == EMPTY
    
    # Check a valid position has a peg
    assert board.grid[3][2] == PEG

def test_count_pegs():
    """Test peg counting."""
    board = Board(size=7, board_type="English")
    # English board 7x7 has 32 pegs initially (33 positions - 1 center)
    assert board.count_pegs() == 32

def test_rating():
    """Test rating system."""
    board = Board(size=7, board_type="English")
    
    # Remove all but 1 peg
    for row in range(7):
        for col in range(7):
            if board.grid[row][col] == PEG:
                board.grid[row][col] = EMPTY
    board.grid[3][3] = PEG
    
    assert board.get_rating() == "Outstanding"
    assert board.count_pegs() == 1

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])