import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from red_black_tree import RedBlackTree

def visualize_tree(tree):
    G = nx.DiGraph()
    tree.build_graph(G)
    if not G.nodes:
        st.warning("Tree is empty!")
        return

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(10,6))
    colors = ['red' if G.nodes[n]['color']=='red' else 'black' for n in G.nodes]
    nx.draw(G, pos, ax=ax, with_labels=True, node_color=colors,
            node_size=1500, font_color='white',
            edgecolors='black', linewidths=1, arrows=False)
    ax.set_title("Red‑Black Tree")
    st.pyplot(fig)
    plt.close(fig)

def main():
    st.title("Red‑Black Tree")

    # persist state
    if 'tree' not in st.session_state:
        st.session_state.tree = RedBlackTree()

    tree = st.session_state.tree

    # input controls
    val = st.number_input("Value to insert", min_value=1, value=1, step=1)
    step_mode = st.checkbox("Enable Step‑by‑Step")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Insert"):
            tree.insert(val)
            if not step_mode:
                tree.fix_insert(tree.last_inserted)
            else:
                # prime step generator
                st.session_state.steps = list(tree.fix_insert_steps(tree.last_inserted))
                st.session_state.step_idx = 0

    with c2:
        if step_mode and st.button("Next"):
            idx = st.session_state.step_idx
            if idx < len(st.session_state.steps):
                action, node = st.session_state.steps[idx]
                st.info(f"{action} on {node.key}")
                st.session_state.step_idx += 1

    if st.button("Clear"):
        st.session_state.tree = RedBlackTree()

    visualize_tree(tree)

    if st.button("Show In‑Order"):
        st.write(tree.inorder_helper(tree.root))

if __name__=='__main__':
    main()
