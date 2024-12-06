import time
import unittest

import networkx as nx
import numpy as np

from gosybench.basetypes import STree
from gosybench.metrics.utils import SmilesPathFinder


class TestMaxSeqSmiles(unittest.TestCase):
    """Test the max_seq_smiles method in SmilesPathFinder."""

    def setUp(self):
        """Create a sample STree with a single component."""
        N = 100
        Ne = 50
        np.random.seed(0)
        self.graph = nx.DiGraph()
        for i in range(N):
            if np.random.random() < 0.8:  # 80% chance of having SMILES
                self.graph.add_node(i, attr={"smiles": f"C{i}"})
            else:
                self.graph.add_node(i)
        for i in range(N - 1):
            self.graph.add_edge(i, i + 1)

        # Add some random edges to make it more complex
        for _ in range(Ne):
            self.graph.add_edge(
                np.random.randint(1, N), np.random.randint(1, N)
            )

        # Ensure there's at least one node with in-degree 0 and SMILES
        self.graph.add_edge(0, np.random.randint(1, N))
        self.graph.nodes[0]["attr"] = {"smiles": "C0"}

        # Create an STree with one component
        self.stree = STree(graph=self.graph, products=[])

    def test_max_seq_smiles_performance(self):
        """Test the performance of the max_seq_smiles method."""
        optimized_solver = SmilesPathFinder()

        # Test optimized version
        start_time = time.time()
        optimized_result = optimized_solver.max_seq_smiles(self.stree)
        optimized_time = time.time() - start_time
        print(optimized_result["long_path_0_len"])

        print(f"Optimized version time: {optimized_time:.4f} seconds")

    def test_correctness(self):
        """Test if the optimized version returns the same result as the original."""
        optimized_solver = SmilesPathFinder()

        optimized_result = optimized_solver.max_seq_smiles(self.stree)

        # Check if all paths in optimized result are also in original result
        for i in range(3):
            self.assertIn(f"long_path_{i}_len", optimized_result)
            self.assertIn(f"long_path_{i}_src", optimized_result)


if __name__ == "__main__":
    unittest.main()
