"""Pygame grid simulation for A* autonomous navigation."""
import random
import pygame
from src.path_planning import astar_path

ROWS, COLS, CELL, PANEL = 22, 30, 28, 220
WIDTH, HEIGHT, FPS = COLS * CELL + PANEL, ROWS * CELL, 60
BG, GRID = (246, 248, 251), (215, 220, 228)
OBSTACLE, PATH = (66, 75, 90), (255, 197, 74)
START, GOAL, ROBOT = (54, 174, 111), (224, 83, 83), (48, 115, 220)
TEXT, WHITE = (35, 43, 55), (255, 255, 255)

def build_obstacles():
    rng = random.Random(17)
    blocked = {(rng.randrange(ROWS), rng.randrange(COLS)) for _ in range(115)}
    start, goal = (1, 1), (ROWS - 2, COLS - 2)
    blocked.discard(start); blocked.discard(goal)
    for c in range(1, 8): blocked.discard((1, c))
    for r in range(1, ROWS - 1): blocked.discard((r, 7))
    for c in range(7, COLS - 1): blocked.discard((ROWS - 2, c))
    return blocked

def run_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI-Based Autonomous Navigation System | A*")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoeui", 18)
    small = pygame.font.SysFont("segoeui", 15)
    start, goal = (1, 1), (ROWS - 2, COLS - 2)
    obstacles = build_obstacles()
    path = astar_path(ROWS, COLS, start, goal, obstacles)
    index, elapsed, paused, running = 0, 0, False, True
    status_message = ""

    def rect(cell):
        r, c = cell
        return pygame.Rect(c * CELL, r * CELL, CELL, CELL)

    while running:
        elapsed += clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE): running = False
                elif event.key == pygame.K_SPACE: paused = not paused
                elif event.key == pygame.K_r:
                    obstacles = build_obstacles()
                    path = astar_path(ROWS, COLS, start, goal, obstacles)
                    index, status_message = 0, "Simulation reset"
                elif event.key == pygame.K_n and path:
                    candidate = path[min(index + 3, len(path) - 1)]
                    if candidate not in (start, goal):
                        obstacles.add(candidate)
                        path = astar_path(ROWS, COLS, start, goal, obstacles)
                        index, status_message = 0, "Obstacle added; route replanned"
        if not paused and path and index < len(path) - 1 and elapsed >= 90:
            index += 1; elapsed = 0

        screen.fill(BG)
        for r in range(ROWS):
            for c in range(COLS):
                cell = (r, c); box = rect(cell)
                if cell in obstacles:
                    pygame.draw.rect(screen, OBSTACLE, box.inflate(-2, -2), border_radius=4)
                pygame.draw.rect(screen, GRID, box, 1)
        for cell in path:
            pygame.draw.rect(screen, PATH, rect(cell).inflate(-8, -8), border_radius=5)
        pygame.draw.rect(screen, START, rect(start).inflate(-3, -3), border_radius=5)
        pygame.draw.rect(screen, GOAL, rect(goal).inflate(-3, -3), border_radius=5)
        if path:
            robot = rect(path[min(index, len(path)-1)])
            pygame.draw.circle(screen, ROBOT, robot.center, CELL // 3)
            pygame.draw.circle(screen, WHITE, robot.center, CELL // 3, 2)

        px, y = COLS * CELL + 16, 22
        pygame.draw.rect(screen, WHITE, pygame.Rect(COLS * CELL, 0, PANEL, HEIGHT))
        labels = [
            ("AUTONOMOUS NAVIGATION", font), ("A* path planning demo", small), ("", small),
            ("CONTROLS", font), ("SPACE  Pause / resume", small), ("R  Reset", small),
            ("N  Add obstacle + replan", small), ("Q / ESC  Quit", small), ("", small),
            ("LEGEND", font)
        ]
        for label, f in labels:
            if label: screen.blit(f.render(label, True, TEXT), (px, y))
            y += 25 if f == font else 22
        for color, label in [(START,"Start"),(GOAL,"Destination"),(OBSTACLE,"Obstacle"),(PATH,"Planned path"),(ROBOT,"Virtual robot")]:
            pygame.draw.rect(screen, color, pygame.Rect(px, y+2, 15, 15), border_radius=3)
            screen.blit(small.render(label, True, TEXT), (px+24, y)); y += 25
        y += 12
        screen.blit(font.render("RUN STATUS", True, TEXT), (px, y)); y += 30
        status = "No route found" if not path else ("Goal reached!" if index >= len(path)-1 else "Navigating...")
        screen.blit(small.render(status, True, TEXT), (px, y)); y += 25
        if path:
            screen.blit(small.render(f"Path cells: {len(path)}", True, TEXT), (px, y)); y += 22
            screen.blit(small.render(f"Robot step: {index+1}/{len(path)}", True, TEXT), (px, y)); y += 25
        if paused: screen.blit(font.render("PAUSED", True, GOAL), (px, y)); y += 25
        if status_message: screen.blit(small.render(status_message[:26], True, ROBOT), (px, y))
        pygame.display.flip()
    pygame.quit()
