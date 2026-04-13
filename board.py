import random

PEG = 1
EMPTY = 0
INVALID = -1

class Board:
    """Base class for all board types."""
    def __init__(self, size=7):
        self.size = size
        self.grid = self._create_grid()

    def _create_grid(self):
        raise NotImplementedError

    def _get_valid_directions(self):
        """Orthogonal moves only by default."""
        return [(-2, 0), (2, 0), (0, -2), (0, 2)]

    def get_cell(self, row, col):
        """Get the state of a cell."""
        return self.grid[row][col]

    def set_cell(self, row, col, value):
        """Set the state of a cell."""
        self.grid[row][col] = value

    def is_valid_move(self, src_row, src_col, dst_row, dst_col):
        if not (0 <= src_row < self.size and 0 <= src_col < self.size):
            return False
        if not (0 <= dst_row < self.size and 0 <= dst_col < self.size):
            return False
        if self.grid[src_row][src_col] != PEG:
            return False
        if self.grid[dst_row][dst_col] != EMPTY:
            return False

        row_diff = dst_row - src_row
        col_diff = dst_col - src_col

        valid_dir = False
        for dr, dc in self._get_valid_directions():
            if row_diff == dr and col_diff == dc:
                valid_dir = True
                break
        if not valid_dir:
            return False

        mid_row = (src_row + dst_row) // 2
        mid_col = (src_col + dst_col) // 2
        if self.grid[mid_row][mid_col] != PEG:
            return False

        return True

    def apply_move(self, src_row, src_col, dst_row, dst_col):
        if not self.is_valid_move(src_row, src_col, dst_row, dst_col):
            return False
        mid_row = (src_row + dst_row) // 2
        mid_col = (src_col + dst_col) // 2
        self.grid[src_row][src_col] = EMPTY
        self.grid[mid_row][mid_col] = EMPTY
        self.grid[dst_row][dst_col] = PEG
        return True

    def count_pegs(self):
        count = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == PEG:
                    count += 1
        return count

    def is_game_over(self):
        for src_row in range(self.size):
            for src_col in range(self.size):
                if self.grid[src_row][src_col] == PEG:
                    for dr, dc in self._get_valid_directions():
                        if self.is_valid_move(src_row, src_col, src_row + dr, src_col + dc):
                            return False
        return True

    def get_rating(self):
        pegs = self.count_pegs()
        if pegs == 1:
            return "Outstanding"
        elif pegs == 2:
            return "Very Good"
        elif pegs == 3:
            return "Good"
        else:
            return "Average"

    def get_all_valid_moves(self):
        moves = []
        for src_row in range(self.size):
            for src_col in range(self.size):
                if self.grid[src_row][src_col] == PEG:
                    for dr, dc in self._get_valid_directions():
                        dst_row = src_row + dr
                        dst_col = src_col + dc
                        if self.is_valid_move(src_row, src_col, dst_row, dst_col):
                            moves.append((src_row, src_col, dst_row, dst_col))
        return moves

    def randomize(self):
        """Randomly redistribute pegs across valid positions."""
        valid_positions = []
        peg_count = 0
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] != INVALID:
                    valid_positions.append((row, col))
                    if self.grid[row][col] == PEG:
                        peg_count += 1
        random.shuffle(valid_positions)
        for i, (row, col) in enumerate(valid_positions):
            self.grid[row][col] = PEG if i < peg_count else EMPTY


class EnglishBoard(Board):
    """Cross-shaped English solitaire board."""
    def __init__(self, size=7):
        super().__init__(size)

    def _create_grid(self):
        grid = []
        for row in range(self.size):
            grid.append([])
            for col in range(self.size):
                if self._is_valid_position(row, col):
                    grid[row].append(PEG)
                else:
                    grid[row].append(INVALID)
        center = self.size // 2
        grid[center][center] = EMPTY
        return grid

    def _is_valid_position(self, row, col):
        if row < 2 and (col < 2 or col >= self.size - 2):
            return False
        if row >= self.size - 2 and (col < 2 or col >= self.size - 2):
            return False
        return True


class HexagonBoard(Board):
    """Diamond-shaped hexagon solitaire board."""
    def __init__(self, size=7):
        super().__init__(size)

    def _create_grid(self):
        grid = []
        for row in range(self.size):
            grid.append([])
            for col in range(self.size):
                if self._is_valid_position(row, col):
                    grid[row].append(PEG)
                else:
                    grid[row].append(INVALID)
        center = self.size // 2
        grid[center][center] = EMPTY
        return grid

    def _is_valid_position(self, row, col):
        center = self.size // 2
        return abs(row - center) + abs(col - center) <= center

    def _get_valid_directions(self):
        """Orthogonal + diagonal moves for hexagon board."""
        return [(-2, 0), (2, 0), (0, -2), (0, 2),
                (-2, -2), (-2, 2), (2, -2), (2, 2)]


class GameRecorder:
    """Records and replays game moves to/from a text file."""

    def __init__(self, filename="game_record.txt"):
        self.filename = filename

    def record_header(self, board_type, size):
        with open(self.filename, "w") as f:
            f.write(f"{board_type},{size}\n")

    def record_move(self, src_row, src_col, dst_row, dst_col):
        with open(self.filename, "a") as f:
            f.write(f"MOVE,{src_row},{src_col},{dst_row},{dst_col}\n")

    def record_randomize(self, grid, size):
        with open(self.filename, "a") as f:
            cells = []
            for row in range(size):
                for col in range(size):
                    cells.append(str(grid[row][col]))
            f.write(f"RANDOMIZE,{','.join(cells)}\n")

    def load(self):
        """Read recorded file, return (board_type, size, events)."""
        with open(self.filename, "r") as f:
            lines = f.read().splitlines()
        parts0 = lines[0].split(",")
        board_type, size = parts0[0], int(parts0[1])
        events = []
        for line in lines[1:]:
            parts = line.split(",")
            if parts[0] == "MOVE":
                events.append(("MOVE", int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])))
            elif parts[0] == "RANDOMIZE":
                cells = list(map(int, parts[1:]))
                events.append(("RANDOMIZE", cells))
        return board_type, size, events


class Game:
    """Base class for game modes."""
    def __init__(self, board):
        self.board = board
        self.recorder = None

    def set_recorder(self, recorder):
        self.recorder = recorder

    def make_move(self, src_row, src_col, dst_row, dst_col):
        return self.board.apply_move(src_row, src_col, dst_row, dst_col)

    def is_over(self):
        return self.board.is_game_over()

    def get_rating(self):
        return self.board.get_rating()

    def count_pegs(self):
        return self.board.count_pegs()


class ManualGame(Game):
    """Human-controlled game mode."""
    def __init__(self, board):
        super().__init__(board)

    def make_move(self, src_row, src_col, dst_row, dst_col):
        result = self.board.apply_move(src_row, src_col, dst_row, dst_col)
        if result and self.recorder:
            self.recorder.record_move(src_row, src_col, dst_row, dst_col)
        return result

    def randomize(self):
        self.board.randomize()
        if self.recorder:
            self.recorder.record_randomize(self.board.grid, self.board.size)


class AutomatedGame(Game):
    """Computer-controlled game mode with random valid moves."""
    def __init__(self, board):
        super().__init__(board)

    def make_move(self, src_row=None, src_col=None, dst_row=None, dst_col=None):
        moves = self.board.get_all_valid_moves()
        if not moves:
            return False
        move = random.choice(moves)
        result = self.board.apply_move(*move)
        if result and self.recorder:
            self.recorder.record_move(*move)
        return result