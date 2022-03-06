from ntris import Tetris

board = Tetris.empty_board()
board = Tetris.place_piece(board, 39, 4, "l", 0)
board = Tetris.place_piece(board, 39, 8, "j", 0)
board = Tetris.place_piece(board, 37, 6, "i", 1)
board = Tetris.place_piece(board, 38, 4, "s", 0)
board = Tetris.place_piece(board, 38, 8, "z", 0)
board = Tetris.place_piece(board, 36, 4, "t", 0)
board = Tetris.place_piece(board, 39, 0, "o", 0)
board = Tetris.place_piece(board, 36, 0, "j", 1)
board = Tetris.place_piece(board, 34, 3, "l", 3)
board = Tetris.place_piece(board, 35, 9, "i", 1)
board = Tetris.place_piece(board, 36, 7, "o", 0)

Tetris.pretty_print(board)

moves = Tetris.generate_moves(board, "j")[3]

Tetris.pretty_print(moves)