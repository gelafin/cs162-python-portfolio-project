# Author: Mark Mendez
# Date: 11/11/2020
# Description: game


def cartesian_to_list(cartesian_coordinate):
    """
    translates cartesian coordinates (x, y) into Python 2D list subscript indices (y, x)
    :param cartesian_coordinate: tuple of two integers representing a Cartesian-style point
    :return: tuple of two integers in the opposite order, which can be used to subscript into a Python list
    """
    x, y = cartesian_coordinate

    return y, x


class FocusBoard:
    """
    Represents the board of a game of Focus/Domination
    Can be customized beyond the official board's parameters
    """
    def __init__(self, board_length=6, pattern=2):
        """
        creates game board
        :param board_length: width and height of board
        :param pattern: for initial pattern; number of a color to place (left-to-right) before switching colors
        """
        self._board = []

        # construct the number of columns called for by board_length
        starting_color = 'R'
        for row_index in range(board_length):
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
        :return: the generated row
        """
        row = []
        alternate = starting_color
        for pattern_index in range(pattern_range):
            if alternate == 'R':
                row.extend([['R'] for r in range(pattern)])  # append R's called for by pattern
                alternate = 'G'
            else:
                row.extend([['G'] for g in range(pattern)])  # append G's called for by pattern
                alternate = 'R'

        return row

    def make_row_basic(self, board_length, pattern, starting_color):
        """
        generates a row based on desired pattern
        :param board_length: number of columns in the board
        :param pattern: for initial pattern; number of same color to place (left-to-right) before switching colors
        :param starting_color: either 'R' or 'G'; which color to place first, at the left of the row
        :return: the generated row
        """
        row = []
        count = 0
        alternate = starting_color
        for column_index in range(board_length):
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

        self._whose_turn = None

        # create 6x6 board with alternating pairs of red/green spots
        self._board = FocusBoard(board_length=6, pattern=2).get_board()

        # optional settings: maximum stack height and number of captures to win
        self._MAX_STACK_HEIGHT = 5
        self._WINNING_CAPTURE_COUNT = 6

        self._ERROR_MESSAGES = {
            'invalid_location': 'invalid location',
            'invalid_number_of_pieces': 'invalid number of pieces',
            'invalid_player_turn': 'not your turn'
        }

        self._CONFIRMATION_MESSAGES = {
            'move_success': 'successfully moved'
        }

    def change_player_turn(self):
        """
        changes whose turn it is
        """
        player_1_name, player_2_name = self._players.keys()  # good place to put a generator if allowing #moreplayers

        self._whose_turn = player_1_name if self._whose_turn != player_1_name else player_2_name

    def show_pieces(self, position):
        """
        returns a list of pieces at a given position
        :param position: tuple representing board coordinate, in (row, column) format
        :return: list of pieces at the given position, with index 0 as bottom
        """
        x, y = cartesian_to_list(position)
        return self._board[x][y]

    def show_reserve(self, player_name):
        """
        shows the count of pieces that are in reserve for the given player
        :param player_name: name of player to check, as given to constructor (spelling not enforced here)
        :return: number of pieces in reserve for the player
        """
        return self._players[player_name]['reserved']

    def show_captured(self, player_name):
        """
        shows the count of pieces that have been captured by the given player
        :param player_name: name of player to check, as given to constructor (spelling not enforced here)
        :return: number of pieces captured by the player
        """
        return self._players[player_name]['captured']

    def remove_pieces_from_stack(self, position, top_or_bottom, number_to_remove):
        """
        removes bottom piece from a stack at given position
        :param position: tuple representing board coordinate, in (row, column) format
        :param top_or_bottom: 'top' or 'bottom'; determines whether pieces should be removed from top or bottom of stack
        :param number_to_remove: how many pieces to remove
        :return: list of pieces removed
        """
        x, y = cartesian_to_list(position)
        full_stack = self._board[x][y]  # lol
        stack_top_no_bottom = self._board[x][y][number_to_remove:]
        stack_bottom_no_top = self._board[x][y][:-number_to_remove]

        if top_or_bottom == 'top':
            self._board[x][y] = stack_bottom_no_top
            removed_pieces = stack_top_no_bottom if len(full_stack) != 1 else full_stack  # no bottom means no singleton
        else:
            self._board[x][y] = stack_top_no_bottom
            removed_pieces = stack_bottom_no_top if len(full_stack) != 1 else full_stack  # no top means no singleton

        return removed_pieces

    def place_atop_safely(self, position, stack):
        """
        places a piece atop a stack at given position
        :param position: tuple representing board coordinate, in (row, column) format
        :param stack: list of pieces to be placed
        """
        x, y = cartesian_to_list(position)
        self._board[x][y].extend(stack)  # place stack atop the stack already at position

        # a piece has been placed! process the consequence based on game rules
        stack = self.show_pieces(position)
        bottom_color = stack[0]
        active_player_color = self._players[self._whose_turn]['color']
        excess_stack_height = len(stack) - self._MAX_STACK_HEIGHT  # has negative "excess" for small stacks

        if excess_stack_height > 0:  # game rules define consequences based on excess stack height
            # if bottom piece belongs to player making move, send to reserve. Else, make capture of opponent piece
            consequence = 'captured'
            if bottom_color == active_player_color:
                consequence = 'reserved'

            # remove the excess pieces from the board
            self.remove_pieces_from_stack(position, 'bottom', number_to_remove=excess_stack_height)

            # place the excess pieces into this player's reserve or capture pile, as appropriate
            self._players[self._whose_turn][consequence] += 1

    def is_in_board(self, position):
        """
        checks whether a position is a playable point on the board
        :param position: tuple representing board coordinate, in (row, column) format
        :return: True if position is playable; False otherwise
        """
        x, y = cartesian_to_list(position)

        # check if y is out of column range
        if y < 0 or y > len(self._board) - 1:  # comparing to 0-based index
            return False
        # check if x is out of row range
        if x < 0 or x > len(self._board[0]) - 1:  # comparing to 0-based index
            return False

        # passed all checks
        return True

    def reserved_move(self, player_name, position):
        """
        makes a move using given player's reserve
        :param player_name: name of player to check, as given to constructor (spelling not enforced here)
        :param position: tuple representing board coordinate, in (row, column) format
        :return: confirmation message if move was processed; error message otherwise
        """
        # enforce player turns like this, or call from move_piece()?
        if player_name != self._whose_turn:
            return 'not your turn'

        # If there are no pieces in reserve, return 'no pieces in reserve'
        if self._players[player_name]['reserve'] <= 0:
            return 'no pieces in reserve'

        # enforce valid position; position is within bounds
        if not self.is_in_board(position):
            return self._ERROR_MESSAGES['invalid_location']

        # move is valid--add player's piece to board
        active_player_piece = self._players[player_name]['color']
        self.place_atop_safely(position, [active_player_piece])

        # update reserve count
        self._players[player_name]['reserve'] -= 1

        # change whose turn it is
        self.change_player_turn()

        # if this was the winning move, announce the winner
        if self._players[player_name]['captured'] >= self._WINNING_CAPTURE_COUNT:
            return self._whose_turn + ' Wins'

        # completed a successful normal move
        return self._CONFIRMATION_MESSAGES['move_success']

    def position_is_in_stack_range(self, stack_position, to_position):
        """
        determines whether a given position is within legal move range of a stack at a given position
        :param stack_position: tuple representing board coordinate of stack position, in (row, column) format
        :param to_position: tuple representing board coordinate of destination position, in (row, column) format
        :return: True if to_position is within legal move range of the stack; False otherwise
        """
        move_range = len(self.show_pieces(stack_position))
        from_x, from_y = stack_position
        to_x, to_y = to_position
        distance_x = abs(from_x - to_x)  # board coordinates are all guaranteed to be non-negative
        distance_y = abs(from_y - to_y)  # board coordinates are all guaranteed to be non-negative
        total_distance = distance_x + distance_y

        if total_distance > move_range or total_distance < 1:  # moving more/less spaces than allowed?
            return False

        # passed all tests; to_position is within legal move range
        return True

    def move_piece(self, player_name, from_position, to_position, pieces_moved):
        """
        moves pieces_moved pieces from from_position to to_position; player_name needed for validation
        :param player_name: name of player to check, as given to constructor (spelling not enforced here)
        :param from_position: tuple representing board coordinate of stack to move, in (row, column) format
        :param to_position: tuple representing board coordinate of destination position, in (row, column) format
        :param pieces_moved: number of pieces to move (equal to number of spaces to move)
        :return: confirmation message if move was processed; error message otherwise
        """
        if self._whose_turn is None:
            self._whose_turn = player_name

        # enforce valid turn
        if self._whose_turn != player_name:
            return self._ERROR_MESSAGES['invalid_player_turn']

        # enforce valid from_position; from_position is not empty
        if len(self.show_pieces(from_position)) < 1:
            return self._ERROR_MESSAGES['invalid_location']

        # enforce valid from_position; player controls top of stack at from_position
        if self.show_pieces(from_position)[-1] != self._players[player_name]['color']:
            return self._ERROR_MESSAGES['invalid_location']

        # enforce valid to_position; to_position is within bounds
        if not self.is_in_board(to_position):
            return self._ERROR_MESSAGES['invalid_location']

        # enforce valid to_position; to_position is within legal range
        if not self.position_is_in_stack_range(from_position, to_position):
            return self._ERROR_MESSAGES['invalid_location']

        # enforce valid number of pieces moved
        if pieces_moved > len(self.show_pieces(from_position)):
            return self._ERROR_MESSAGES['invalid_number_of_pieces']

        # move is valid--process the move by removing pieces from from_position and placing atop to_position
        removed_pieces = self.remove_pieces_from_stack(from_position, 'top', pieces_moved)
        self.place_atop_safely(to_position, removed_pieces)

        # change whose turn it is
        self.change_player_turn()

        # if this was the winning move, announce the winner
        if self._players[player_name]['captured'] >= self._WINNING_CAPTURE_COUNT:
            return self._whose_turn + ' Wins'

        # completed a successful normal move
        return self._CONFIRMATION_MESSAGES['move_success']


# test
p1 = ('george', 'G')
p2 = ('ralph', 'R')
game = FocusGame(p1, p2)

game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 0,1 has [R, R]
game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 1,0 has [R, R, G]

message_invalid_location_2 = game.move_piece('george', (0, 1), (0, 1), 1)  # move stack to same location?

message_invalid_location_3 = game.move_piece('george', (0, 1), (0, 1), 0)  # move stack to same location, using turn?

game.move_piece('ralph', (2, 1), (2, 0), 1)  # 2,1 has nothing and 2,0 has [R]


