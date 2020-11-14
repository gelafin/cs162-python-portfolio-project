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
        self._player_1 = {'name': player_1_info[0], 'color': player_1_info[1].upper()}
        self._player_2 = {'name': player_2_info[0], 'color': player_2_info[1].upper()}

        # create 6x6 board with alternating pairs of red/green spots
        self._board = FocusBoard(board_length=6, pattern=2).get_board()

    def show_pieces(self, position):
        """
        :param position: tuple representing board coordinate in (row, column) format
        :return stack: list of pieces at the given position, with index 0 as bottom
        """
        x, y = position
        return self._board[x][y]


# test
p1 = ('george', 'G')
p2 = ('ralph', 'R')
game = FocusGame(p1, p2)
stack_at_origin = game.show_pieces((0, 0))
stack_here = game.show_pieces((5, 5))
print(0)
