import collections


def BreadthFirstSearch(graph, start, draw_fn, wait_fn, event_fn):
    visited = set()
    queue = collections.deque([start])
    frontier = {start}

    while queue:
        current = queue.popleft()
        frontier.discard(current)
        visited.add(current)

        draw_fn(visited=visited, frontier=frontier, current=current)
        wait_fn(700)
        if not event_fn():
            return False

        for neighbour in graph[current]:
            if neighbour not in visited and neighbour not in frontier:
                frontier.add(neighbour)
                queue.append(neighbour)

    draw_fn(visited=visited, frontier=set(), current=None)
    return True