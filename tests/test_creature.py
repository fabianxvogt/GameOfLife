import unittest

from creatures.creature import Creature


class CreatureTest(unittest.TestCase):
    def test_copy_isolates_nested_state(self):
        original = Creature([[True, False], [False, True]])

        copied = original.copy()
        copied.state[0][0] = False
        copied.state[1].append(True)

        self.assertEqual(original.state, [[True, False], [False, True]])
        self.assertEqual(copied.state, [[False, False], [False, True, True]])


if __name__ == "__main__":
    unittest.main()
