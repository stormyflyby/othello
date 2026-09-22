import unittest
from tracemalloc import start

from board import Board, BoardOutOfBoundsError, starting_board
from square_color import PieceColor, SquareColor


# In the expected boards in the tests below, 0 represents an empty cell,
# 1 represents a white piece, and 2 represents a black piece
def to_board_grid(grid: list[list[int]]) -> list[list[SquareColor]]:
    def replace_num(num: int) -> SquareColor:
        match num:
            case 0:
                return SquareColor.EMPTY
            case 1:
                return SquareColor.WHITE
            case 2:
                return SquareColor.BLACK
            case _:
                raise ValueError(f"inappropriate number {num} found in test grid")

    result = []
    for row in grid:
        result.append([replace_num(num) for num in row])

    return result


class TestBoard(unittest.TestCase):
    def test_board_init(self):
        board = Board(8)
        self.assertListEqual(
            board.grid, [[SquareColor.EMPTY for i in range(8)] for j in range(8)]
        )
        self.assertEqual(board.white_count, 0)
        self.assertEqual(board.black_count, 0)

    def test_board_init_large(self):
        board = Board(64)
        self.assertListEqual(
            board.grid, [[SquareColor.EMPTY for i in range(64)] for j in range(64)]
        )
        self.assertEqual(board.white_count, 0)
        self.assertEqual(board.black_count, 0)

    def test_board_init_small(self):
        board = Board(1)
        self.assertListEqual(
            board.grid, [[SquareColor.EMPTY for i in range(1)] for j in range(1)]
        )
        self.assertEqual(board.white_count, 0)
        self.assertEqual(board.black_count, 0)

    def test_board_init_zero(self):
        with self.assertRaises(ValueError):
            _ = Board(0)

    def test_board_init_negative(self):
        with self.assertRaises(ValueError):
            _ = Board(-7)

    def test_board_place_piece(self):
        self.maxDiff = None

        board = Board(8)
        board.place_piece(4, 3, PieceColor.BLACK)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 0)
        self.assertEqual(board.black_count, 1)

        board.place_piece(0, 0, PieceColor.WHITE)
        expected_board = to_board_grid(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 1)
        self.assertEqual(board.black_count, 1)

        board.place_piece(7, 2, PieceColor.WHITE)
        expected_board = to_board_grid(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 2)
        self.assertEqual(board.black_count, 1)

    def test_board_place_piece_out_of_bounds(self):
        board = Board(13)

        with self.assertRaises(BoardOutOfBoundsError):
            board.place_piece(-1, 8, PieceColor.BLACK)

        with self.assertRaises(BoardOutOfBoundsError):
            board.place_piece(3, -10, PieceColor.WHITE)

        with self.assertRaises(BoardOutOfBoundsError):
            board.place_piece(100, 3, PieceColor.BLACK)

        with self.assertRaises(BoardOutOfBoundsError):
            board.place_piece(12, 13, PieceColor.BLACK)

        board.place_piece(12, 12, PieceColor.WHITE)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            ]
        )
        self.assertEqual(board.grid, expected_board)

    def test_board_place_piece_on_piece(self):
        board = Board(4)

        board.place_piece(2, 1, PieceColor.WHITE)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)

        board.place_piece(0, 3, PieceColor.BLACK)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 0],
                [2, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)

        with self.assertRaises(ValueError):
            board.place_piece(2, 1, PieceColor.BLACK)

        with self.assertRaises(ValueError):
            board.place_piece(0, 3, PieceColor.BLACK)

    def test_starting_board(self):
        board = starting_board()
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 2, 0, 0, 0],
                [0, 0, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 2)
        self.assertEqual(board.black_count, 2)

    def test_board_flip_piece(self):
        board = starting_board()
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 2, 0, 0, 0],
                [0, 0, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 2)
        self.assertEqual(board.black_count, 2)

        board.flip_piece(3, 3)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 2, 0, 0, 0],
                [0, 0, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 1)
        self.assertEqual(board.black_count, 3)

        board.flip_piece(4, 4)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 2, 0, 0, 0],
                [0, 0, 0, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 0)
        self.assertEqual(board.black_count, 4)

        board.flip_piece(4, 3)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 2, 2, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 1)
        self.assertEqual(board.black_count, 3)

        with self.assertRaises(BoardOutOfBoundsError):
            board.flip_piece(-1, 6)

    def test_board_play_piece(self):
        board = starting_board()

        board.play_piece(2, 3, PieceColor.BLACK)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 1)
        self.assertEqual(board.black_count, 4)

        board.play_piece(2, 2, PieceColor.WHITE)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 2, 1, 2, 0, 0, 0],
                [0, 0, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 3)
        self.assertEqual(board.black_count, 3)

        board.play_piece(3, 2, PieceColor.BLACK)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 2, 0, 0, 0, 0],
                [0, 0, 2, 2, 2, 0, 0, 0],
                [0, 0, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 2)
        self.assertEqual(board.black_count, 5)

        board.play_piece(2, 4, PieceColor.WHITE)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 2, 0, 0, 0, 0],
                [0, 0, 1, 2, 2, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 5)
        self.assertEqual(board.black_count, 3)

    def test_board_play_piece_corner(self):
        board = starting_board()
        board.set_all_squares(
            to_board_grid(
                [
                    [1, 2, 2, 2, 2, 2, 2, 1],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2],
                    [0, 2, 2, 2, 2, 2, 2, 1],
                ]
            )
        )
        expected_board = to_board_grid(
            [
                [1, 2, 2, 2, 2, 2, 2, 1],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 2, 2],
                [0, 2, 2, 2, 2, 2, 2, 1],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 3)
        self.assertEqual(board.black_count, 60)

        board.play_piece(0, 7, PieceColor.WHITE)
        expected_board = to_board_grid(
            [
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 2, 2, 2, 2, 1, 2],
                [1, 2, 2, 2, 2, 1, 2, 2],
                [1, 2, 2, 2, 1, 2, 2, 2],
                [1, 2, 2, 1, 2, 2, 2, 2],
                [1, 2, 1, 2, 2, 2, 2, 2],
                [1, 1, 2, 2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1, 1, 1, 1],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 22)
        self.assertEqual(board.black_count, 42)

    def test_board_play_piece_no_flip(self):
        board = starting_board()
        board.play_piece(6, 1, PieceColor.WHITE)
        expected_board = to_board_grid(
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 2, 0, 0, 0],
                [0, 0, 0, 2, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        self.assertEqual(board.grid, expected_board)
        self.assertEqual(board.white_count, 3)
        self.assertEqual(board.black_count, 2)

    def test_board_play_piece_out_of_bounds(self):
        board = starting_board()
        with self.assertRaises(BoardOutOfBoundsError):
            board.play_piece(-1, 0, PieceColor.BLACK)

        with self.assertRaises(BoardOutOfBoundsError):
            board.play_piece(3, -4, PieceColor.WHITE)

        with self.assertRaises(BoardOutOfBoundsError):
            board.play_piece(8, 2, PieceColor.WHITE)

        with self.assertRaises(BoardOutOfBoundsError):
            board.play_piece(6, 983, PieceColor.BLACK)


if __name__ == "__main__":
    unittest.main()
