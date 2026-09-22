from square_color import PieceColor, SquareColor

STANDARD_BOARD_SIZE = 8


class BoardOutOfBoundsError(Exception):
    "Raised when specified coordinates are out of bounds for the board"


class Board:
    def __init__(self, board_size: int):
        if board_size <= 0:
            raise ValueError(f"board size {board_size} is not positive")

        self.grid = [
            [SquareColor.EMPTY for i in range(board_size)] for j in range(board_size)
        ]
        self.board_size = board_size
        self.white_count = 0
        self.black_count = 0

    def __repr__(self) -> str:
        result = "~~~Board~~~\n"

        result += "grid:\n"
        for row in self.grid:
            for square in row:
                result += f"{square.value}"
            result += "\n"

        result += f"white count: {self.white_count}\n"
        result += f"black count: {self.black_count}\n"
        result += "~~~~~~~~~~~"
        return result

    def set_all_squares(self, grid: list[list[SquareColor]]) -> None:
        errorMessage = f"grid of invalid size received; board size should be {self.board_size}: {grid}"

        if len(self.grid) != len(grid):
            raise ValueError(errorMessage)
        for i in range(len(grid)):
            if len(self.grid[i]) != len(grid[i]):
                raise ValueError(errorMessage)

        self.white_count = 0
        self.black_count = 0

        for y in range(len(grid)):
            for x in range(len(grid[0])):
                self.grid[y][x] = grid[y][x]
                match grid[y][x]:
                    case SquareColor.WHITE:
                        self.white_count += 1
                    case SquareColor.BLACK:
                        self.black_count += 1
                    case SquareColor.EMPTY:
                        continue

    # Returns true if given coordinates are out of bounds
    def check_bounds(self, x: int, y: int) -> bool:
        return x < 0 or y < 0 or x >= self.board_size or y >= self.board_size

    def check_bounds_and_raise(self, x: int, y: int) -> None:
        if self.check_bounds(x, y):
            raise BoardOutOfBoundsError(f"coordinates X: {x} Y: {y} are not in bounds")

    def place_piece(self, x: int, y: int, piece_color: PieceColor) -> None:
        self.check_bounds_and_raise(x, y)

        if self.grid[y][x] != SquareColor.EMPTY:
            raise ValueError(f"the square at coordinates X: {x} Y: {y} is not empty")

        self.grid[y][x] = piece_color.value
        match piece_color:
            case PieceColor.WHITE:
                self.white_count += 1
            case PieceColor.BLACK:
                self.black_count += 1

    def flip_piece(self, x: int, y: int) -> None:
        self.check_bounds_and_raise(x, y)

        original_color = self.grid[y][x]

        match original_color:
            case SquareColor.EMPTY:
                raise ValueError(f"the square at coordinates X: {x} Y: {y} is empty")
            case SquareColor.WHITE:
                self.grid[y][x] = SquareColor.BLACK
                self.black_count += 1
                self.white_count -= 1
            case SquareColor.BLACK:
                self.grid[y][x] = SquareColor.WHITE
                self.white_count += 1
                self.black_count -= 1

    def play_piece(self, x: int, y: int, piece_color: PieceColor) -> None:
        self.place_piece(x, y, piece_color)

        opponent_color = (
            PieceColor.BLACK if piece_color == PieceColor.WHITE else PieceColor.WHITE
        )
        # Move directions as vectors in the format[x_offset, y_offset]
        directions = [
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
        ]
        pieces_to_flip: list[tuple[int, int]] = []

        for x_move, y_move in directions:
            current_x = x
            current_y = y
            # Possible flips searching in this direction
            candidate_flips: list[tuple[int, int]] = []
            should_flip: bool = False

            while True:
                current_x += x_move
                current_y += y_move

                if self.check_bounds(current_x, current_y):
                    break

                current_square_color = self.grid[current_y][current_x]
                if current_square_color == piece_color.value:
                    should_flip = True
                    break
                elif current_square_color == opponent_color.value:
                    candidate_flips.append((current_x, current_y))
                elif current_square_color == SquareColor.EMPTY:
                    break
                else:
                    raise Exception(
                        f"this branch of play_piece should not execute; X: {x} Y: {y} CURRENT_X: {current_x} CURRENT_Y: {current_y} CURRENT_SQUARE_COLOR: {current_square_color} PIECE_COLOR: {piece_color} OPPONENT_COLOR: {opponent_color}"
                    )

            # Get confirmed flips from this direction
            if should_flip:
                pieces_to_flip.extend(candidate_flips)

        # Flip all pieces confirmed for flipping
        for flip_x, flip_y in pieces_to_flip:
            self.flip_piece(flip_x, flip_y)


def starting_board() -> Board:
    board = Board(STANDARD_BOARD_SIZE)

    # Four starting pieces in the center of the board
    board.place_piece(3, 3, PieceColor.WHITE)
    board.place_piece(4, 4, PieceColor.WHITE)
    board.place_piece(4, 3, PieceColor.BLACK)
    board.place_piece(3, 4, PieceColor.BLACK)

    return board
