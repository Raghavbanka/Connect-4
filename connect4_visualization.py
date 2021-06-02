"""CSC111 Winter 2021 Final Project

This file is Copyright (c) 2021 An Nguyen-Trinh and Raghav Banka.
"""
import numpy as np

import pygame
from pygame.colordict import THECOLORS
import connect4_game

HUMAN_PLAYER = 1
AI_PLAYER = 2


def initialize_screen(screen_size: tuple[int, int], allowed_motions: list) -> pygame.Surface:
    """Initialize the Pygame screen for the game and the display window.

    The parameter allow_motions is a list of pygame event types
    that will have an effect while pygame is running.
    """
    # Initializing our pygame screen
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(THECOLORS['black'])
    pygame.display.flip()

    # Specifying the types of events we are allowing for our implementation
    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed_motions)

    return screen


def draw_text(screen: pygame.Surface, text: str, pos: tuple[int, int]) -> None:
    """Draw the given text to the pygame screen at the given position (pos).

    pos represents the *upper-left corner* of the text.
    """
    # Specifying the format of the text that will be displayed
    font = pygame.font.SysFont('inconsolata', 70)
    text_surface = font.render(text, True, THECOLORS['green'])
    width, height = text_surface.get_size()
    # Displaying the input message at the given location
    screen.blit(text_surface,
                pygame.Rect(pos, (pos[0] + width, pos[1] + height)))


def draw_board(screen: pygame.Surface, board: np.ndarray, player1: int, player2: int) -> None:
    """Displays the game board using pygame.
    """
    # Calculating the radius of the token and the size of the board displayed
    square = (connect4_game.SCREEN_SIZE[1] // connect4_game.COLUMN)
    radius = int(square / 2 - 5)
    pygame.draw.rect(screen, THECOLORS['black'], ((0, 0), (connect4_game.SCREEN_SIZE[0], square)))
    pygame.draw.rect(screen, THECOLORS['blue'], ((0, square), (connect4_game.SCREEN_SIZE[0],
                                                               connect4_game.SCREEN_SIZE[
                                                                   1] - square)))

    # Loop to iterate over the game' s board and print the tokens accordingly in the pygame window
    for i in range(connect4_game.ROW):
        for j in range(connect4_game.COLUMN):
            y_position = square + square * (i + 1) - square // 2
            x_position = square * (j + 1) - square // 2
            piece = board[i][j]
            # Check whether the position is empty or has been occupied by a player's token
            if piece == player1:
                pygame.draw.circle(screen, THECOLORS['yellow'], (x_position, y_position), radius)
            elif piece == player2:
                pygame.draw.circle(screen, THECOLORS['red'], (x_position, y_position), radius)
            else:
                pygame.draw.circle(screen, THECOLORS['black'], (x_position, y_position), radius)


def handle_mouse_motion(game: connect4_game.Connect4Game, event: pygame.event.Event,
                        screen: pygame.Surface) -> None:
    """Displays for the event when the player moves their cursor across the board before dropping
     their piece"""
    square = (connect4_game.SCREEN_SIZE[1] // connect4_game.COLUMN)
    radius = int(square // 2 - 5)
    if event.type == pygame.MOUSEMOTION:
        # Displaying the black rectangle on the head of the game board
        pygame.draw.rect(screen, THECOLORS['black'],
                         ((0, 0), (connect4_game.SCREEN_SIZE[0], square)))
        # Extracting the horizontal position of the players cursor
        position_x = event.pos[0]
        # Displaying the token if player1 is making the cursor motion
        if game.is_player1_move():
            pygame.draw.circle(screen, THECOLORS['yellow'], (position_x, square // 2),
                               radius)


def handle_mouse_click(game: connect4_game.Connect4Game, event: pygame.event.Event,
                       screen: pygame.Surface,
                       result: bool) -> bool:
    """Displays for the event when the player does a mouse click on the board.
    """
    square = (connect4_game.SCREEN_SIZE[1] // connect4_game.COLUMN)
    pygame.draw.rect(screen, THECOLORS['black'], ((0, 0), (connect4_game.SCREEN_SIZE[0], square)))

    # Extracting the horizontal position of the player's right click
    position_x = event.pos[0]
    column = position_x // square
    if column == connect4_game.COLUMN:
        column = connect4_game.COLUMN - 1

    # Getting the corresponding column from the horizontal position of the player's right click
    rows = game.get_move(column)
    if rows != -1:
        move = connect4_game.index_to_algebraic((column, rows))
        game.make_move(move)
        if game.has_winner(1):
            result = True

    return result


def win_situation(game: connect4_game.Connect4Game, screen: pygame.Surface, result: bool) -> bool:
    """If the game has a winner, display to announce the winner. If not, return whether the
    game has end by checking if the game ends in a draw.
    """
    font = pygame.font.SysFont('inconsolata', 70)
    if result:
        if game.is_player1_move() is False:
            # Condition when the user wins
            pos = (40, 40)
            text_surface = font.render("Player 1 wins ", True, THECOLORS['green'])
            width, height = text_surface.get_size()
            screen.blit(text_surface,
                        pygame.Rect(pos, (pos[0] + width, pos[1] + height)))
            pygame.display.update()
        else:
            # Winning condition for the AI
            pos = (40, 40)
            text_surface = font.render("Player 2 wins ", True, THECOLORS['green'])
            width, height = text_surface.get_size()
            screen.blit(text_surface,
                        pygame.Rect(pos, (pos[0] + width, pos[1] + height)))
            pygame.display.update()
        pygame.event.wait(11000)
        pygame.display.quit()

    if game.is_draw() and result is False:
        # Condition when the game is drawn
        pos = (40, 40)
        text_surface = font.render("Draw", True, THECOLORS['green'])
        width, height = text_surface.get_size()
        screen.blit(text_surface,
                    pygame.Rect(pos, (pos[0] + width, pos[1] + height)))
        pygame.display.update()
        result = True
        pygame.event.wait(11000)
        pygame.display.quit()

    # Returning the outcome of the game
    return result


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'exclude-protected': ['_first'],
        'extra-imports': ['pygame', 'pygame.colordict', 'connect4_game', 'numpy'],
        'generated-members': ['pygame.*']
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
