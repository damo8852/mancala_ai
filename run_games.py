import time
import random
import copy
from mancala import Mancala
from mancala_ai import minimax_move, alphabeta_move


def random_move(game):
    """random move for the random player (player 2)"""
    return game.random_move_generator()


def play_game(ai_func=None, depth=5, starting_player=1):
    """
    plays 1 complete game and returns final scores and total moves
    (player 1 = AI)
    (player 2 = random)
    """
    game = Mancala(verbose=False)
    game.current_player = starting_player
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

    print(f"\n--- Results after {num_games} games ---")
    print(f"AI Function: {ai_func.__name__ if ai_func else 'Random'}, Depth: {depth}")
    print(f"Player 1 Wins(AI): {results['p1_wins']}, ({results['p1_wins'] / num_games * 100:.1f}%)")
    print(f"Player 2 Wins(Random): {results['p2_wins']}, ({results['p2_wins'] / num_games * 100:.1f}%)")
    print(f"Ties: {results['ties']}, ({results['ties'] / num_games * 100:.1f}%)")
    print(f"Average Moves per Game: {avg_moves:.2f}")
    print(f"Average Time per Game: {avg_time:.2f}s")
    print("-----------------------------------")

def first_move_advantage_test(num_games=100, depth=5):
    p1_wins_as_first = 0
    p2_wins_as_first = 0
    ties = 0

    for i in range(num_games):
        if i % 2 == 0:
            p1, p2, moves = play_game(ai_func=alphabeta_move, depth=depth, starting_player=1)
            if p1 > p2:
                p1_wins_as_first += 1
            elif p2 > p1:
                p2_wins_as_first += 1
            else:
                ties += 1
        else:
            p1, p2, moves = play_game(ai_func=alphabeta_move, depth=depth, starting_player=2)
            if p2 > p1:
                p1_wins_as_first += 1
            elif p1 > p2:
                p2_wins_as_first += 1
            else:
                ties += 1

    total = num_games
    print(f"\n--- First-Move Advantage over {total} games ---")
    print(f"Player 1 wins when starting first: {p1_wins_as_first} ({100*p1_wins_as_first/total:.1f}%)")
    print(f"Player 2 wins when starting first: {p2_wins_as_first} ({100*p2_wins_as_first/total:.1f}%)")
    print(f"Ties: {ties} ({100*ties/total:.1f}%)")
    print("-----------------------------------")



if __name__ == "__main__":
    print("MANCALA AI RESULTS")
    print("1. Random vs Random:")
    simulate_games(num_games=100, ai_func=None, depth=0)

    print("\n2. Minimax vs Random (depth 5):")
    simulate_games(num_games=100, ai_func=minimax_move, depth=5)

    print("\n3. Alpha-Beta vs Random (depth 5):")
    simulate_games(num_games=100, ai_func=alphabeta_move, depth=5)

    print("\n4. Alpha-Beta vs Random (depth 10):")
    simulate_games(num_games=100, ai_func=alphabeta_move, depth=10)

    print("\n5. First-Move Advantage Test (Alpha-Beta depth 5):")
    first_move_advantage_test(num_games=100, depth=5)