import unittest

from agent2048.env import Game2048Env


class TestEnv(unittest.TestCase):
    def test_reset_has_two_tiles(self):
        env = Game2048Env(size=4, seed=1)
        board = env.reset()
        non_zero = sum(1 for row in board for value in row if value != 0)
        self.assertEqual(non_zero, 2)

    def test_step_returns_result(self):
        env = Game2048Env(size=4, seed=1)
        env.reset()
        result = env.step("a")
        self.assertEqual(len(result.board), 4)


if __name__ == "__main__":
    unittest.main()
