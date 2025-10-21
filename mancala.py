import random
import copy

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit=4, verbose=False):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        only display the board if verbose=True
        """
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player + 1) * 2)
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.verbose = verbose

        # Pit and Mancala indices
        self.p1_pits_index = [0, self.pits_per_player - 1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player + 1, len(self.board) - 2]
        self.p2_mancala_index = len(self.board) - 1

        # Empty the Mancalas
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        if not self.verbose:
            return

        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1] + 1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1] + 1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(
                    i + 1, player_1_pits[i], player_2_pits[-(i + 1)], self.pits_per_player - i))
            else:
                print('{} -> | {} | {} | <- {}'.format(
                    i + 1, player_1_pits[i], player_2_pits[-(i + 1)], self.pits_per_player - i))
        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.current_player == 1 else 'P2'
        print('Turn: ' + turn)

    def valid_move(self, pit):
        # Check for a valid move
        if self.current_player == 1:
            index = pit - 1
            if index < self.p1_pits_index[0] or index > self.p1_pits_index[1]:
                if self.verbose: print("Invalid Move")
                return False
        else:
            index = self.p2_pits_index[0] + (pit - 1)
            if index < self.p2_pits_index[0] or index > self.p2_pits_index[1]:
                if self.verbose: print("Invalid Move")
                return False

        if self.board[index] == 0:
            if self.verbose: print("Invalid Move")
            return False

        return True

    def random_move_generator(self):
        
        valid = []
        if self.current_player == 1:
            for i in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1):
                if self.board[i] > 0:
                    valid.append(i - self.p1_pits_index[0] + 1)
        else:
            for i in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1):
                if self.board[i] > 0:
                    valid.append(i - self.p2_pits_index[0] + 1)
        if not valid:
            return None
        return random.choice(valid)

    def play(self, pit):
        """
        Runs a move for the game checking if someone won or not
        """
        if not self.valid_move(pit):
            if self.verbose: print("Invalid Move")
            return self.board

        if self.winning_eval(check_only=True):
            if self.verbose: print("GAME OVER")
            return self.board

        self.moves.append((self.current_player, pit))
        if self.current_player == 1:
            index = pit - 1
            own = self.p1_mancala_index
            skip = self.p2_mancala_index
        else:
            index = self.p2_pits_index[0] + (pit - 1)
            own = self.p2_mancala_index
            skip = self.p1_mancala_index

        stones = self.board[index]
        self.board[index] = 0
        ind = index

        while stones > 0:
            ind = (ind + 1) % len(self.board)
            if ind == skip:
                continue
            self.board[ind] += 1
            stones -= 1

        # capture feature - if last stone lands in an empty pit on player's side
        if self.current_player == 1 and ind in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1):
            if self.board[ind] == 1:
                opposite_index = self.p2_pits_index[1] - (ind - self.p1_pits_index[0])
                captured = self.board[opposite_index]
                if captured > 0:
                    self.board[self.p1_mancala_index] += captured + 1
                    self.board[ind] = 0
                    self.board[opposite_index] = 0
        elif self.current_player == 2 and ind in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1):
            if self.board[ind] == 1:
                opposite_index = self.p1_pits_index[1] - (ind - self.p2_pits_index[0])
                captured = self.board[opposite_index]
                if captured > 0:
                    self.board[self.p2_mancala_index] += captured + 1
                    self.board[ind] = 0
                    self.board[opposite_index] = 0
        # switch turn
        self.current_player = 2 if self.current_player == 1 else 1

        if self.verbose:
            self.display_board()

        # Check if game ended
        self.winning_eval()
        return self.board

    def winning_eval(self, check_only=False):
        """
        check only does not mutate the board
        checks if someone has won the game
        """
        empty1 = all(s == 0 for s in self.board[self.p1_pits_index[0]:self.p1_pits_index[1] + 1])
        empty2 = all(s == 0 for s in self.board[self.p2_pits_index[0]:self.p2_pits_index[1] + 1])
        
        # Only checking condition (for AI search)
        if check_only:
            return empty1 or empty2

        if not (empty1 or empty2):
            return False

        if empty1:
            rem = sum(self.board[self.p2_pits_index[0]:self.p2_pits_index[1] + 1])
            self.board[self.p2_mancala_index] += rem
            for i in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1):
                self.board[i] = 0
        elif empty2:
            rem = sum(self.board[self.p1_pits_index[0]:self.p1_pits_index[1] + 1])
            self.board[self.p1_mancala_index] += rem
            for i in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1):
                self.board[i] = 0

        score1 = self.board[self.p1_mancala_index]
        score2 = self.board[self.p2_mancala_index]

        if score1 > score2:
            if self.verbose: print("Game Over - P1 WINS")
        elif score1 < score2:
            if self.verbose: print("Game Over - P2 WINS")
        else:
            if self.verbose: print("Game Over - It's a Tie")
        return True

    def clone(self):
        """Clones the game state in order to keep track during simulations"""
        new_game = Mancala(self.pits_per_player)
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        new_game.moves = self.moves.copy()
        return new_game



if __name__ == "__main__":
    game = Mancala(verbose=True)
    game.display_board()
