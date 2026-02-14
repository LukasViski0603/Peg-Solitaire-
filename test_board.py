# test_board.py
import pytest
from board import Board, PEG, EMPTY

def test_valid_move():
    """Test a valid move: jump from (2,0) to (2,2) over (2,1)"""
    board = Board(size=5)
    
    # Set up: peg at (2,0), peg at (2,1), empty at (2,2)
    board.grid[2][0] = PEG
    board.grid[2][1] = PEG
    board.grid[2][2] = EMPTY
    
    # This should be valid
    assert board.is_valid_move(2, 0, 2, 2) == True
    
    # Apply the move
    assert board.apply_move(2, 0, 2, 2) == True
    
    # Check board state after move
    assert board.grid[2][0] == EMPTY  # source now empty
    assert board.grid[2][1] == EMPTY  # jumped peg removed
    assert board.grid[2][2] == PEG    # destination has peg

def test_invalid_move_distance():
    """Test invalid move: only 1 space instead of 2"""
    board = Board(size=5)
    board.grid[2][0] = PEG
    board.grid[2][1] = EMPTY
    
    # Moving only 1 space is invalid
    assert board.is_valid_move(2, 0, 2, 1) == False

def test_invalid_move_no_peg_to_jump():
    """Test invalid move: no peg in middle to jump over"""
    board = Board(size=5)
    board.grid[2][0] = PEG
    board.grid[2][1] = EMPTY  # no peg to jump!
    board.grid[2][2] = EMPTY
    
    assert board.is_valid_move(2, 0, 2, 2) == False