"""CSC111 Winter 2021 Final Project

This file is Copyright (c) 2021 An Nguyen-Trinh and Raghav Banka.
"""
import pygame
import connect4_game
import connect4_visualization
import alpha_beta

HUMAN_PLAYER = 1
AI_PLAYER = 2

LEVEL_PROMPT = 'Select the Difficulty Level(from 1 to 5 with 1 being the easiest and 5 the hardest)'

dif_level = 10

while not(dif_level in range(0, 6)):
    # ACCUMULATOR: The state selected so far.
    dif_level = int(input(LEVEL_PROMPT))

screen = connect4_visualization.initialize_screen(connect4_game.SCREEN_SIZE,
                                                  [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION])

# Initiate a new game based on the input difficulty level
game = connect4_game.Connect4Game(difficulty_level=dif_level)

connect4_visualization.draw_board(screen, game.get_board(), HUMAN_PLAYER, AI_PLAYER)
result = False

while not result:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            connect4_visualization.handle_mouse_motion(game, event, screen)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Store whether the human has won the game or not
            result = connect4_visualization.handle_mouse_click(game, event, screen, result)

            connect4_visualization.draw_board(screen, game.get_board(), HUMAN_PLAYER, AI_PLAYER)

            # Check whether the game ends in a draw.
            result = connect4_visualization.win_situation(game, screen, result)

        if event.type == pygame.QUIT:
            break

    if not game.is_player1_move() and not result:
        # Get the most optimal move for the AI player
        move = alpha_beta.find_best_ai_move(game)

        # Play that most optimal move
        game.make_move(move)

        # Check whether the AI player has won the game.
        if game.has_winner(2):
            result = True

        connect4_visualization.draw_board(screen, game.get_board(), HUMAN_PLAYER, AI_PLAYER)

        # Check whether the game ends in a draw.
        result = connect4_visualization.win_situation(game, screen, result)
