import pygame
import sys
import random

from modules.shared import (
    clock, draw_test_overlay,
    ease_out_cubic, ease_out_back, ease_in_cubic, ease_out_bounce,
    AnimManager, make_block, draw_block,
    WIDTH, HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT, START_X, BASE_Y,
)
from modules.data_structures.stack import Stack
from tests.data_structures.test_stack import TestStack
from modules.data_structures.queue import Queue
from tests.data_structures.test_queue import TestQueue
from modules.data_structures.linked_list import LinkedList
from tests.data_structures.test_linked_list import TestLinkedList
from modules.data_structures.binary_search_tree import BinarySearchTree
from tests.data_structures.test_binary_search_tree import TestBinarySearchTree


def stack_visualisation(screen, font):
    stack = Stack()
    anim = AnimManager()
    blocks = []
    counter = 1
    running = True
    PUSH_DUR = 0.22
    POP_DUR  = 0.18

    def target_y(i):
        return BASE_Y - i * (BLOCK_HEIGHT + 5)

    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stack.push(counter)
                    idx = len(blocks)
                    ty = target_y(idx)
                    b = make_block(counter, START_X, ty - 80, alpha=0, scale=0.6)
                    blocks.append(b)
                    anim.tween(b, "y",     ty - 80, ty,   PUSH_DUR, ease_out_back)
                    anim.tween(b, "alpha", 0,       255,  PUSH_DUR)
                    anim.tween(b, "scale", 0.6,     1.0,  PUSH_DUR, ease_out_back)
                    counter += 1

                elif event.key == pygame.K_BACKSPACE and not stack.is_empty():
                    stack.pop()
                    if blocks:
                        b = blocks.pop()
                        ghost = dict(b)
                        ghost["value"] = b["value"]
                        anim.tween(ghost, "y",     b["y"], b["y"] - 60, POP_DUR, ease_in_cubic)
                        anim.tween(ghost, "alpha", 255,    0,           POP_DUR, ease_in_cubic)
                        anim.tween(ghost, "scale", 1.0,   0.5,         POP_DUR)
                        b["_ghost"] = ghost

                elif event.key == pygame.K_t:
                    draw_test_overlay(screen, font, TestStack, "Stack")
                elif event.key == pygame.K_ESCAPE:
                    running = False

        anim.update(dt)
        screen.fill((30, 32, 40))

        for b in blocks:
            draw_block(screen, font, b)

        info_text = font.render(
            "SPACE: Push | BACKSPACE: Pop | T: Run Tests | ESC: Menu",
            True, (180, 180, 200)
        )
        screen.blit(info_text, (10, 10))
        pygame.display.flip()


def queue_visualisation(screen, font):
    queue = Queue()
    anim = AnimManager()
    blocks = []
    ghosts = []
    counter = 1
    running = True
    ENQUEUE_DUR = 0.24
    DEQUEUE_DUR = 0.20
    SHIFT_DUR   = 0.22
    BLOCK_GAP   = 10
    COL_STEP    = BLOCK_WIDTH + BLOCK_GAP

    def target_pos(i):
        cols = max(1, (WIDTH - 40) // COL_STEP)
        col = i % cols
        row = i // cols
        x = 20 + col * COL_STEP
        y = 60 + row * (BLOCK_HEIGHT + BLOCK_GAP)
        return float(x), float(y)

    def reflow(start_idx=0, delay_per=0.0):
        for idx in range(start_idx, len(blocks)):
            b = blocks[idx]
            tx, ty = target_pos(idx)
            anim.tween(b, "x", b["x"], tx, SHIFT_DUR, ease_out_cubic, delay=idx * delay_per)
            anim.tween(b, "y", b["y"], ty, SHIFT_DUR, ease_out_cubic, delay=idx * delay_per)

    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    queue.enqueue(counter)
                    idx = len(blocks)
                    tx, ty = target_pos(idx)
                    b = make_block(counter, float(WIDTH + 20), ty, alpha=0)
                    blocks.append(b)
                    anim.tween(b, "x",     WIDTH + 20, tx,  ENQUEUE_DUR, ease_out_cubic)
                    anim.tween(b, "alpha", 0,          255, ENQUEUE_DUR)
                    anim.tween(b, "scale", 0.6,        1.0, ENQUEUE_DUR, ease_out_back)
                    counter += 1

                elif event.key == pygame.K_BACKSPACE and not queue.is_empty():
                    queue.dequeue()
                    if blocks:
                        b = blocks.pop(0)
                        ghost = dict(b)
                        ghosts.append(ghost)
                        anim.tween(ghost, "x",     ghost["x"], ghost["x"] - 80, DEQUEUE_DUR, ease_in_cubic)
                        anim.tween(ghost, "alpha", 255,        0,               DEQUEUE_DUR)
                        anim.tween(ghost, "scale", 1.0,        0.4,             DEQUEUE_DUR)
                        reflow()

                elif event.key == pygame.K_t:
                    draw_test_overlay(screen, font, TestQueue, "Queue")
                elif event.key == pygame.K_ESCAPE:
                    running = False

        anim.update(dt)
        ghosts = [g for g in ghosts if g["alpha"] > 1]
        screen.fill((30, 32, 40))

        if blocks:
            fx, fy = blocks[0]["x"], blocks[0]["y"]
            lbl = font.render("FRONT", True, (100, 230, 130))
            screen.blit(lbl, (int(fx), int(fy) - 20))
            bx, by = blocks[-1]["x"], blocks[-1]["y"]
            lbl2 = font.render("BACK", True, (230, 160, 80))
            screen.blit(lbl2, (int(bx) + 140, int(by) + 40))

        for b in blocks:
            draw_block(screen, font, b)
        for g in ghosts:
            draw_block(screen, font, g, color=(180, 100, 100))

        info_text = font.render(
            "SPACE: Enqueue | BACKSPACE: Dequeue | T: Run Tests | ESC: Menu",
            True, (180, 180, 200)
        )
        screen.blit(info_text, (10, 10))
        pygame.display.flip()


def linked_list_visualisation(screen, font):
    linkedlist = LinkedList()
    anim = AnimManager()
    blocks = []
    ghosts = []
    counter = 1
    running = True
    INSERT_DUR  = 0.26
    DELETE_DUR  = 0.20
    REFLOW_DUR  = 0.22
    STEP        = BLOCK_HEIGHT + 20

    input_active = False
    input_text   = ""

    def target_y(i, n):
        total = n * STEP
        start = (HEIGHT - total) // 2
        return float(start + i * STEP)

    def reflow(n_total):
        for i, b in enumerate(blocks):
            ty = target_y(i, n_total)
            anim.tween(b, "y", b["y"], ty, REFLOW_DUR, ease_out_cubic)

    def do_insert_front():
        nonlocal counter
        linkedlist.insert(counter)
        n = len(blocks) + 1
        ty = target_y(0, n)
        b = make_block(counter, float(START_X), ty - 60, alpha=0, scale=0.5)
        blocks.insert(0, b)
        anim.tween(b, "y",     ty - 60, ty,   INSERT_DUR, ease_out_back)
        anim.tween(b, "alpha", 0,       255,   INSERT_DUR)
        anim.tween(b, "scale", 0.5,     1.0,   INSERT_DUR, ease_out_back)
        reflow(n)
        counter += 1

    def do_insert_at(position):
        nonlocal counter
        pos = max(0, min(position, len(blocks)))
        linkedlist.insert(counter, pos)
        n  = len(blocks) + 1
        ty = target_y(pos, n)
        b  = make_block(counter, float(START_X), ty - 60, alpha=0, scale=0.5)
        blocks.insert(pos, b)
        anim.tween(b, "y",     ty - 60, ty,   INSERT_DUR, ease_out_back)
        anim.tween(b, "alpha", 0,       255,   INSERT_DUR)
        anim.tween(b, "scale", 0.5,     1.0,   INSERT_DUR, ease_out_back)
        reflow(n)
        counter += 1

    def draw_input_box():
        box_w, box_h = 320, 80
        bx = (WIDTH  - box_w) // 2
        by = (HEIGHT - box_h) // 2
        pygame.draw.rect(screen, (50, 54, 68), (bx, by, box_w, box_h), border_radius=8)
        pygame.draw.rect(screen, (120, 130, 200), (bx, by, box_w, box_h), 2, border_radius=8)
        prompt = font.render("Insert at position:", True, (200, 210, 255))
        screen.blit(prompt, (bx + 12, by + 10))
        entry = font.render(input_text + "|", True, (255, 255, 150))
        screen.blit(entry, (bx + 12, by + 44))

    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if input_text.lstrip("-").isdigit():
                            do_insert_at(int(input_text))
                        input_active = False
                        input_text   = ""
                    elif event.key == pygame.K_ESCAPE:
                        input_active = False
                        input_text   = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit():
                        input_text += event.unicode
                    continue

                if event.key == pygame.K_SPACE:
                    do_insert_front()
                elif event.key == pygame.K_i:
                    input_active = True
                    input_text   = ""
                elif event.key == pygame.K_BACKSPACE and not linkedlist.is_empty():
                    linkedlist.delete(position=0)
                    if blocks:
                        b = blocks.pop(0)
                        ghost = dict(b)
                        ghosts.append(ghost)
                        anim.tween(ghost, "x",     ghost["x"], ghost["x"] - 80, DELETE_DUR, ease_in_cubic)
                        anim.tween(ghost, "alpha", 255,        0,               DELETE_DUR)
                        anim.tween(ghost, "scale", 1.0,        0.3,             DELETE_DUR)
                        reflow(len(blocks))
                elif event.key == pygame.K_r:
                    linkedlist.reverse()
                    blocks.reverse()
                    reflow(len(blocks))
                elif event.key == pygame.K_t:
                    draw_test_overlay(screen, font, TestLinkedList, "Linked List")
                elif event.key == pygame.K_ESCAPE:
                    running = False

        anim.update(dt)
        ghosts = [g for g in ghosts if g["alpha"] > 1]
        screen.fill((30, 32, 40))

        for i in range(len(blocks) - 1):
            b_cur  = blocks[i]
            b_next = blocks[i + 1]
            cx = int(b_cur["x"])  + BLOCK_WIDTH // 2
            cy = int(b_cur["y"])  + BLOCK_HEIGHT
            nx = int(b_next["x"]) + BLOCK_WIDTH // 2
            ny = int(b_next["y"])
            alpha = int(min(b_cur["alpha"], b_next["alpha"]))
            if alpha > 10:
                line_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.line(line_surf, (200, 200, 200, alpha), (cx, cy), (nx, ny), 2)
                pygame.draw.polygon(line_surf, (200, 200, 200, alpha),
                                    [(nx - 5, ny - 8), (nx + 5, ny - 8), (nx, ny)])
                screen.blit(line_surf, (0, 0))

        for i, b in enumerate(blocks):
            draw_block(screen, font, b)
            if i == 0:
                lbl = font.render("HEAD", True, (100, 230, 130))
                screen.blit(lbl, (int(b["x"]) - 65, int(b["y"]) + BLOCK_HEIGHT // 4))
            if i == len(blocks) - 1:
                lbl2 = font.render("NULL", True, (230, 80, 80))
                screen.blit(lbl2, (int(b["x"]) + BLOCK_WIDTH + 10, int(b["y"]) + BLOCK_HEIGHT // 4))

        for g in ghosts:
            draw_block(screen, font, g, color=(180, 100, 100))

        if input_active:
            draw_input_box()

        info_text = font.render(
            "SPACE: Insert Front | I: Insert at pos | BACKSPACE: Delete Front | R: Reverse | T: Tests | ESC: Menu",
            True, (180, 180, 200)
        )
        screen.blit(info_text, (10, 10))
        pygame.display.flip()


def binary_search_tree_visualisation(screen, font):
    bst = BinarySearchTree()
    anim = AnimManager()
    node_anims  = {}
    ghost_nodes = []
    traversals  = ["inorder", "preorder", "postorder"]
    traversal_idx = 0
    running = True
    INSERT_DUR = 0.30
    DELETE_DUR = 0.22
    MOVE_DUR   = 0.28

    class BSTNodeAnim:
        def __init__(self, value):
            self.value = value
            self.alpha = 0.0
            self.scale = 0.0
            self.cx = 0.0
            self.cy = 0.0
            self.tx = 0.0
            self.ty = 0.0

    search_active = False
    search_text   = ""
    search_path   = []
    search_found  = None
    SEARCH_FADE   = 2.5
    search_timer  = 0.0

    delete_active = False
    delete_text   = ""

    NODE_R = 22

    def layout_positions(node, depth, left, right, positions):
        if node is None:
            return
        mid = (left + right) / 2
        positions[node.value] = (mid, 80 + depth * 70)
        layout_positions(node.left,  depth + 1, left, mid,   positions)
        layout_positions(node.right, depth + 1, mid,  right, positions)

    def sync_positions():
        positions = {}
        if not bst.is_empty():
            layout_positions(bst.root, 0, 0, WIDTH, positions)
        for val, (tx, ty) in positions.items():
            if val not in node_anims:
                na = BSTNodeAnim(val)
                na.cx, na.cy = float(tx), float(ty - 60)
                na.tx, na.ty = float(tx), float(ty)
                node_anims[val] = na
                anim.tween(na.__dict__, "cy",    na.cy,  na.ty,  INSERT_DUR, ease_out_bounce)
                anim.tween(na.__dict__, "alpha", 0,      255,    INSERT_DUR * 0.6)
                anim.tween(na.__dict__, "scale", 0.2,    1.0,    INSERT_DUR, ease_out_back)
            else:
                na = node_anims[val]
                na.tx, na.ty = float(tx), float(ty)
                anim.tween(na.__dict__, "cx", na.cx, na.tx, MOVE_DUR, ease_out_cubic)
                anim.tween(na.__dict__, "cy", na.cy, na.ty, MOVE_DUR, ease_out_cubic)

        dead = [v for v in list(node_anims.keys()) if v not in positions]
        for v in dead:
            na = node_anims.pop(v)
            ghost_nodes.append(na)
            anim.tween(na.__dict__, "alpha", na.alpha, 0,   DELETE_DUR)
            anim.tween(na.__dict__, "scale", na.scale, 0.0, DELETE_DUR, ease_in_cubic)

    def get_search_path(value):
        path = []
        node = bst.root
        while node is not None:
            path.append(node.value)
            if value == node.value:
                return path, True
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        return path, False

    def node_color(val):
        if search_path and search_timer > 0:
            t = min(search_timer / SEARCH_FADE, 1.0)
            if val == search_found:
                base = (60, 220, 100)
            elif val in search_path:
                base = (230, 170, 50)
            else:
                return (100, 150, 250)

            def lerp(a, b, f):
                return int(a + (b - a) * (1 - f))

            blue = (100, 150, 250)
            return (lerp(blue[0], base[0], t),
                    lerp(blue[1], base[1], t),
                    lerp(blue[2], base[2], t))
        return (100, 150, 250)

    def draw_node(na, ghost=False):
        alpha = max(0, min(255, int(na.alpha)))
        scale = max(0.0, na.scale)
        r = int(NODE_R * scale)
        if r < 1 or alpha == 0:
            return
        cx, cy = int(na.cx), int(na.cy)
        surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
        if ghost:
            color = (180, 80, 80, alpha)
        else:
            rc, gc, bc = node_color(na.value)
            color = (rc, gc, bc, alpha)
        pygame.draw.circle(surf, color, (r + 2, r + 2), r)
        pygame.draw.circle(surf, (255, 255, 255, max(0, alpha - 80)), (r + 2, r + 2), r, 2)
        screen.blit(surf, (cx - r - 2, cy - r - 2))
        txt = font.render(str(na.value), True, (20, 20, 20))
        txt.set_alpha(alpha)
        screen.blit(txt, txt.get_rect(center=(cx, cy)))

    def draw_edges(node, positions):
        if node is None:
            return
        for child in (node.left, node.right):
            if child is not None and node.value in positions and child.value in positions:
                px, py = positions[node.value]
                cx, cy = positions[child.value]
                a_p = int(node_anims.get(node.value, BSTNodeAnim(0)).alpha)
                a_c = int(node_anims.get(child.value, BSTNodeAnim(0)).alpha)
                alpha = min(a_p, a_c)

                on_path = (search_timer > 0 and
                           node.value in search_path and
                           child.value in search_path)
                t = min(search_timer / SEARCH_FADE, 1.0) if on_path else 0
                edge_r = int(100 + (230 - 100) * t)
                edge_g = int(160 + (170 - 160) * t)
                edge_b = int(200 + (50  - 200) * t)

                if alpha > 10:
                    line_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    width = 3 if on_path else 2
                    pygame.draw.line(line_surf, (edge_r, edge_g, edge_b, alpha),
                                     (int(px), int(py)), (int(cx), int(cy)), width)
                    screen.blit(line_surf, (0, 0))
            draw_edges(child, positions)

    def draw_input_box(prompt, text):
        box_w, box_h = 320, 80
        bx = (WIDTH  - box_w) // 2
        by = (HEIGHT - box_h) // 2
        pygame.draw.rect(screen, (50, 54, 68),    (bx, by, box_w, box_h), border_radius=8)
        pygame.draw.rect(screen, (120, 130, 200), (bx, by, box_w, box_h), 2, border_radius=8)
        p = font.render(prompt, True, (200, 210, 255))
        screen.blit(p, (bx + 12, by + 10))
        e = font.render(text + "|", True, (255, 255, 150))
        screen.blit(e, (bx + 12, by + 44))

    while running:
        dt = clock.tick(60) / 1000.0
        if search_timer > 0:
            search_timer = max(0.0, search_timer - dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if search_active:
                    if event.key == pygame.K_RETURN:
                        if search_text.lstrip("-").isdigit():
                            val = int(search_text)
                            search_path, found = get_search_path(val)
                            search_found  = val if found else None
                            search_timer  = SEARCH_FADE
                        search_active = False
                        search_text   = ""
                    elif event.key == pygame.K_ESCAPE:
                        search_active = False
                        search_text   = ""
                    elif event.key == pygame.K_BACKSPACE:
                        search_text = search_text[:-1]
                    elif event.unicode.isdigit():
                        search_text += event.unicode
                    continue

                if delete_active:
                    if event.key == pygame.K_RETURN:
                        if delete_text.lstrip("-").isdigit():
                            val = int(delete_text)
                            deleted = bst.delete(val)
                            if deleted:
                                if val in search_path:
                                    search_path  = []
                                    search_found = None
                                    search_timer = 0.0
                                sync_positions()
                        delete_active = False
                        delete_text   = ""
                    elif event.key == pygame.K_ESCAPE:
                        delete_active = False
                        delete_text   = ""
                    elif event.key == pygame.K_BACKSPACE:
                        delete_text = delete_text[:-1]
                    elif event.unicode.isdigit():
                        delete_text += event.unicode
                    continue

                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    bst.insert(random.randint(1, 99))
                    sync_positions()
                elif event.key == pygame.K_BACKSPACE and not bst.is_empty():
                    inorder = bst.inorder()
                    if inorder:
                        bst.delete(inorder[0])
                        sync_positions()
                elif event.key == pygame.K_d:
                    delete_active = True
                    delete_text   = ""
                elif event.key == pygame.K_s:
                    search_active = True
                    search_text   = ""
                elif event.key == pygame.K_t:
                    draw_test_overlay(screen, font, TestBinarySearchTree, "Binary Search Tree")
                elif event.key == pygame.K_v:
                    traversal_idx = (traversal_idx + 1) % len(traversals)

        anim.update(dt)
        ghost_nodes[:] = [g for g in ghost_nodes if g.alpha > 1]
        screen.fill((30, 32, 40))

        positions = {v: (na.cx, na.cy) for v, na in node_anims.items()}
        if not bst.is_empty():
            draw_edges(bst.root, positions)

        for na in node_anims.values():
            draw_node(na)
        for g in ghost_nodes:
            draw_node(g, ghost=True)

        if search_timer > 0 and search_path:
            alpha = int(255 * min(search_timer / SEARCH_FADE, 1.0))
            if search_found is not None:
                msg = f"Found {search_found}:  path: {', '.join(str(v) for v in search_path)}."
                col = (100, 230, 130)
            else:
                msg = f"Not found :  path: {', '.join(str(v) for v in search_path)}."
                col = (230, 100, 100)
            banner = font.render(msg, True, col)
            banner.set_alpha(alpha)
            screen.blit(banner, (10, HEIGHT - 55))

        mode = traversals[traversal_idx]
        order = getattr(bst, mode)()
        traversal_text = font.render(f"{mode}: {order}", True, (200, 200, 200))
        screen.blit(traversal_text, (10, HEIGHT - 30))

        info_text = font.render(
            "SPACE: Insert | BACKSPACE: Del Min | D: Delete val | S: Search | V: Traversal | T: Tests | ESC: Menu",
            True, (180, 180, 200)
        )
        screen.blit(info_text, (10, 10))

        if search_active:
            draw_input_box("Search for value:", search_text)
        if delete_active:
            draw_input_box("Delete value:", delete_text)

        pygame.display.flip()


def run(screen):
    font = pygame.font.SysFont(None, 28)
    menu_items = [
        "Stack Visualisation",
        "Queue Visualisation",
        "Linked List Visualisation",
        "Binary Search Tree Visualisation",
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
                    if choice == "Stack Visualisation":
                        stack_visualisation(screen, font)
                    elif choice == "Queue Visualisation":
                        queue_visualisation(screen, font)
                    elif choice == "Linked List Visualisation":
                        linked_list_visualisation(screen, font)
                    elif choice == "Binary Search Tree Visualisation":
                        binary_search_tree_visualisation(screen, font)
                    elif choice == "Back":
                        running = False
        clock.tick(30)