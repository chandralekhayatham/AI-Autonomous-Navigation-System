import unittest
from src.path_planning import astar_path

class TestAStar(unittest.TestCase):
    def test_shortest_open_grid(self):
        path = astar_path(5, 5, (0, 0), (4, 4), set())
        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (4, 4))
        self.assertEqual(len(path), 9)

    def test_avoids_obstacles(self):
        blocked = {(1, 0), (1, 1), (1, 2)}
        path = astar_path(4, 4, (0, 0), (3, 0), blocked)
        self.assertTrue(path)
        self.assertTrue(all(cell not in blocked for cell in path))

    def test_unreachable_goal(self):
        self.assertEqual(astar_path(3, 3, (0, 0), (2, 2), {(0, 1), (1, 0)}), [])

if __name__ == "__main__":
    unittest.main()
