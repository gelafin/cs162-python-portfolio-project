# Author: Mark Mendez
# Date: 11/11/2020
# Description: game

class FocusBoard:
    """
    Represents the board of a game of Focus/Domination
    Can be customized beyond the official board's parameters
    """
    def __init__(self, board_length=6, pattern=2):
        """
        creates game board
        :param board_length: width and height of board
        :param pattern: for initial pattern; number of same color to place (left-to-right) before switching colors
        """
        self._board = []

        # construct the number of columns called for by board_length
        starting_color = 'R'
        for column_index in range(board_length):
            # optimize loop if the given pattern evenly divides rows
            pattern_range = int(board_length / pattern) if board_length % pattern == 0 else board_length
            using_efficient_method = pattern_range != board_length

            # construct a row
            if using_efficient_method:
                row = self.make_row_efficiently(pattern_range, pattern, starting_color)
            else:
                row = self.make_row_basic(pattern_range, pattern, starting_color)

            # add the completed row to the board
            self._board.append(row)

            # alternate starting color
            starting_color = 'R' if starting_color == 'G' else 'G'

    def make_row_efficiently(self, pattern_range, pattern, starting_color):
        """
        generates a row based on desired pattern
        :param pattern_range: used to reduce iterations; int(board_length / pattern)
        :param pattern: for initial pattern; number of same color to place (left-to-right) before switching colors
        :param starting_color: either 'R' or 'G'; which color to place first, at the left of the row
        :return row: the generated row
        """
        row = []
        alternate = starting_color
        for row_index in range(pattern_range):
            if alternate == 'R':
                row.extend([['R'] for r in range(pattern)])  # append R's called for by pattern
                alternate = 'G'
            else:
                row.extend([['G'] for g in range(pattern)])  # append G's called for by pattern
                alternate = 'R'

        return row

    def make_row_basic(self, pattern_range, pattern, starting_color):
        """
        generates a row based on desired pattern
        :param pattern_range:
        :param pattern:
        :param starting_color: either 'R' or 'G'; which color to place first, at the left of the row
        :return row: the generated row
        """
        row = []
        count = 0
        alternate = starting_color
        for row_index in range(pattern_range):
            row.append([alternate])

            # hey, we just added a piece. Maintain counter
            count += 1
            if count >= pattern:  # if done with red
                count = 0
                alternate = 'G' if alternate == 'R' else 'R'

        return row

    def get_board(self):
        """ returns the whole board, which is a 3D list """
        return self._board


class FocusGame:
    """ facilitates playing Focus/Domination """
    def __init__(self, player_1_info, player_2_info):
        """
        initializes game board and records player info
        :param player_1_info: tuple with player 1 name and color abbreviation. E.g., ('George', 'G')
        :param player_2_info: tuple with player 2 name and color abbreviation. E.g., ('Ralph', 'R')
        """
        # hold player info
        self._players = {
            player_1_info[0]: {'color': player_1_info[1].upper(), 'reserved': 0, 'captured': 0},
            player_2_info[0]: {'color': player_2_info[1].upper(), 'reserved': 0, 'captured': 0}
        }

        self._player_turn = None

        # create 6x6 board with alternating pairs of red/green spots
        self._board = FocusBoard(board_length=6, pattern=2).get_board()

        # set maximum stack height
        self._MAX_STACK = 5

    def show_pieces(self, position):
        """
        :param position: tuple representing board coordinate in (row, column) format
        :return: list of pieces at the given position, with index 0 as bottom
        """
        x, y = position
        return self._board[x][y]

    def show_reserve(self, player_name):
        """
        shows the count of pieces that are in reserve for the given player
        :param player_name: name of player to check, as given to constructor
        :return: count of pieces in reserve for the player
        """
        return self._players[player_name]['reserved']

    def show_captured(self, player_name):
        """
        shows the count of pieces that have been captured by the given player
        :param player_name: name of player to check, as given to constructor
        :return: count of pieces captured by the player
        """
        return self._players[player_name]['captured']

    def update_stack_at_position(self, position):
        """
        if a position's stack is > stack max, processes reserve or capture for bottom piece, as appropriate
        :param position: tuple representing board coordinate in (row, column) format
        """
        stack = self.show_pieces(position)
        bottom_color = stack[0]
        active_player_color = self._players[self._player_turn]['color']
        consequence = 'captured'
        if len(stack) > self._MAX_STACK:
            # if bottom piece belongs to player making move, send to reserve
            # else, bottom piece belongs to opponent. Make capture
            if bottom_color == active_player_color:
                consequence = 'reserved'

            self._players[self._player_turn][consequence] += 1
            self.remove_bottom_from(position)

    def remove_bottom_from(self, position):
        """
        removes bottom piece from a stack at given position
        :param position: tuple representing board coordinate in (row, column) format
        """
        x, y = position
        del(self._board[x][y][0])

    def place_atop_safely(self, position, color_abbreviation):
        """
        places a piece atop a stack at given position
        :param position: tuple representing board coordinate in (row, column) format
        :param color_abbreviation: capital letter representing the color of piece to be placed
        """
        x, y = position
        self._board[x][y].append(color_abbreviation)

        # a piece has been placed!
        self.update_stack_at_position(position)

    def reserved_move(self, player_name, position):
        """
        makes a move using given player's reserve
        :param player_name: name of player to check, as given to constructor
        :param position: tuple representing board coordinate in (row, column) format
        :return:
        """

        # enforce player turns, or call from move_piece()?
        if player_name != self._player_turn:
            return 'not your turn, pumpkin-eater'

        # If there are no pieces in reserve, return 'no pieces in reserve'
        if self._players[player_name]['reserve'] == 0:
            return 'no pieces in reserve'

        # move is valid--add player's piece to board
        active_player_piece = self._players[self._player_turn]['color']
        self.place_atop_safely(position, active_player_piece)

        # remove piece from reserve
        self._players[player_name]['reserve'] -= 1

    def move_piece(self, player_name):

        # enforce valid move

        if self._player_turn is None:
            self._player_turn = player_name


# test
p1 = ('george', 'G')
p2 = ('ralph', 'R')
game = FocusGame(p1, p2)
stack_at_origin = game.show_pieces((0, 0))
stack_here = game.show_pieces((5, 5))
p1_reserve = game.show_reserve('george')
p2_reserve = game.show_reserve('ralph')
p1_captured = game.show_captured('george')
p2_captured = game.show_captured('ralph')
game.move_piece('george')
game.update_stack_at_position((0, 1))
print(0)
