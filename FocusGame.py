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
        for column_index in range(board_length):
            # optimize loop if the given pattern evenly divides rows
            pattern_range = int(board_length / pattern) if board_length % pattern == 0 else board_length
            using_efficient_method = pattern_range != board_length

            # construct a row
            if using_efficient_method:
                row = self.make_row_efficiently(pattern_range, pattern)
            else:
                row = self.make_row_basic(pattern_range, pattern)

            # add the completed row to the board
            self._board.append(row)

    def make_row_efficiently(self, pattern_range, pattern):
        """
        generates a row based on desired pattern
        :param pattern_range: used to reduce iterations; int(board_length / pattern)
        :param pattern: for initial pattern; number of same color to place (left-to-right) before switching colors
        :return row: the generated row
        """
        row = []
        alternate = 'R'

        for row_index in range(pattern_range):
            if alternate == 'R':
                row.extend([['R'] for r in range(pattern)])  # append R's called for by pattern
                alternate = 'G'
            else:
                row.extend([['G'] for g in range(pattern)])  # append G's called for by pattern
                alternate = 'R'

        return row

    def make_row_basic(self, pattern_range, pattern):
        """
        generates a row based on desired pattern
        :param pattern_range:
        :param pattern:
        :return row: the generated row
        """
        row = []
        red_count = 0
        green_count = 0

        for row_index in range(pattern_range):
            # if adding red
            if red_count < pattern:
                row.append(['R'])

                # hey, we just added a red piece. Maintain counter
                red_count += 1
                if red_count >= pattern:
                    red_count = 0

            # if adding green
            elif green_count < pattern:
                row.append(['G'])

                # hey, we just added a green piece
                green_count += 1
                if green_count >= pattern:
                    green_count = 0


class FocusGame:
    """ facilitates playing Focus/Domination """
    def __init__(self, player_1_info, player_2_info):
        """ creates game board and tracks player colors """
        # hold player info
        self._player_1 = {}
        self._player_2 = {}
        (self._player_1['name'], self._player_1['color']) = player_1_info
        (self._player_2['name'], self._player_2['color']) = player_2_info

        # create 6x6 board with alternating pairs of red/green spots
        self._board = FocusBoard()

        print('glo')


# test
p1 = ('george', 'G')
p2 = ('ralph', 'R')
game = FocusGame(p1, p2)

