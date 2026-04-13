import pytest
import os
from board import EnglishBoard, HexagonBoard, ManualGame, AutomatedGame, GameRecorder, PEG, EMPTY, INVALID


# pytest test_game.py -v

# --- Manual Game Tests ---

def test_english_board_shape():
    board = EnglishBoard(7)
    assert board.get_cell(0, 0) == INVALID
    assert board.get_cell(3, 3) == EMPTY
    assert board.get_cell(3, 0) == PEG

def test_hexagon_board_shape():
    board = HexagonBoard(7)
    assert board.get_cell(0, 0) == INVALID
    assert board.get_cell(3, 3) == EMPTY
    assert board.get_cell(3, 0) == PEG

def test_manual_move_valid():
    board = EnglishBoard(7)
    game = ManualGame(board)
    result = game.make_move(1, 3, 3, 3)
    assert result == True
    assert board.get_cell(1, 3) == EMPTY
    assert board.get_cell(2, 3) == EMPTY
    assert board.get_cell(3, 3) == PEG

def test_manual_move_invalid():
    board = EnglishBoard(7)
    game = ManualGame(board)
    result = game.make_move(0, 3, 0, 4)
    assert result == False

def test_manual_game_over():
    board = EnglishBoard(7)
    game = ManualGame(board)
    for row in range(7):
        for col in range(7):
            if board.get_cell(row, col) == PEG:
                board.set_cell(row, col, EMPTY)
    board.set_cell(2, 2, PEG)
    board.set_cell(2, 6, PEG)
    assert game.is_over() == True

def test_manual_game_not_over_at_start():
    board = EnglishBoard(7)
    game = ManualGame(board)
    assert game.is_over() == False

def test_rating_outstanding():
    board = EnglishBoard(7)
    game = ManualGame(board)
    for row in range(7):
        for col in range(7):
            if board.get_cell(row, col) == PEG:
                board.set_cell(row, col, EMPTY)
    board.set_cell(3, 3, PEG)
    assert game.get_rating() == "Outstanding"

def test_randomize_preserves_peg_count():
    board = EnglishBoard(7)
    game = ManualGame(board)
    count_before = game.count_pegs()
    game.randomize()
    assert game.count_pegs() == count_before

# --- Automated Game Tests ---

def test_automated_move_reduces_pegs():
    board = EnglishBoard(7)
    game = AutomatedGame(board)
    before = game.count_pegs()
    game.make_move()
    assert game.count_pegs() == before - 1

def test_automated_game_runs_to_completion():
    board = EnglishBoard(7)
    game = AutomatedGame(board)
    while not game.is_over():
        game.make_move()
    assert game.is_over() == True

def test_automated_no_move_when_over():
    board = EnglishBoard(7)
    game = AutomatedGame(board)
    for row in range(7):
        for col in range(7):
            if board.get_cell(row, col) == PEG:
                board.set_cell(row, col, EMPTY)
    board.set_cell(3, 3, PEG)
    result = game.make_move()
    assert result == False

# --- Record/Replay Tests ---

def test_record_creates_file():
    board = EnglishBoard(7)
    game = ManualGame(board)
    recorder = GameRecorder("test_record.txt")
    recorder.record_header("English", 7)
    game.set_recorder(recorder)
    game.make_move(1, 3, 3, 3)
    assert os.path.exists("test_record.txt")
    os.remove("test_record.txt")

def test_record_saves_moves():
    board = EnglishBoard(7)
    game = ManualGame(board)
    recorder = GameRecorder("test_record.txt")
    recorder.record_header("English", 7)
    game.set_recorder(recorder)
    game.make_move(1, 3, 3, 3)
    _, _, events = recorder.load()
    assert len(events) == 1
    assert events[0] == ("MOVE", 1, 3, 3, 3)
    os.remove("test_record.txt")

def test_record_saves_randomize():
    board = EnglishBoard(7)
    game = ManualGame(board)
    recorder = GameRecorder("test_record.txt")
    recorder.record_header("English", 7)
    game.set_recorder(recorder)
    game.randomize()
    _, _, events = recorder.load()
    assert len(events) == 1
    assert events[0][0] == "RANDOMIZE"
    os.remove("test_record.txt")

def test_replay_restores_correct_peg_count():
    board = EnglishBoard(7)
    game = ManualGame(board)
    recorder = GameRecorder("test_record.txt")
    recorder.record_header("English", 7)
    game.set_recorder(recorder)
    game.make_move(1, 3, 3, 3)
    game.make_move(4, 3, 2, 3)

    # Replay
    _, size, events = recorder.load()
    replay_board = EnglishBoard(size)
    for event in events:
        if event[0] == "MOVE":
            replay_board.apply_move(event[1], event[2], event[3], event[4])

    assert replay_board.count_pegs() == board.count_pegs()
    os.remove("test_record.txt")

def test_automated_recording():
    board = EnglishBoard(7)
    game = AutomatedGame(board)
    recorder = GameRecorder("test_record.txt")
    recorder.record_header("English", 7)
    game.set_recorder(recorder)
    game.make_move()
    game.make_move()
    _, _, events = recorder.load()
    assert len(events) == 2
    assert all(e[0] == "MOVE" for e in events)
    os.remove("test_record.txt")
