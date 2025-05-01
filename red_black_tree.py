import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Red-Black Tree Node class
class RedBlackNode:
    def __init__(self, key):
        self.key = key
        self.color = 'red'  # New nodes are red initially
        self.left = None
        self.right = None
        self.parent = None

# Red-Black Tree class
class RedBlackTree:
    def __init__(self):
        self.TNULL = RedBlackNode(0)  # Sentinel node (used for leaves)
        self.TNULL.color = 'black'
        self.root = self.TNULL
        self.last_inserted = None
    
    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, key):
        # standard BST insert
        node = RedBlackNode(key)
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 'red'

        parent = None
        curr = self.root
        while curr != self.TNULL:
            parent = curr
            curr = curr.left if key < curr.key else curr.right

        node.parent = parent
        if parent is None:
            self.root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node

        self.last_inserted = node
        self.fix_insert(node)

    def fix_insert(self, k):
        """Run the full red‑black fix in one shot."""
        while k.parent and k.parent.color == 'red':
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == 'red':
                    k.parent.color = u.color = 'black'
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
                    k.parent.color = u.color = 'black'
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

    def fix_insert_steps(self, k):
        """Yield (‘recolor’/‘rotate_left’/‘rotate_right’, node) at each atomic step."""
        while k.parent and k.parent.color == 'red':
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == 'red':
                    u.color = k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    yield ('recolor', k.parent.parent)
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.rotate_left(k)
                        yield ('rotate_left', k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    yield ('recolor', k.parent)
                    self.rotate_right(k.parent.parent)
                    yield ('rotate_right', k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == 'red':
                    u.color = k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    yield ('recolor', k.parent.parent)
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rotate_right(k)
                        yield ('rotate_right', k)
                    k.parent.color = 'black'
                    k.parent.parent.color = 'red'
                    yield ('recolor', k.parent)
                    self.rotate_left(k.parent.parent)
                    yield ('rotate_left', k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'black'
        yield ('done', self.root)

    # ─── Graph & Traversal ─────────────────────────────────────────────────────
    
    def inorder_helper(self, node):
        if node == self.TNULL:
            return []
        return (self.inorder_helper(node.left) +
                [node.key] +
                self.inorder_helper(node.right))

    def build_graph(self, G):
        if self.root != self.TNULL:
            self._build_graph_helper(self.root, G)

    def _build_graph_helper(self, node, G):
        if node == self.TNULL:
            return
        G.add_node(node.key, color=node.color)
        if node.left  != self.TNULL:
            G.add_edge(node.key, node.left.key)
            self._build_graph_helper(node.left, G)
        if node.right != self.TNULL:
            G.add_edge(node.key, node.right.key)
            self._build_graph_helper(node.right, G)

# ─── Layout Helpers ──────────────────────────────────────────────────────────

def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = {root: (xcenter, vert_loc)}
    children = list(G.neighbors(root))
    if children:
        dx = width / len(children)
        nextx = xcenter - width/2 - dx/2
        for c in children:
            nextx += dx
            pos.update(hierarchy_pos(G, c, dx, vert_gap, vert_loc-vert_gap, nextx))
    return pos

""" 
def visualize_tree(tree):
    G = nx.DiGraph();  tree.build_graph(G)
    if not G.nodes:
        st.warning("Tree is empty!"); return

    try:
        pos = hierarchy_pos(G, tree.root.key)
    except:
        pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(10,6))
    colors = ['red' if G.nodes[n]['color']=='red' else 'black' for n in G.nodes]
    nx.draw(G, pos, ax=ax, with_labels=True, node_color=colors,
            node_size=1500, font_color='white', edgecolors='black',
            linewidths=1, arrows=False, font_weight='bold')
    ax.set_title("Red‑Black Tree")
    st.pyplot(fig)
    plt.close(fig)

# ─── Streamlit App ───────────────────────────────────────────────────────────

def main():
    st.title("Red‑Black Tree Visualization")

    # — initialize session state —
    tree = st.session_state.setdefault('tree', RedBlackTree())
    steps    = st.session_state.setdefault('steps', [])
    step_idx = st.session_state.setdefault('step_idx', 0)

    # — controls —
    val       = st.number_input("Value to insert", min_value=1, value=1, step=1)
    step_mode = st.checkbox("Enable Step‑by‑Step")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Insert"):
            tree.insert(val)
            if step_mode:
                st.session_state.steps = list(tree.fix_insert_steps(tree.last_inserted))
                st.session_state.step_idx = 0
            else:
                tree.fix_insert(tree.last_inserted)
                st.session_state.steps = []

    with c2:
        if step_mode and st.button("Next Step"):
            idx = st.session_state.step_idx
            if idx < len(st.session_state.steps):
                action, node = st.session_state.steps[idx]
                st.info(f"{action} on node {node.key}")
                st.session_state.step_idx += 1

    with c3:
        if st.button("Clear"):
            st.session_state.tree = RedBlackTree()
            st.session_state.steps = []
            st.session_state.step_idx = 0

    visualize_tree(tree)

    if step_mode and steps:
        st.write(f"Step {step_idx}/{len(steps)}")
        if st.button("Show In‑Order"):
            st.write(tree.inorder_helper(tree.root))

if __name__ == "__main__":
    main() """