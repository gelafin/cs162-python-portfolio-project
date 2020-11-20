import unittest
from FocusGame import FocusBoard, FocusGame

MESSAGES = {
    'invalid_location': 'invalid location',
    'invalid_number_of_pieces': 'invalid number of pieces',
    'not_your_turn': 'not your turn',
    'move_success': 'successfully moved',
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

    def test_move_one_piece_horizontally_success_default_settings(self):
        game = initialize_basic_game()
        message_success = game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 1,0 has [R, R]

        self.assertEqual(message_success, MESSAGES['move_success'])
        self.assertListEqual(game.show_pieces((0, 0)), [])
        self.assertListEqual(game.show_pieces((1, 0)), ['R', 'R'])

    def test_move_one_piece_vertically_success_default_settings(self):
        game = initialize_basic_game()
        message_success = game.move_piece('ralph', (0, 0), (0, 1), 1)  # 0,0 has nothing and 0, 1 has [G, R]

        self.assertEqual(message_success, MESSAGES['move_success'])
        self.assertListEqual(game.show_pieces((0, 0)), [])
        self.assertListEqual(game.show_pieces((0, 1)), ['G', 'R'])

    def test_move_two_of_three_pieces_success_default_settings(self):
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 1, 0 has [R, R]
        game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 1,0 has [R, R, G]
        game.move_piece('ralph', (5, 0), (4, 0), 1)  # ralph has no more stacks in range of 1,0
        message_success = game.move_piece('george', (1, 0), (3, 0), 2)  # 1,0 has [R] and 3,0 has [G, R, G]

        self.assertEqual(message_success, MESSAGES['move_success'])
        self.assertListEqual(game.show_pieces((1, 0)), ['R'])
        self.assertListEqual(game.show_pieces((3, 0)), ['G', 'R', 'G'])

    def test_move_three_of_three_pieces_success_default_settings(self):
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 1, 0 has [R, R]
        game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 1,0 has [R, R, G]
        game.move_piece('ralph', (5, 0), (4, 0), 1)  # 5,0 has nothing and 4,0 has [R, R]
        message_success = game.move_piece('george', (1, 0), (4, 0), 3)  # 1,0 has nothing and 4,0 has [R, R, R, R, G]

        self.assertEqual(message_success, MESSAGES['move_success'])
        self.assertListEqual(game.show_pieces((1, 0)), [])
        self.assertListEqual(game.show_pieces((4, 0)), ['R', 'R', 'R', 'R', 'G'])

    def test_move_two_of_three_pieces_diagonal_success_default_settings(self):
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 1, 0 has [R, R]
        game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 1,0 has [R, R, G]
        game.move_piece('ralph', (5, 0), (4, 0), 1)  # ralph has no more stacks in range of 1,0
        message_success = game.move_piece('george', (1, 0), (2, 1), 2)  # 1,0 has [R] and 2,1 has [R, R, G]

        self.assertEqual(message_success, MESSAGES['move_success'])
        self.assertListEqual(game.show_pieces((1, 0)), ['R'])
        self.assertListEqual(game.show_pieces((2, 1)), ['R', 'R', 'G'])

    def test_add_1_to_capture_success_default_settings(self):
        """ the game kind of stack, the good kind of overflow """
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 1, 0 has [R, R]
        game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 1,0 has [R, R, G]
        game.move_piece('ralph', (5, 0), (4, 0), 1)  # 5,0 has nothing and 4,0 has [R, R]
        game.move_piece('george', (1, 0), (4, 0), 3)  # 1,0 has nothing and 4,0 has [R, R, R, R, G]
        game.move_piece('ralph', (3, 5), (4, 5), 1)  # 3,5 has nothing and 4,5 has [G, R]
        message_success = game.move_piece('george', (4, 1), (4, 0), 1)  # 4,1 has nothing and 4,0 has [R, R, R, R, G, G]

        # red on bottom means capture [R]

        self.assertEqual(message_success, MESSAGES['move_success'])
        self.assertListEqual(game.show_pieces((4, 0)), ['R', 'R', 'R', 'G', 'G'])
        self.assertEqual(game.show_captured('george'), 1)

    def test_add_2_split_into_reserve_and_capture_success_default_settings(self):
        """ the game kind of stack, the good kind of overflow """
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 1, 0 has [R, R]
        game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 1,0 has [R, R, G]
        game.move_piece('ralph', (5, 0), (4, 0), 1)  # 5,0 has nothing and 4,0 has [R, R]
        game.move_piece('george', (1, 0), (4, 0), 3)  # 1,0 has nothing and 4,0 has [R, R, R, R, G]
        game.move_piece('ralph', (3, 5), (4, 5), 1)  # 3,5 has nothing and 4,5 has [G, R]
        message_success = game.move_piece('george', (4, 0), (4, 5), 5)  # 4,0 has nothing and 4,5 has [G, R, R, R, R, R, G]

        # green on bottom means reserve and capture [G, R]

        self.assertEqual(message_success, MESSAGES['move_success'])
        self.assertListEqual(game.show_pieces((4, 0)), [])
        self.assertListEqual(game.show_pieces((4, 5)), ['R', 'R', 'R', 'R', 'G'])
        self.assertEqual(game.show_reserve('george'), 1)
        self.assertEqual(game.show_captured('george'), 1)

    def test_add_2_into_capture_success_default_settings(self):
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 1, 0 has [R, R]
        game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 1,0 has [R, R, G]
        game.move_piece('ralph', (5, 0), (4, 0), 1)  # 5,0 has nothing and 4,0 has [R, R]
        game.move_piece('george', (1, 0), (4, 0), 3)  # 1,0 has nothing and 4,0 has [R, R, R, R, G]
        game.move_piece('ralph', (4, 4), (5, 4), 1)  # 4,4 has nothing and 5,4 has [R, R]
        message_success = game.move_piece('george', (4, 0), (5, 4), 5)  # 4,1 has nothing and  has [R, R, R, R, R, R, G]

        # red on bottom means capture [R, R]

        self.assertEqual(message_success, MESSAGES['move_success'])
        self.assertListEqual(game.show_pieces((4, 0)), [])
        self.assertListEqual(game.show_pieces((5, 4)), ['R', 'R', 'R', 'R', 'G'])
        self.assertEqual(game.show_captured('george'), 2)

    def test_add_2_into_reserve_success_default_settings(self):
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 1, 0 has [R, R]
        game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 1,0 has [R, R, G]
        game.move_piece('ralph', (5, 0), (4, 0), 1)  # 5,0 has nothing and 4,0 has [R, R]
        game.move_piece('george', (1, 0), (4, 0), 3)  # 1,0 has nothing and 4,0 has [R, R, R, R, G]
        game.move_piece('ralph', (4, 4), (5, 4), 1)  # 4,4 has nothing and 5,4 has [R, R]
        game.move_piece('george', (5, 5), (4, 5), 1)  # 5,5 has nothing and 4,5 has [G, G]
        game.move_piece('ralph', (0, 2), (0, 3), 1)  # 0,2 has nothing and 0,3 has [G, R]
        message_success = game.move_piece('george', (4, 0), (4, 5), 5)  # 4,0 has nothing and 4,5 has [G, G, R, R, R, R, G]

        # green on bottom means reserve [G, G] (lol)

        self.assertEqual(message_success, MESSAGES['move_success'])
        self.assertListEqual(game.show_pieces((4, 0)), [])
        self.assertListEqual(game.show_pieces((4, 5)), ['R', 'R', 'R', 'R', 'G'])
        self.assertEqual(game.show_reserve('george'), 2)

    def test_make_reserved_move_success_default_settings(self):
        game = initialize_basic_game()
        game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 1, 0 has [R, R]
        game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 1,0 has [R, R, G]
        game.move_piece('ralph', (5, 0), (4, 0), 1)  # 5,0 has nothing and 4,0 has [R, R]
        game.move_piece('george', (1, 0), (4, 0), 3)  # 1,0 has nothing and 4,0 has [R, R, R, R, G]
        game.move_piece('ralph', (4, 4), (5, 4), 1)  # 4,4 has nothing and 5,4 has [R, R]
        game.move_piece('george', (5, 5), (4, 5), 1)  # 5,5 has nothing and 4,5 has [G, G]
        game.move_piece('ralph', (0, 2), (0, 3), 1)  # 0,2 has nothing and 0,3 has [G, R]
        message_success = game.move_piece('george', (4, 0), (4, 5), 5)  # 4,0 has nothing and 4,5 has [G, G, R, R, R, R, G]

        # green on bottom means reserve [G, G] (lol)
        self.assertEqual(message_success, MESSAGES['move_success'])
        self.assertListEqual(game.show_pieces((4, 0)), [])
        self.assertListEqual(game.show_pieces((4, 5)), ['R', 'R', 'R', 'R', 'G'])
        self.assertEqual(game.show_reserve('george'), 2)

        # make reserved move
        game.move_piece('ralph', (0, 3), (0, 4), 1)  # 0,3 has [G] and 0,4 has [R, R]
        game.reserved_move('george', (4, 5))  # 4,5 has [R, R, R, R, G, G] and reserve = 1 and captured = 1

        self.assertEqual(game.show_reserve('george'), 1)
        self.assertEqual(game.show_captured('george'), 1)
        self.assertListEqual(game.show_pieces((4, 5)), ['R', 'R', 'R', 'G', 'G'])

    def test_victory_default_settings(self):
        game = initialize_basic_game()
        game._players['george']['captured'] = 5  # 1 more piece needed for victory

        game.move_piece('ralph', (0, 0), (1, 0), 1)  # 0,0 has nothing and 1, 0 has [R, R]
        game.move_piece('george', (2, 0), (1, 0), 1)  # 2,0 has nothing and 1,0 has [R, R, G]
        game.move_piece('ralph', (5, 0), (4, 0), 1)  # 5,0 has nothing and 4,0 has [R, R]
        game.move_piece('george', (1, 0), (4, 0), 3)  # 1,0 has nothing and 4,0 has [R, R, R, R, G]
        game.move_piece('ralph', (4, 4), (5, 4), 1)  # 4,4 has nothing and 5,4 has [R, R]
        message_win = game.move_piece('george', (4, 0), (5, 4), 5)  # 4,1 has nothing and  has [R, R, R, R, R, R, G]

        # red on bottom means capture [R, R]

        self.assertEqual(message_win, 'george Wins')
        self.assertListEqual(game.show_pieces((4, 0)), [])
        self.assertListEqual(game.show_pieces((5, 4)), ['R', 'R', 'R', 'R', 'G'])
        self.assertEqual(game.show_captured('george'), 7)


if __name__ == '__main__':
    unittest.main()
