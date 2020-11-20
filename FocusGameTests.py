import unittest
from FocusGame import FocusBoard, FocusGame

MESSAGES = {
    'invalid_location': 'invalid location',
    'invalid_number_of_pieces': 'invalid number of pieces',
    'not_your_turn': 'not your turn',
    'move_success': 'successfully moved'
}


def initialize_basic_game():
    p1 = ('george', 'G')
    p2 = ('ralph', 'R')
    game = FocusGame(p1, p2)

    return game


class MyTestCase(unittest.TestCase):

    def test_initializations_default_settings(self):
        game = initialize_basic_game()

        stack_at_origin = game.show_pieces((0, 0))
        self.assertListEqual(['R'], stack_at_origin)

        stack_at_end = game.show_pieces((5, 5))  # ['G']
        self.assertListEqual(['G'], stack_at_end)

        p1_reserve = game.show_reserve('george')  # 0
        self.assertEqual(p1_reserve, 0)

        p2_reserve = game.show_reserve('ralph')  # 0
        self.assertEqual(p2_reserve, 0)

        p1_captured = game.show_captured('george')  # 0
        self.assertEqual(p1_captured, 0)

        p2_captured = game.show_captured('ralph')  # 0
        self.assertEqual(p2_captured, 0)

    def test_attempt_moving_opponent_piece_during_first_turn_default_settings(self):
        game = initialize_basic_game()
        message_not_piece = game.move_piece('ralph', (2, 0), (1, 0), 1)

        self.assertEqual(message_not_piece, MESSAGES['invalid_location'])

    def test_attempt_moving_opponent_piece_during_second_turn_default_settings(self):
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (0, 1), 1)  # 0,0 has nothing and 0,1 has [R, R]
        message_not_piece = game.move_piece('george', (0, 1), (0, 0), 1)  # not your piece

        self.assertEqual(message_not_piece, MESSAGES['invalid_location'])

    def test_move_piece_success_default_settings(self):
        game = initialize_basic_game()
        message_yes = game.move_piece('ralph', (0, 0), (0, 1), 1)  # 0,0 has nothing and 0,1 has [R, R]

        self.assertEqual(message_yes, MESSAGES['move_success'])

    def test_attempt_moving_during_opponent_turn_default_settings(self):
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (0, 1), 1)  # 0,0 has nothing and 0,1 has [R, R]
        message_not_turn = game.move_piece('ralph', (0, 1), (0, 2), 1)  # hey, not your turn

        self.assertEqual(message_not_turn, MESSAGES['not_your_turn'])

    def test_attempt_moving_empty_space_default_settings(self):
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 0,1 has [R, R]
        game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 0,1 has [R, R, G]
        message_invalid_location = game.move_piece('ralph', (0, 0), (0, 1), 1)  # used to be ralph's piece; now empty

        self.assertEqual(message_invalid_location, MESSAGES['invalid_location'])

    def test_attempt_moving_piece_to_its_own_location_default_settings(self):
        game = initialize_basic_game()
        message_invalid_location = game.move_piece('ralph', (0, 0), (0, 0), 1)

        self.assertEqual(message_invalid_location, MESSAGES['invalid_location'])


if __name__ == '__main__':
    unittest.main()
