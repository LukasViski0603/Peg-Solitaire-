# test_solitaire.py
import pytest
from board import Board, PEG, EMPTY, INVALID

def test_english_board_shape():
    """Test that English board has correct cross shape."""
    board = Board(size=7, board_type="English")
    
    # Top-left corner should be invalid
    assert board.grid[0][0] == INVALID
    assert board.grid[0][1] == INVALID
    assert board.grid[1][0] == INVALID
    assert board.grid[1][1] == INVALID
    
    # Center of top edge should be valid (has peg)
    assert board.grid[0][3] == PEG
    
    # Center should be empty
    assert board.grid[3][3] == EMPTY
    
    # Middle row should be all valid (pegs except center)
    assert board.grid[3][0] == PEG
    assert board.grid[3][6] == PEG

def test_valid_move_execution():
    """Test that a valid move updates board correctly."""
    board = Board(size=7, board_type="English")
    
    # Make a move from (1,3) to (3,3) - jump down over (2,3)
    assert board.is_valid_move(1, 3, 3, 3) == True
    result = board.apply_move(1, 3, 3, 3)
    
    assert result == True
    assert board.grid[1][3] == EMPTY  # Source now empty
    assert board.grid[2][3] == EMPTY  # Jumped peg removed
    assert board.grid[3][3] == PEG    # Destination has peg

def test_game_over_detection():
    """Test that game over is correctly detected."""
    board = Board(size=7, board_type="English")
    
    # Fresh board should have valid moves
    assert board.is_game_over() == False
    
    # Create a board with no valid moves (just 2 pegs far apart)
    for row in range(7):
        for col in range(7):
            if board.grid[row][col] == PEG:
                board.grid[row][col] = EMPTY
    
    # Place 2 pegs that can't jump each other
    board.grid[2][2] = PEG
    board.grid[2][6] = PEG
    
    assert board.is_game_over() == True

def test_rating_system():
    """Test all rating levels."""
    board = Board(size=7, board_type="English")
    
    # Clear board
    for row in range(7):
        for col in range(7):
            if board.grid[row][col] == PEG:
                board.grid[row][col] = EMPTY
    
    # Test Outstanding (1 peg)
    board.grid[3][3] = PEG
    assert board.get_rating() == "Outstanding"
    assert board.count_pegs() == 1
    
    # Test Very Good (2 pegs)
    board.grid[3][4] = PEG
    assert board.get_rating() == "Very Good"
    assert board.count_pegs() == 2
    
    # Test Good (3 pegs)
    board.grid[3][5] = PEG
    assert board.get_rating() == "Good"
    assert board.count_pegs() == 3
    
    # Test Average (4+ pegs)
    board.grid[4][3] = PEG
    assert board.get_rating() == "Average"
    assert board.count_pegs() == 4

def test_invalid_move_to_invalid_position():
    """Test that moves to invalid (corner) positions are rejected."""
    board = Board(size=7, board_type="English")
    
    # Try to move to a corner (invalid position)
    assert board.is_valid_move(2, 2, 0, 0) == False

def test_count_pegs_initial():
    """Test initial peg count for English board."""
    board = Board(size=7, board_type="English")
    # English 7x7 has 33 valid positions - 1 empty center = 32 pegs
    assert board.count_pegs() == 32

# ai generated tests: 

def test_multiple_consecutive_moves():
    """Test that multiple valid moves execute correctly in sequence."""
    board = Board(size=7, board_type="English")
    
    initial_pegs = board.count_pegs()
    
    # Move 1: (1,3) to (3,3)
    board.apply_move(1, 3, 3, 3)
    assert board.count_pegs() == initial_pegs - 1
    
    # Move 2: (4,3) to (2,3)
    board.apply_move(4, 3, 2, 3)
    assert board.count_pegs() == initial_pegs - 2
    
    # Move 3: (3,1) to (3,3)
    board.apply_move(3, 1, 3, 3)
    assert board.count_pegs() == initial_pegs - 3
    
    # Verify final board state
    assert board.grid[1][3] == EMPTY
    assert board.grid[4][3] == EMPTY
    assert board.grid[3][1] == EMPTY
    assert board.grid[3][3] == PEG

def test_invalid_move_preserves_board_state():
    """Test that attempting an invalid move does not modify the board."""
    board = Board(size=7, board_type="English")
    
    # Save initial state
    initial_pegs = board.count_pegs()
    initial_grid = [row[:] for row in board.grid]  # Deep copy
    
    # Attempt invalid move (only 1 space instead of 2)
    result = board.apply_move(3, 2, 3, 3)
    
    assert result == False
    assert board.count_pegs() == initial_pegs
    
    # Verify grid is unchanged
    for row in range(7):
        for col in range(7):
            assert board.grid[row][col] == initial_grid[row][col]

        