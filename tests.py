import unittest
from red_black_tree import RedBlackTree

class TestRedBlackTree(unittest.TestCase):
    
    def test_insert(self):
        tree = RedBlackTree()
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        
        # Check if the tree maintains its structure and balancing after insertion
        self.assertEqual(tree.inorder_helper(tree.root), [10, 20, 30])
        self.assertEqual(tree.root.color, 'black')

if __name__ == '__main__':
    unittest.main()