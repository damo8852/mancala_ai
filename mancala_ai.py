import sys
import os
import math
import copy
AIMA_PATH = os.path.join(os.path.dirname(__file__), "aima-python")
sys.path.append(AIMA_PATH)
from games import Game, minmax_decision, alpha_beta_search, alpha_beta_cutoff_search
from mancala import Mancala

class MancalaGame(Game):
    def __init__(self):
        self.initial = Mancala(verbose=False)

    def actions(self, state):
        valid = []
        if state.current_player == 1:
            start, end = state.p1_pits_index
            for i in range(start, end + 1):
                if state.board[i] > 0:
                    valid.append(i - start + 1)
        else:
            start, end = state.p2_pits_index
            for i in range(start, end + 1):
                if state.board[i] > 0:
                    valid.append(i - start + 1)
        return valid

    def result(self, state, move):
        """clone state with the move applied."""
        s2 = state.clone()
        s2.play(move)
        return s2

    def utility(self, state, player):
        """util function = (stones in player's Mancala) - (stones in opponent's Mancala)"""
        if player == 1:
            return state.board[state.p1_mancala_index] - state.board[state.p2_mancala_index]
        else:
            return state.board[state.p2_mancala_index] - state.board[state.p1_mancala_index]

    def terminal_test(self, state):
        """checks if the game is over"""
        return state.winning_eval(check_only=True)

    def to_move(self, state):
        return state.current_player

def _minimax_value(game: MancalaGame, state: Mancala, depth: int, player: int, maximizing: bool) -> int:
    if depth == 0 or game.terminal_test(state):
        return game.utility(state, player)

    if maximizing:
        best = -math.inf # maximize
        for a in game.actions(state):
            val = _minimax_value(game, game.result(state, a), depth - 1, player, False)
            if val > best:
                best = val
        return best
    else:
        best = math.inf # minimize
        for a in game.actions(state):
            val = _minimax_value(game, game.result(state, a), depth - 1, player, True)
            if val < best:
                best = val
        return best


def depth_limited_minimax_decision(state: Mancala, depth: int) -> int:
    """
    runs minimax without pruning and returns the best move for player
    """
    game = MancalaGame()
    player = game.to_move(state)

    best_action = None
    best_val = -math.inf # maximize

    for a in game.actions(state):
        val = _minimax_value(game, game.result(state, a), depth - 1, player, False)
        if val > best_val:
            best_val = val
            best_action = a
    return best_action

def alphabeta_move(state: Mancala, depth: int = 5) -> int:
    """
    choses the best move using alpha beta pruning with x depth cutoff
    """
    game = MancalaGame()
    return alpha_beta_cutoff_search(state, game, d=depth)


def minimax_move(state: Mancala, depth: int = 5) -> int:
    """
    choses the best move
    """
    return depth_limited_minimax_decision(state, depth)