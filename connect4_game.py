"""CSC111 Winter 2021 Final Project

This file is Copyright (c) 2021 An Nguyen-Trinh and Raghav Banka.
"""
from __future__ import annotations

import copy
import numpy as np

SCREEN_SIZE = (700, 700)

ROW = 6
COLUMN = 7

HUMAN_PLAYER = 1
AI_PLAYER = 2

################################################################################
# Representing Connect Four
################################################################################
_FILE_TO_INDEX = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}
INDEX_TO_FILE = {i: f for f, i in _FILE_TO_INDEX.items()}
_RANK_TO_INDEX = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6}
INDEX_TO_RANK = {i: r for r, i in _RANK_TO_INDEX.items()}

_MAX_MOVES = 42


class Connect4Game:
    """A class representing a state of a game of ConnectFour.

    """
    # Private Instance Attributes:
    #   - _board: a two-dimensional representation of a Connect Four board
    #   - _valid_moves: a list of the valid moves of the current player
    #   - _is_player1_active: a boolean representing whether the human player (player 1)
    #       is the current player
    #   - _move_count: the number of moves that have been made in the current game
    #   - _difficulty_level: the difficulty level of this Connect4 game
    _board: np.ndarray
    _valid_moves: list[str]
    _is_player1_active: bool
    _move_count: int
    _difficulty_level: int

    def __init__(self, board: np.ndarray = None,
                 player1_active: bool = True, move_count: int = 0,
                 difficulty_level: int = 3) -> None:
        """Initialize a new Connect 4 game.
        """

        if board is not None:
            self._board = board
        else:
            # Initialize a completely new game
            self._board = np.zeros((ROW, COLUMN))

        self._is_player1_active = player1_active
        self._move_count = move_count
        self._difficulty_level = difficulty_level
        self._valid_moves = []

        self._valid_moves = self.calculate_moves_for_board()

    def get_difficulty_level(self) -> int:
        """Return the difficulty level of this game of Connect4"""
        return self._difficulty_level

    def get_valid_moves(self) -> list[str]:
        """Return a list of the valid moves for the active player."""
        return self._valid_moves

    def make_move(self, move: str) -> None:
        """Make the given Connect 4 move. This instance of Connect 4 will be mutated, and will
        afterwards represent the game state after move is made.

        If move is not a currently valid move, raise a ValueError.
        """
        if move not in self._valid_moves:
            raise ValueError(f'Move "{move}" is not valid')

        self._board = self._board_after_move(move)

        self._is_player1_active = not self._is_player1_active
        self._move_count += 1

        self._valid_moves = self.calculate_moves_for_board()

    def get_move(self, column: int) -> int:
        """Return the open row in the given column, which is a valid move. If the column is full,
        return -1.
        """
        for i in range(ROW - 1, -1, -1):
            if self._board[i][column] == 0:
                return i
        return -1

    def copy_and_make_move(self, move: str) -> Connect4Game:
        """Make the given Connect 4 move in a copy of this Connect4Game, and return that copy.

        If move is not a currently valid move, raise a ValueError.
        """
        if move in self._valid_moves:
            return Connect4Game(board=self._board_after_move(move),
                                player1_active=not self._is_player1_active,
                                move_count=self._move_count + 1)
        raise ValueError(f'Move "{move}" is not valid')

    def is_player1_move(self) -> bool:
        """Return whether the player 1 (the human player) is to move next."""
        return self._is_player1_active

    def get_board(self) -> np.ndarray:
        """ Return the board for the game"""
        return self._board

    def is_draw(self) -> bool:
        """Return whether the game ends in a draw or not"""
        if self._move_count == _MAX_MOVES:
            return True
        else:
            return False

    def has_winner(self, player: int) -> bool:
        """ Return whether the given player has won the game or not.

        Precondition:
        - player == HUMAN_PLAYER or player == AI_PLAYER
        """
        # Check horizontal connections of the same 4 pieces
        for row1 in range(ROW):
            if any(self._board[row1][col1] == player
                   and self._board[row1][col1 - 1] == player
                   and self._board[row1][col1 - 2] == player
                   and self._board[row1][col1 - 3] == player
                   for col1 in range(COLUMN - 1, 2, -1)):
                return True

        # Check vertical locations for win
        for col2 in range(COLUMN):
            if any(self._board[row2][col2] == player
                   and self._board[row2 - 1][col2] == player
                   and self._board[row2 - 2][col2] == player
                   and self._board[row2 - 3][col2] == player
                   for row2 in range(ROW - 1, 2, -1)):
                return True

        for col3 in range(COLUMN - 3):
            if any(self._board[row3][col3] == player
                   and self._board[row3 + 1][col3 + 1] == player
                   and self._board[row3 + 2][col3 + 2] == player
                   and self._board[row3 + 3][col3 + 3] == player
                   for row3 in range(ROW - 3)):
                return True

        # Check negatively sloped diagonals
        for col4 in range(COLUMN - 3):
            if any(self._board[row4][col4] == player
                   and self._board[row4 - 1][col4 + 1] == player
                   and self._board[row4 - 2][col4 + 2] == player
                   and self._board[row4 - 3][col4 + 3] == player
                   for row4 in range(3, ROW)):
                return True

        return False

    def _board_after_move(self, move: str) -> np.ndarray:
        """Return a copy of self._board representing the state of the board
        after the given move is made.
        """
        # Create of copy of the current self_board
        board_copy = copy.deepcopy(self._board)

        end_pos, start_pos = algebraic_to_index(move)

        # Check which player the one make the move
        if self._is_player1_active:
            board_copy[start_pos][end_pos] = HUMAN_PLAYER
        else:
            board_copy[start_pos][end_pos] = AI_PLAYER

        return board_copy

    def calculate_moves_for_board(self) -> list[str]:
        """Return all possible moves based on the current state of the game."""
        moves = []
        for i in range(COLUMN):
            for j in range(ROW - 1, -1, -1):
                if self._board[j][i] == 0:
                    move = index_to_algebraic((i, j))
                    moves.append(move)
                    break
        return moves


def algebraic_to_index(move: str) -> tuple[int, int]:
    """Convert coordinates in algebraic format ex. 'a2' to array indices (y, x)."""
    return (_RANK_TO_INDEX[move[1]], _FILE_TO_INDEX[move[0]])


def index_to_algebraic(pos: tuple[int, int]) -> str:
    """Convert coordinates in array indices (y, x) to algebraic format."""
    return INDEX_TO_FILE[pos[1]] + INDEX_TO_RANK[pos[0]]


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['PEP8'],
        'exclude-protected': ['_first'],
        'extra-imports': ['numpy', 'copy'],
        'generated-members': ['pygame.*']
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
