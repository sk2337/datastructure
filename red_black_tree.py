class RedBlackNode:
    def __init__(self, key):
        self.key = key
        self.color = 'red'  # New nodes are red initially
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = RedBlackNode(0)  # Sentinel node (used for leaves)
        self.TNULL.color = 'black'
        self.root = self.TNULL
    
    def rotate_left(self, x):
        # Perform left rotation
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
    
    def rotate_right(self, x):
        # Perform right rotation
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fix_insert(self, k):
        # Fix the Red-Black Tree after an insertion
        while k.parent.color == 'red':
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == 'red':
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.rotate_left(k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.rotate_right(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == 'red':
                    u.color = 'black'
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rotate_right(k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    self.rotate_left(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'black'

    def insert(self, key):
        # Insert a new node with the given key
        node = RedBlackNode(key)
        node.parent = None
        node.key = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 'red'

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        
        if node.parent == None:
            node.color = 'black'
            return
        
        if node.parent.parent == None:
            return
        
        self.fix_insert(node)
    
    def inorder_helper(self, node):
        if node == self.TNULL:
            return []
        return self.inorder_helper(node.left) + [node.key] + self.inorder_helper(node.right)

    def build_graph(self, G):
        # Build a graph from the Red-Black Tree nodes
        if self.root == self.TNULL:
            return
        self._build_graph_helper(self.root, G)

    def _build_graph_helper(self, node, G):
        if node == self.TNULL:
            return
        if node.left != self.TNULL:
            G.add_edge(node.key, node.left.key)
        if node.right != self.TNULL:
            G.add_edge(node.key, node.right.key)
        self._build_graph_helper(node.left, G)
        self._build_graph_helper(node.right, G)