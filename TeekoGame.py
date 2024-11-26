
import random
import math

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.r
        """
        self.my_piece = random.choice(self.pieces)
        self.dropCount = 0
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def run_challenge_test(self):
        # Set to True if you would like to run gradescope against the challenge AI!
        # Leave as False if you would like to run the gradescope tests faster for debugging.
        # You can still get full credit with this set to False
        return True

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        
        best_move = None
        best_value = - math.inf  # Start with the worst possible value
        # drop phase behavior  
        drop_phase = sum(row.count('b') + row.count('r') for row in state) < 8
        
        def find_winning_move(player_piece):
            """Find a winning move for the given player."""
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        # Simulate placing the player's piece
                        simulated_state = [r.copy() for r in state]
                        simulated_state[row][col] = player_piece
                        if self.game_value(simulated_state) == (1 if player_piece == self.my_piece else -1):
                            return (row, col)
            return None
        
        if drop_phase:
            opp_count = sum(row.count(self.opp) for row in state)
            my_count = sum(row.count(self.my_piece) for row in state)
            my_winning_move = find_winning_move(self.my_piece)
            if my_winning_move:
                return [my_winning_move]  # Take the winning move
            # Defensive drop phase behavior: Block opponent threats
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        # Simulate opponent move
                        simulated_state = [row.copy() for row in state]
                        simulated_state[row][col] = self.opp
                        if self.game_value(simulated_state) == -1:  # Opponent wins here
                            return [(row, col)]  # Block this move immediately
                        
            
            if opp_count == 2 and my_count == 1:
                # Check rows
                for row in range(5):
                    for col in range(2):
                        line = state[row][col:col+4]
                        if line.count(self.opp) == 2 and line.count(' ') == 2:
                            for i, val in enumerate(line):
                                if val == ' ':
                                    return [(row, col + i)]

                # Check columns
                for col in range(5):
                    for row in range(2):
                        line = [state[row+i][col] for i in range(4)]
                        if line.count(self.opp) == 2 and line.count(' ') == 2:
                            for i, val in enumerate(line):
                                if val == ' ':
                                    return [(row + i, col)]

                # Check \ diagonals
                for row in range(2):
                    for col in range(2, 5):
                        diag = [state[row+i][col-i] for i in range(4)]
                        if diag.count(self.opp) == 2 and diag.count(' ') == 2:
                            for i, val in enumerate(diag):
                                if val == ' ':
                                    return [(row + i, col - i)]

                # Check / diagonals
                for row in range(2):
                    for col in range(2):
                        diag = [state[row+i][col+i] for i in range(4)]
                        if diag.count(self.opp) == 2 and diag.count(' ') == 2:
                            for i, val in enumerate(diag):
                                if val == ' ':
                                    return [(row + i, col + i)]
                            
                            
            # First move: Place in the center if available
            if my_count == 0:
                if state[2][2] == ' ':
                    return [(2, 2)]  # Center position
                else:
                    # Center is taken, choose an immediate neighbor
                    for pos in [(2, 1), (2, 3), (1, 2), (3, 2)]:
                        if state[pos[0]][pos[1]] == ' ':
                            return [pos]

            # Second move: Place near the center
            elif my_count == 1:
                # Choose an available neighbor of the center
                for pos in [(2, 1), (2, 3), (1, 2), (3, 2), (1, 1), (1, 3), (3, 1), (3, 3)]:
                    if state[pos[0]][pos[1]] == ' ':
                        return [pos]
             # Non-drop phase: Hardcoded actions
        if not drop_phase:
            
            # 2. Secure our winning move
            my_winning_move = find_winning_move(self.my_piece)
            if my_winning_move:
                row, col = my_winning_move
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    source_row, source_col = row + dr, col + dc
                    if (
                        0 <= source_row < 5 and 0 <= source_col < 5 and  # Within board boundaries
                        state[source_row][source_col] == self.my_piece  # Is our piece
                    ):
                        # Simulate the move to ensure it maintains a winning pattern
                        simulated_state = [r.copy() for r in state]
                        simulated_state[source_row][source_col] = ' '  # Remove the piece from its current spot
                        simulated_state[row][col] = self.my_piece  # Place it in the winning spot
                        if self.game_value(simulated_state) == 1:  # Check if this move leads to a win
                            print("this is happening")
                            return [(row, col), (source_row, source_col)]  # Move to secure win
            
            # 1. Block opponent's winning move
            opp_winning_move = find_winning_move(self.opp)
            if opp_winning_move:
                row, col = opp_winning_move
                
                # Check if any of the opponent's pieces is adjacent to the winning square
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    adj_row, adj_col = row + dr, col + dc
                    if (
                        0 <= adj_row < 5 and 0 <= adj_col < 5 and  # Within board boundaries
                        state[adj_row][adj_col] == self.opp  # Opponent's piece is adjacent
                    ):
                        # Now find one of our pieces adjacent to the winning square to block
                        for dr2, dc2 in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                            source_row, source_col = row + dr2, col + dc2
                            if (
                                0 <= source_row < 5 and 0 <= source_col < 5 and  # Within board boundaries
                                state[source_row][source_col] == self.my_piece  # Our piece is adjacent
                            ):
                                print("This is happening")
                                return [(row, col), (source_row, source_col)]  # Move to block

        
        
        
        for succ_state in self.succ(state):
            move_value = self.max_value(succ_state, 1, depth_limit=3)  # Start depth at 1
            if move_value > best_value:
                best_value = move_value
                best_move = succ_state  # Update to the best state
        
        # Extract the move from the best state (this needs to map back to move format)
        return self.extract_move(state, best_move)
    
    
    def extract_move(self, old_state, new_state):
        """Extracts the move made to transition from old_state to new_state.

        Args:
            old_state (list of lists): The original state.
            new_state (list of lists): The resulting state.

        Returns:
            list: The move as a list of tuples [(row, col), (source_row, source_col)].
        """
        move = []
        for row in range(5):
            for col in range(5):
                if old_state[row][col] != new_state[row][col]:
                    if new_state[row][col] == self.my_piece:  # Piece placed or moved here
                        move.insert(0, (row, col))
                    elif old_state[row][col] == self.my_piece:  # Piece moved from here
                        move.append((row, col))
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)
        
    def succ(self, state):
        successors = []
        drop_phase = sum(row.count('b') + row.count('r') for row in state) < 8
        
        if drop_phase:
            # Drop phase: Add a new piece to an unoccupied space
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        new_state = [row.copy() for row in state]
                        new_state[row][col] = self.my_piece
                        successors.append(new_state)
                        
        else:
            # Move phase: Move a piece to an adjacent unoccupied space
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        # Check adjacent spaces
                        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                            new_row, new_col = row + dr, col + dc
                            if 0 <= new_row < 5 and 0 <= new_col < 5 and state[new_row][new_col] == ' ':
                                new_state = [row.copy() for row in state]
                                new_state[row][col] = ' '  # Remove piece from old location
                                new_state[new_row][new_col] = self.my_piece  # Place piece in new location
                                successors.append(new_state)
        return successors

        
    def heuristic_game_value(self, state):
        """Evaluates the heuristic value of the game state, prioritizing the center of the board.

        Args:
            state (list of lists): The current board state.

        Returns:
            float: A heuristic value representing the favorability of the state for the AI.
        """
        my_score = 0
        opp_score = 0

        # Order of evaluation: Start from the center and move outward
        positions = [
            (2, 2),  # Center
            (2, 1), (2, 3), (1, 2), (3, 2),  # Immediate neighbors of the center
            (1, 1), (1, 3), (3, 1), (3, 3),  # Diagonals around the center
            (0, 2), (4, 2), (2, 0), (2, 4),  # Vertical and horizontal lines from the center
            (0, 1), (0, 3), (1, 0), (1, 4), (3, 0), (3, 4), (4, 1), (4, 3),  # Outer neighbors
            (0, 0), (0, 4), (4, 0), (4, 4)   # Corners
        ]

        # Evaluate horizontal and vertical lines
        for row, col in positions:
            if col <= 1:  # Horizontal lines starting from this column
                my_score = max(my_score, state[row][col:col+4].count(self.my_piece))
                opp_score = max(opp_score, state[row][col:col+4].count(self.opp))
            if row <= 1:  # Vertical lines starting from this row
                col_pattern = [state[row+k][col] for k in range(4) if row+k < 5]
                my_score = max(my_score, col_pattern.count(self.my_piece))
                opp_score = max(opp_score, col_pattern.count(self.opp))

        # Evaluate diagonals
        for row, col in positions:
            if 0 <= row <= 1 and 0 <= col <= 1:  # Diagonal (top-left to bottom-right)
                diag1_pattern = [state[row+k][col+k] for k in range(4) if row+k < 5 and col+k < 5]
                my_score = max(my_score, diag1_pattern.count(self.my_piece))
                opp_score = max(opp_score, diag1_pattern.count(self.opp))
            if 0 <= row <= 1 and 3 <= col <= 4:  # Diagonal (top-right to bottom-left)
                diag2_pattern = [state[row+k][col-k] for k in range(4) if row+k < 5 and col-k >= 0]
                my_score = max(my_score, diag2_pattern.count(self.my_piece))
                opp_score = max(opp_score, diag2_pattern.count(self.opp))

        # Evaluate 2x2 boxes
        for row, col in positions:
            if row < 4 and col < 4:
                box_pattern = [
                    state[row][col], state[row][col+1],
                    state[row+1][col], state[row+1][col+1]
                ]
                my_score = max(my_score, box_pattern.count(self.my_piece))
                opp_score = max(opp_score, box_pattern.count(self.opp))

        # Normalize scores for heuristic
        return my_score / 4 if my_score >= opp_score else opp_score / -4
        
        

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def min_value(self, state, depth, depth_limit=2):
        """Implements the min_value function of the minimax algorithm.

        Args:
            state (list of lists): The current game state.
            depth (int): The current depth of recursion.
            depth_limit (int): The maximum depth to explore.

        Returns:
            float: The heuristic value of the state.
        """
        # Check for terminal state or depth limit
        game_val = self.game_value(state)
        if game_val != 0:  # Terminal stateC
            return game_val
        if depth >= depth_limit:
            return self.heuristic_game_value(state)

        min_val = math.inf
        for succ_state in self.succ(state):
            min_val = min(min_val, self.max_value(succ_state, depth + 1, depth_limit))
            if min_val == -1:  # Opponent has a guaranteed win, prune
                break
        return min_val
    
    def max_value(self, state, depth, depth_limit=2):
        """Implements the max_value function of the minimax algorithm.

        Args:
            state (list of lists): The current game state.
            depth (int): The current depth of recursion.
            depth_limit (int): The maximum depth to explore.

        Returns:
            float: The heuristic value of the state.
        """
        # Check for terminal state or depth limit
        game_val = self.game_value(state)
        if game_val != 0:  # Terminal state
            return game_val
        if depth >= depth_limit:
            return self.heuristic_game_value(state)

        max_val = -math.inf
        for succ_state in self.succ(state):
            max_val = max(max_val, self.min_value(succ_state, depth + 1, depth_limit))
            if max_val == 1:  # AI has a guaranteed win, prune
                break
        return max_val

    def game_value(self, state):
        
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1
        # Check \ diagonal wins
        for row in range(2):
            for col in range(2, 5):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    return 1 if state[row][col] == self.my_piece else -1

        # Check / diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col] == self.my_piece else -1
                
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row][col+1] == state[row+1][col] == state[row+1][col+1]:
                    return 1 if state[row][col] == self.my_piece else -1


        # TODO: check \ diagonal wins
        # TODO: check / diagonal wins
        # TODO: check box wins

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:
        
        print("Game value " + str(ai.heuristic_game_value(ai.board)))

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(move)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:
        
        print("Game value " + str(ai.heuristic_game_value(ai.board)))

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()