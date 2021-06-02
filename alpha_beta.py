"""CSC111 Winter 2021 Final Project

This file is Copyright (c) 2021 An Nguyen-Trinh and Raghav Banka.
"""
import math
import connect4_game

HUMAN_PLAYER = 1
AI_PLAYER = 2


def alpha_beta(game: connect4_game.Connect4Game, depth: int,
               alpha: float, beta: float) -> float:
    """Return utility score of game state based on the Alpha-Beta Minimax algorithm"""
    if depth == 0:
        return score_calculator_ai(game)
    elif game.has_winner(1) or game.has_winner(2) or game.get_valid_moves() == []:
        # Calculate the utility score of this node for the AI player
        return utility_calc_end(game)

    # Get all possible moves based on the current state of the game.
    child_list = game.get_valid_moves()

    # Check whether it is the AI player turn, which is also the maximizing player in the algorithm
    if not game.is_player1_move():
        ut_val = -math.inf
        for c in child_list:
            ut_val = max(ut_val, alpha_beta(game.copy_and_make_move(c),
                                            depth - 1, alpha, beta))
            if alpha < ut_val:
                alpha = ut_val

            if beta <= alpha:
                break
        return ut_val
    else:  # It is the human player's turn, which is also the minimizing player
        ut_val = math.inf
        for c in child_list:
            ut_val = min(ut_val, alpha_beta(game.copy_and_make_move(c),
                                            depth - 1, alpha, beta))
            if beta > ut_val:
                beta = ut_val

            if beta <= alpha:
                break
        return ut_val


def utility_calc_end(game: connect4_game.Connect4Game) -> float:
    """Function to calculate the utility score for move the AI player when the game is ending.
    """
    # Check whether the game ends in a draw.
    if len(game.get_valid_moves()) == 0:
        # There are not more moves left, so the game ends in a draw.
        return 0
    # The AI player is the winner, so this node has the most optimal utility value
    elif game.has_winner(2):
        return math.inf
    else:
        # The human player (opponent) is the winner,
        # so this node has the worst optimal utility value
        return -math.inf


def score_calculator_ai(game: connect4_game.Connect4Game) -> float:
    """Function to calculate utility score for moves for the AI player when the depth is 0.
    """
    # Accumulator: store the calculated utility score so far
    score_so_far = 0
    board = game.get_board()

    # Score center column
    center_array = []
    for i in list(board[:, connect4_game.COLUMN // 2]):
        center_array.append(int(i))
    center_count = center_array.count(AI_PLAYER)
    score_so_far += center_count * 3

    # Score Horizontal
    for r in range(connect4_game.ROW):
        row_array = []
        for i in list(board[r, :]):
            row_array.append(int(i))

        for c in range(connect4_game.COLUMN - 3):
            window = row_array[c:c + 4]
            score_so_far += evaluate_window(window, AI_PLAYER)

    # Score Vertical
    for c in range(connect4_game.COLUMN):
        col_array = []
        for i in list(board[:, c]):
            col_array.append(int(i))

        for r in range(connect4_game.ROW - 3):
            window = col_array[r:r + 4]
            score_so_far += evaluate_window(window, AI_PLAYER)

    # Score positive sloped diagonal
    for r in range(connect4_game.ROW - 3):
        for c in range(connect4_game.COLUMN - 3):
            window = [board[r + i2][c + i2] for i2 in range(4)]
            score_so_far += evaluate_window(window, AI_PLAYER)

    for r in range(connect4_game.ROW - 3):
        for c in range(connect4_game.COLUMN - 3):
            window = [board[r + 3 - i3][c + i3] for i3 in range(4)]
            score_so_far += evaluate_window(window, AI_PLAYER)
    return score_so_far


def evaluate_window(window: list, piece: int) -> int:
    """The scoring criteria set used to evaluate the utility score for
    possible moves in a Connect4Game for the given player.

    Preconditions:
        - piece == HUMAN_PLAYER or piece == AI_PLAYER
    """
    score = 0
    if piece == HUMAN_PLAYER:
        opp_piece = AI_PLAYER
    else:
        opp_piece = HUMAN_PLAYER

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # Check whether the opponent is closing to winning.
    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


def find_best_ai_move(game: connect4_game.Connect4Game) -> str:
    """Return the move with the most optimal score for the AI player based on the score calculated
    by the MiniMax Alpha-Beta algorithm. """
    valid_moves = game.get_valid_moves()
    max_move = valid_moves[0]
    dif_level = game.get_difficulty_level()
    max_utility = alpha_beta(game.copy_and_make_move(max_move), dif_level, -math.inf, math.inf)
    for item in valid_moves:
        new_utility = alpha_beta(game.copy_and_make_move(item), dif_level, -math.inf, math.inf)
        if max_utility < new_utility:
            max_move = item
            max_utility = new_utility

    return max_move


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'exclude-protected': ['_first'],
        'extra-imports': ['math', 'connect4_game'],
        'generated-members': ['pygame.*']
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
