import pygame
import sys
import math
import random

from modules.shared import clock, draw_test_overlay
from modules.graphs.breadth_first_search import BreadthFirstSearch
from tests.graphs.test_breadth_first_search import TestBreadthFirstSearch
from modules.graphs.depth_first_search import DepthFirstSearch
from tests.graphs.test_depth_first_search import TestDepthFirstSearch
from modules.graphs.priority_queue import PriorityQueue, Event
from tests.graphs.test_priority_queue import TestPriorityQueue
from modules.graphs.grid_path_counter import CountGridPaths
from tests.graphs.test_grid_path_counter import TestCountGridPaths

GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E'],
}

NODE_POSITIONS = {
    'A': (0.15, 0.25),
    'B': (0.38, 0.15),
    'C': (0.38, 0.50),
    'D': (0.60, 0.25),
    'E': (0.75, 0.38),
    'F': (0.60, 0.75),
}

NODE_R = 24


def _make_visualisation(screen, font, algorithm_fn, test_class, label):
    WIDTH, HEIGHT   = screen.get_size()
    running         = True
    start_node      = 'A'
    traversal_order = []
    visited_final   = set()

    def pos(node):
        fx, fy = NODE_POSITIONS[node]
        return (int(fx * WIDTH), int(fy * HEIGHT))

    def node_at(mx, my):
        for node in GRAPH:
            nx, ny = pos(node)
            if (mx - nx) ** 2 + (my - ny) ** 2 <= NODE_R ** 2:
                return node
        return None

    def draw_graph(visited=None, frontier=None, current=None):
        visited  = visited  or set()
        frontier = frontier or set()

        screen.fill((30, 32, 40))

        drawn = set()
        for node, neighbours in GRAPH.items():
            x1, y1 = pos(node)
            for nb in neighbours:
                pair = frozenset((node, nb))
                if pair in drawn:
                    continue
                drawn.add(pair)
                x2, y2 = pos(nb)
                color = (100, 210, 130) if (node in visited and nb in visited) \
                        else (120, 120, 150)
                pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)

        for node in GRAPH:
            x, y = pos(node)
            if node == current:
                color = (230,  90,  90)
            elif node in frontier:
                color = (230, 180,  60)
            elif node in visited:
                color = ( 80, 200, 120)
            else:
                color = ( 70,  80, 110)

            pygame.draw.circle(screen, color, (x, y), NODE_R)

            ring_color = (255, 255,  80) if node == start_node else (255, 255, 255)
            ring_width = 3              if node == start_node else 1
            pygame.draw.circle(screen, ring_color, (x, y), NODE_R, ring_width)

            lbl = font.render(node, True, (230, 230, 230))
            screen.blit(lbl, lbl.get_rect(center=(x, y)))

        if traversal_order:
            arrow_str = ", ".join(traversal_order)
            prefix    = font.render("Order: ", True, (160, 160, 190))
            order_str = font.render(arrow_str, True, (200, 220, 255))
            screen.blit(prefix,    (10, HEIGHT - 52))
            screen.blit(order_str, (10 + prefix.get_width(), HEIGHT - 52))

        legend = [
            ((255, 255, 80), "Start"),
            ((230, 90, 90), "Current"),
            ((230, 180, 60), "Frontier"),
            ((80, 200, 120), "Visited"),
            ((70, 80, 110), "Unvisited"),
        ]
        lx, ly = 10, HEIGHT - 52 - len(legend) * 22 - 12
        for color, lname in legend:
            pygame.draw.circle(screen, color, (lx + 8, ly + 8), 7)
            t = font.render(lname, True, (180, 180, 200))
            screen.blit(t, (lx + 22, ly))
            ly += 22

        info = font.render(
            f"SPACE or Click: Run {label} | Click Node: Set Start | R: Reset | T: Tests | ESC: Menu",
            True, (180, 180, 200)
        )
        screen.blit(info, (10, 10))
        pygame.display.flip()

    def run_search():
        nonlocal traversal_order, visited_final
        traversal_order = []
        visited_final   = set()

        def tracking_draw(visited, frontier, current):
            if current is not None and current not in traversal_order:
                traversal_order.append(current)
            visited_final.update(visited)
            draw_graph(visited=visited, frontier=frontier, current=current)

        draw_graph()
        pygame.time.wait(400)
        algorithm_fn(GRAPH, start_node, tracking_draw, pygame.time.wait, check_events)
        draw_graph(visited=visited_final)

    def check_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    draw_graph()

    while running:
        pygame.time.wait(16)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = node_at(*event.pos)
                if clicked:
                    start_node = clicked
                    traversal_order = []
                    visited_final   = set()
                    draw_graph()
                    pygame.time.wait(120)
                    run_search()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    run_search()
                elif event.key == pygame.K_r:
                    traversal_order = []
                    visited_final   = set()
                    draw_graph()
                elif event.key == pygame.K_t:
                    draw_test_overlay(screen, font, test_class, label)

        draw_graph(visited=visited_final)


def breadth_first_search_visualisation(screen, font):
    _make_visualisation(screen, font, BreadthFirstSearch, TestBreadthFirstSearch, "BFS")


def depth_first_search_visualisation(screen, font):
    _make_visualisation(screen, font, DepthFirstSearch, TestDepthFirstSearch, "DFS")


def priority_queue_visualisation(screen, font):
    WIDTH, HEIGHT = screen.get_size()
    queue = PriorityQueue()
    running = True
    processed_event = None

    pending_events = [
        Event(12, "Spawn Enemy"),
        Event(4, "Play Sound"),
        Event(20, "Boss Appears"),
        Event(2, "Load Assets"),
        Event(8, "Open Door"),
        Event(15, "Trigger Alarm"),
        Event(1, "Game Start"),
        Event(10, "NPC Dialogue"),
    ]

    insertion_index = 0

    def draw_heap(heap, highlight_indices=None, active_event=None):

        highlight_indices = highlight_indices or []

        screen.fill((30, 32, 40))

        if not heap:

            empty = font.render(
                "No Scheduled Events",
                True,
                (180, 180, 180),
            )

            screen.blit(empty, (WIDTH // 2 - 90, 120))

        node_positions = []

        if heap:

            for i in range(len(heap)):

                level = int(math.floor(math.log2(i + 1)))
                index_in_level = i - (2 ** level - 1)

                gap = WIDTH // (2 ** level + 1)

                x = gap * (index_in_level + 1)
                y = 100 + level * 90

                node_positions.append((x, y))

            for i in range(len(heap)):

                left = 2 * i + 1
                right = 2 * i + 2

                if left < len(heap):
                    pygame.draw.line(
                        screen,
                        (120, 120, 150),
                        node_positions[i],
                        node_positions[left],
                        2,
                    )

                if right < len(heap):
                    pygame.draw.line(
                        screen,
                        (120, 120, 150),
                        node_positions[i],
                        node_positions[right],
                        2,
                    )

            for i, event in enumerate(heap):

                if i in highlight_indices:
                    color = (230, 90, 90)
                else:
                    color = (80, 200, 120)

                pygame.draw.circle(
                    screen,
                    color,
                    node_positions[i],
                    28,
                )

                pygame.draw.circle(
                    screen,
                    (255, 255, 255),
                    node_positions[i],
                    28,
                    2,
                )

                text = font.render(
                    str(event.time),
                    True,
                    (20, 20, 20),
                )

                text_rect = text.get_rect(
                    center=node_positions[i]
                )

                screen.blit(text, text_rect)

        panel_x = WIDTH - 260

        panel_title = font.render(
            "Upcoming Events",
            True,
            (255, 255, 255),
        )

        screen.blit(panel_title, (panel_x, 60))

        sorted_events = sorted(heap, key=lambda e: e.time)

        y = 95

        for event in sorted_events[:8]:

            line = font.render(
                f"{event.time}: {event.description}",
                True,
                (200, 220, 255),
            )

            screen.blit(line, (panel_x, y))

            y += 28

        if active_event:

            current_title = font.render(
                "Processing Event",
                True,
                (255, 210, 120),
            )

            screen.blit(current_title, (20, HEIGHT - 110))

            current_text = font.render(
                f"{active_event.time}: {active_event.description}",
                True,
                (255, 255, 255),
            )

            screen.blit(current_text, (20, HEIGHT - 75))

        info = font.render(
            "SPACE: Schedule Event | E: Process Event | R: Reset | T: Tests | ESC: Back",
            True,
            (180, 180, 200),
        )

        screen.blit(info, (10, 10))

        pygame.display.flip()

    draw_heap(queue.heap)

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:

                    if insertion_index < len(pending_events):

                        queue.insert(
                            pending_events[insertion_index],
                            draw_fn=draw_heap,
                            wait_fn=pygame.time.wait,
                        )

                        insertion_index += 1

                elif event.key == pygame.K_e:

                    if not queue.is_empty():

                        processed_event = queue.extract_min(
                            draw_fn=draw_heap,
                            wait_fn=pygame.time.wait,
                        )

                        draw_heap(
                            queue.heap,
                            [],
                            processed_event,
                        )

                        pygame.time.wait(800)

                elif event.key == pygame.K_r:

                    queue = PriorityQueue()

                    processed_event = None

                    insertion_index = 0

                    pending_events = [
                        Event(12, "Spawn Enemy"),
                        Event(4,  "Play Sound"),
                        Event(20, "Boss Appears"),
                        Event(2,  "Load Assets"),
                        Event(8,  "Open Door"),
                        Event(15, "Trigger Alarm"),
                        Event(1,  "Game Start"),
                        Event(10, "NPC Dialogue"),
                    ]
                
                elif event.key == pygame.K_t:

                    draw_test_overlay(
                        screen,
                        font,
                        TestPriorityQueue,
                        "Priority Queue",
                    )

        draw_heap(queue.heap, [], processed_event)

        clock.tick(30)


def grid_path_counting_visualisation(screen, font):
    WIDTH, HEIGHT = screen.get_size()

    ROWS, COLS = 6, 6
    CELL_SIZE = min(WIDTH // COLS - 13, HEIGHT // ROWS - 13)

    OFFSET_X = (WIDTH - CELL_SIZE * COLS) // 2
    OFFSET_Y = (HEIGHT - CELL_SIZE * ROWS) // 2

    OBSTACLE_RATE = 0.25

    running = True
    running_sim = False
    step_index = 0

    dp = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    parent = [[None for _ in range(COLS)] for _ in range(ROWS)]
    path = set()

    def new_grid():
        g = [[-1 if random.random() < OBSTACLE_RATE else 0
              for _ in range(COLS)] for _ in range(ROWS)]

        g[0][0] = 0
        g[ROWS - 1][COLS - 1] = 0
        return g

    grid = new_grid()

    def has_path(g):
        test = [[0] * COLS for _ in range(ROWS)]
        if g[0][0] == -1:
            return False

        test[0][0] = 1
        for r in range(ROWS):
            for c in range(COLS):
                if g[r][c] == -1:
                    continue
                if r > 0:
                    test[r][c] += test[r - 1][c]
                if c > 0:
                    test[r][c] += test[r][c - 1]

        return test[ROWS - 1][COLS - 1] > 0

    while not has_path(grid):
        grid = new_grid()

    def rect(r, c):
        return pygame.Rect(
            OFFSET_X + c * CELL_SIZE,
            OFFSET_Y + r * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

    def draw(visited=None, current=None):
        visited = visited or set()

        screen.fill((30, 32, 40))

        for r in range(ROWS):
            for c in range(COLS):
                rct = rect(r, c)

                if grid[r][c] == -1:
                    color = (40, 40, 50)
                elif (r, c) in path:
                    color = (80, 200, 120)
                else:
                    color = (60, 60, 75)

                if current == (r, c):
                    color = (230, 90, 90)

                pygame.draw.rect(screen, color, rct, border_radius=6)
                pygame.draw.rect(screen, (90, 90, 110), rct, 1, border_radius=6)

                if dp[r][c] > 0:
                    txt = font.render(str(dp[r][c]), True, (220, 220, 230))
                    screen.blit(txt, txt.get_rect(center=rct.center))

        legend = [
            ((230, 90, 90), "Current"),
            ((80, 200, 120), "Path"),
            ((60, 60, 75), "Unvisited"),
            ((40, 40, 50), "Obstacle"),
        ]

        lx, ly = 10, HEIGHT - 20 - len(legend) * 22

        for color, name in legend:
            pygame.draw.circle(screen, color, (lx + 8, ly + 8), 7)
            t = font.render(name, True, (180, 180, 200))
            screen.blit(t, (lx + 22, ly))
            ly += 22

        info = font.render(
            f"SPACE: Run | R: Reset | T: Tests | ESC: Menu",
            True,
            (180, 180, 200)
        )
        screen.blit(info, (10, 10))

        pygame.display.flip()

    def step(r, c):
        if grid[r][c] == -1:
            return

        if r == 0 and c == 0:
            dp[r][c] = 1
        else:
            ways = 0

            if r > 0 and grid[r - 1][c] != -1:
                ways += dp[r - 1][c]
                if dp[r - 1][c] > 0:
                    parent[r][c] = (r - 1, c)

            if c > 0 and grid[r][c - 1] != -1:
                ways += dp[r][c - 1]
                if dp[r][c - 1] > 0:
                    parent[r][c] = (r, c - 1)

            dp[r][c] = ways

    def run():
        nonlocal step_index, path, running_sim

        running_sim = True
        step_index = 0
        path = set()

        dp[:] = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        parent[:] = [[None for _ in range(COLS)] for _ in range(ROWS)]

        while step_index < ROWS * COLS:
            pygame.time.wait(40)

            r = step_index // COLS
            c = step_index % COLS

            step(r, c)

            draw(current=(r, c))
            step_index += 1

        # reconstruct path
        if dp[ROWS - 1][COLS - 1] > 0:
            r, c = ROWS - 1, COLS - 1
            while True:
                path.add((r, c))
                if parent[r][c] is None:
                    break
                r, c = parent[r][c]

        running_sim = False

    def reset():
        nonlocal grid, dp, parent, path, step_index, running_sim

        grid = new_grid()
        while not has_path(grid):
            grid = new_grid()

        dp = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        parent = [[None for _ in range(COLS)] for _ in range(ROWS)]
        path = set()
        step_index = 0
        running_sim = False

    draw()

    while running:
        pygame.time.wait(16)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    run()
                elif event.key == pygame.K_r:
                    reset()
                    draw()
                elif event.key == pygame.K_t:
                    draw_test_overlay(
                        screen,
                        font,
                        TestCountGridPaths,
                        "Grid Path Counter",
                    )

        draw()


def run(screen):
    font = pygame.font.SysFont(None, 28)
    menu_items = [
        "Breadth First Search Visualisation",
        "Depth First Search Visualisation",
        "Priority Queue Visualisation",
        "Grid Path Counting Visualisation",
        "Back",
    ]
    selected = 0
    running = True

    while running:
        screen.fill((220, 220, 220))
        for i, item in enumerate(menu_items):
            color = (255, 0, 0) if i == selected else (0, 0, 0)
            text = font.render(item, True, color)
            screen.blit(text, (100, 100 + i * 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_items)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    choice = menu_items[selected]
                    if choice == "Breadth First Search Visualisation":
                        breadth_first_search_visualisation(screen, font)
                    elif choice == "Depth First Search Visualisation":
                        depth_first_search_visualisation(screen, font)
                    elif choice == "Priority Queue Visualisation":
                        priority_queue_visualisation(screen, font)
                    elif choice == "Grid Path Counting Visualisation":
                        grid_path_counting_visualisation(screen, font)
                    elif choice == "Back":
                        running = False
        clock.tick(30)