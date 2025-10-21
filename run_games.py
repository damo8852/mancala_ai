import time
import random
import copy
from mancala import Mancala
from mancala_ai import minimax_move, alphabeta_move


def random_move(game):
    """random move for the random player (player 2)"""
    return game.random_move_generator()


def play_game(ai_func=None, depth=5):
    """
    plays 1 complete game and returns final scores and total moves
    (player 1 = AI)
    (player 2 = random)
    """
    game = Mancala(verbose=False)
    total_moves = 0

    while not game.winning_eval(check_only=True):
        total_moves += 1
        if game.current_player == 1:
            if ai_func:
                move = ai_func(copy.deepcopy(game), depth)
            else:
                move = random_move(game)
        else:
            move = random_move(game)

        if move is None:
            break

        game.play(move)

    p1_score = game.board[game.p1_mancala_index]
    p2_score = game.board[game.p2_mancala_index]
    return p1_score, p2_score, total_moves


def simulate_games(num_games=100, ai_func=None, depth=5):
    """runs x number of games with results"""
    results = {'p1_wins': 0, 'p2_wins': 0, 'ties': 0}
    move_counts = []

    start_time = time.time()
    for _ in range(num_games):
        p1, p2, moves = play_game(ai_func=ai_func, depth=depth)
        move_counts.append(moves)

        if p1 > p2:
            results['p1_wins'] += 1
        elif p2 > p1:
            results['p2_wins'] += 1
        else:
            results['ties'] += 1

    total_time = time.time() - start_time
    avg_moves = sum(move_counts) / len(move_counts)
    avg_time = total_time / num_games

    print(f"\n----- Results after {num_games} games -----")
    print(f"AI Function: {ai_func.__name__ if ai_func else 'Random'}  |  Depth: {depth}")
    print(f"Player 1 Wins(AI): {results['p1_wins']}  ({results['p1_wins'] / num_games * 100:.1f}%)")
    print(f"Player 2 Wins(Random): {results['p2_wins']}  ({results['p2_wins'] / num_games * 100:.1f}%)")
    print(f"Ties: {results['ties']}  ({results['ties'] / num_games * 100:.1f}%)")
    print(f"Average Moves per Game: {avg_moves:.2f}")
    print(f"Average Time per Game: {avg_time:.2f}s")
    print("-----------------------------------")


if __name__ == "__main__":
    print("========== MANCALA AI PROJECT ==========")
    print("1. Random vs Random:")
    simulate_games(num_games=100, ai_func=None, depth=0)

    print("\n2. Minimax (depth 5) vs Random:")
    simulate_games(num_games=100, ai_func=minimax_move, depth=5)

    print("\n3. Alpha-Beta (depth 5) vs Random:")
    simulate_games(num_games=100, ai_func=alphabeta_move, depth=5)

    print("\n4. Alpha-Beta (depth 10) vs Random:")
    simulate_games(num_games=10, ai_func=alphabeta_move, depth=10)