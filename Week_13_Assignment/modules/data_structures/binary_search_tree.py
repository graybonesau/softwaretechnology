class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self._size = 0

    def is_empty(self):
        return self.root is None

    def size(self):
        return self._size

    def insert(self, value):
        if self.root is None:
            self.root = BSTNode(value)
            self._size += 1
        else:
            self._size += self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value)
                return 1
            else:
                return self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = BSTNode(value)
                return 1
            else:
                return self._insert_recursive(node.right, value)
        return 0

    def search(self, value):
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        if node is None:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def delete(self, value):
        self.root, deleted = self._delete_recursive(self.root, value)
        if deleted:
            self._size -= 1
        return deleted

    def _delete_recursive(self, node, value):
        if node is None:
            return node, False

        deleted = False
        if value < node.value:
            node.left, deleted = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right, deleted = self._delete_recursive(node.right, value)
        else:
            deleted = True

            if node.left is None:
                return node.right, deleted
            elif node.right is None:
                return node.left, deleted

            successor = self._min_node(node.right)
            node.value = successor.value
            node.right, _ = self._delete_recursive(node.right, successor.value)

        return node, deleted

    def _min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def height(self):
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left),
                       self._height_recursive(node.right))

    def preorder(self):
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder(self):
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def layout_positions(self, width):
        positions = {}
        self._layout_recursive(self.root, 0, 0, width, positions)
        return positions

    def _layout_recursive(self, node, depth, left_bound, right_bound, positions):
        if node is None:
            return
        x = (left_bound + right_bound) // 2
        y = 80 + depth * 90
        positions[id(node)] = (x, y, node)
        self._layout_recursive(node.left,  depth + 1, left_bound, x,           positions)
        self._layout_recursive(node.right, depth + 1, x,          right_bound, positions)

    def draw(self, screen, font, width, height):
        import pygame
        node_col = (100, 150, 250)
        edge_col = (200, 200, 200)
        text_col = (  0,   0,   0)
        node_r   = 26

        positions = self.layout_positions(width)

        for _, (x, y, node) in positions.items():
            for child in (node.left, node.right):
                if child and id(child) in positions:
                    cx, cy, _ = positions[id(child)]
                    pygame.draw.line(screen, edge_col, (x, y), (cx, cy), 2)

        for _, (x, y, node) in positions.items():
            pygame.draw.circle(screen, node_col, (x, y), node_r)
            label = font.render(str(node.value), True, text_col)
            screen.blit(label, label.get_rect(center=(x, y)))

    def __repr__(self):
        return f"BinarySearchTree(inorder={self.inorder()})"