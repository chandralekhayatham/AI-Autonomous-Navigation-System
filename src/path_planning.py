"""A* path planning for a 2D grid."""
import heapq
from typing import Iterable
Cell = tuple[int, int]

def heuristic(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_path(rows: int, cols: int, start: Cell, goal: Cell, obstacles: Iterable[Cell]) -> list[Cell]:
    """Return a shortest 4-directional path including start and goal, or [] if unreachable."""
    blocked = set(obstacles)
    for point in (start, goal):
        if not (0 <= point[0] < rows and 0 <= point[1] < cols):
            raise ValueError("Start and goal must be inside the grid.")
    if start in blocked or goal in blocked:
        return []
    frontier = [(heuristic(start, goal), 0, start)]
    came_from = {start: None}
    costs = {start: 0}
    counter = 0
    for_priority_directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    while frontier:
        _, _, current = heapq.heappop(frontier)
        if current == goal:
            break
        for dr, dc in for_priority_directions:
            nxt = (current[0] + dr, current[1] + dc)
            if not (0 <= nxt[0] < rows and 0 <= nxt[1] < cols) or nxt in blocked:
                continue
            new_cost = costs[current] + 1
            if nxt not in costs or new_cost < costs[nxt]:
                costs[nxt] = new_cost
                came_from[nxt] = current
                counter += 1
                heapq.heappush(frontier, (new_cost + heuristic(nxt, goal), counter, nxt))
    if goal not in came_from:
        return []
    path, current = [], goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    return path[::-1]
