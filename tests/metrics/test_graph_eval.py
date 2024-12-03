import unittest

import networkx as nx

from gosybench.metrics.metrics import GraphEval, POSet


class TestGraphEvalMetrics(unittest.TestCase):
    """Evaluate the GraphEval metrics"""

    def setUp(self):
        """Set up the test cases"""
        self.ge = GraphEval()

        # Original graphs
        self.G1 = nx.DiGraph()
        self.G1.add_edges_from([(0, 1), (1, 2), (2, 3), (1, 4), (4, 3)])

        self.G2 = nx.DiGraph()
        self.G2.add_edges_from(
            [(0, 1), (1, 2), (2, 3), (1, 4), (2, 4), (4, 5)]
        )

        # Identical graphs
        self.G_identical_1 = nx.DiGraph()
        self.G_identical_1.add_edges_from([(0, 1), (1, 2), (2, 3)])

        self.G_identical_2 = nx.DiGraph()
        self.G_identical_2.add_edges_from([(0, 1), (1, 2), (2, 3)])

        # Completely different graphs
        self.G_different_1 = nx.DiGraph()
        self.G_different_1.add_edges_from([(0, 1), (1, 2), (2, 3)])

        self.G_different_2 = nx.DiGraph()
        self.G_different_2.add_edges_from([(4, 5), (5, 6), (6, 7)])

    def test_identical_graphs(self):
        """Test the case of identical graphs"""
        result = self.ge(self.G_identical_1, self.G_identical_2)
        self.assertEqual(result["path_sim_in"], 1.0)
        self.assertEqual(result["path_sim_out"], 1.0)
        self.assertEqual(result["local_sim_in"], 1.0)
        self.assertEqual(result["local_sim_out"], 1.0)
        self.assertEqual(result["ploc_sim_in"], 1.0)
        self.assertEqual(result["ploc_sim_out"], 1.0)

    def test_completely_different_graphs(self):
        """Test the case of completely different graphs"""
        result = self.ge(self.G_different_1, self.G_different_2)
        self.assertAlmostEqual(result["path_sim_in"], 0.0, places=3)
        self.assertAlmostEqual(result["path_sim_out"], 0.0, places=3)
        self.assertAlmostEqual(result["local_sim_in"], 0.0, places=3)
        self.assertAlmostEqual(result["local_sim_out"], 0.0, places=3)
        self.assertAlmostEqual(result["ploc_sim_in"], 0.0, places=3)
        self.assertAlmostEqual(result["ploc_sim_out"], 0.0, places=3)

    def test_empty_graphs(self):
        """Test the case of empty graphs"""
        G_empty_1 = nx.DiGraph()
        G_empty_2 = nx.DiGraph()
        result = self.ge(G_empty_1, G_empty_2)

        # Empty graphs default to 0 sim (assume graph.nodes>0)
        self.assertEqual(result["path_sim_in"], 0.0)
        self.assertEqual(result["path_sim_out"], 0.0)
        self.assertEqual(result["local_sim_in"], 0.0)
        self.assertEqual(result["local_sim_out"], 0.0)
        self.assertEqual(result["ploc_sim_in"], 0.0)
        self.assertEqual(result["ploc_sim_out"], 0.0)

    def test_empty_and_non_empty_graphs(self):
        """Test the case of empty and non-empty graphs"""
        G_empty = nx.DiGraph()
        result = self.ge(G_empty, self.G1)
        self.assertAlmostEqual(result["path_sim_in"], 0.0, places=3)
        self.assertAlmostEqual(result["path_sim_out"], 0.0, places=3)
        self.assertAlmostEqual(result["local_sim_in"], 0.0, places=3)
        self.assertAlmostEqual(result["local_sim_out"], 0.0, places=3)
        self.assertAlmostEqual(result["ploc_sim_in"], 0.0, places=3)
        self.assertAlmostEqual(result["ploc_sim_out"], 0.0, places=3)

    def test_compare_porder(self):
        """Test the compare_porder method"""
        result = self.ge.compare_porder(self.G1, self.G2)
        self.assertAlmostEqual(result[0], 0.6666, places=3)
        self.assertAlmostEqual(result[1], 0.5454, places=3)

    def test_compare_path_exact(self):
        """Test the compare_path_exact method
        TODO Check"""
        result = self.ge.compare_path_exact(self.G1, self.G2)
        self.assertAlmostEqual(result[0], 0.875, places=3)
        self.assertAlmostEqual(result[1], 0.7, places=3)

    def test_compare_path_exact_pruned(self):
        """Test the compare_path_exact_pruned method
        TODO Check"""
        result = self.ge.compare_path_exact_pruned(self.G1, self.G2)
        self.assertAlmostEqual(result[0], 0.7272, places=3)
        self.assertAlmostEqual(result[1], 0.4706, places=3)

    def test_all_metrics(self):
        """Test all metrics at once
        TODO Check"""
        result = self.ge(self.G1, self.G2)
        self.assertAlmostEqual(result["path_sim_in"], 0.875, places=3)
        self.assertAlmostEqual(result["path_sim_out"], 0.7, places=3)
        self.assertAlmostEqual(result["local_sim_in"], 0.833, places=3)
        self.assertAlmostEqual(result["local_sim_out"], 0.571, places=3)
        self.assertAlmostEqual(result["ploc_sim_in"], 0.875, places=3)
        self.assertAlmostEqual(result["ploc_sim_out"], 0.7, places=3)


class TestGraphEval(unittest.TestCase):
    """Test the GraphEval class - qualitative"""

    def setUp(self):
        """Set up the test cases"""
        self.ge = GraphEval()

        # Create some sample graphs for testing
        self.g1 = nx.DiGraph()
        self.g1.add_edges_from([(0, 1), (1, 2), (2, 3)])

        self.g2 = nx.DiGraph()
        self.g2.add_edges_from([(0, 1), (1, 2), (2, 3), (1, 3)])

        self.g3 = nx.DiGraph()
        self.g3.add_edges_from([(0, 1), (1, 2)])

    def test_compare_porder(self):
        """Test the compare_porder method"""
        result = self.ge.compare_porder(self.g1, self.g2)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)
        self.assertGreaterEqual(result[0], 0)
        self.assertLessEqual(result[0], 1)
        self.assertGreaterEqual(result[1], 0)
        self.assertLessEqual(result[1], 1)

    def test_compare_path_exact(self):
        """Test the compare_path_exact method"""
        result = self.ge.compare_path_exact(self.g1, self.g3)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)
        self.assertGreaterEqual(result[0], 0)
        self.assertLessEqual(result[0], 1)
        self.assertGreaterEqual(result[1], 0)
        self.assertLessEqual(result[1], 1)

    def test_compare_path_exact_pruned(self):
        """Test the compare_path_exact_pruned method"""
        result = self.ge.compare_path_exact_pruned(self.g1, self.g2)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)
        self.assertGreaterEqual(result[0], 0)
        self.assertLessEqual(result[0], 1)
        self.assertGreaterEqual(result[1], 0)
        self.assertLessEqual(result[1], 1)

    def test_prune(self):
        """Test the prune method"""
        g = nx.DiGraph()
        g.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (1, 5)])
        pruned = self.ge._prune(g)
        self.assertEqual(len(pruned.nodes), 4)  # Nodes 4 and 5 should be pruned
        self.assertNotIn(4, pruned.nodes)
        self.assertNotIn(5, pruned.nodes)

    def test_get_paths(self):
        """Test the get_paths method"""
        paths = self.ge._get_paths(self.g1)
        expected_paths = [
            [0, 1],
            [0, 1, 2],
            [0, 1, 2, 3],
            [1, 2],
            [1, 2, 3],
            [2, 3],
        ]
        self.assertEqual(sorted(paths), sorted(expected_paths))


class TestPOSet(unittest.TestCase):
    """Test the POSet class"""

    def setUp(self):
        """Set up the test cases"""
        g = nx.DiGraph()
        g.add_edges_from([(0, 1), (1, 2), (2, 3)])
        self.poset = POSet(path=g)

    def test_gt(self):
        """Test the gt method"""
        self.assertTrue(self.poset.gt(0, 3))
        self.assertTrue(self.poset.gt(1, 3))
        self.assertFalse(self.poset.gt(3, 0))
        self.assertFalse(self.poset.gt(2, 1))

    def test_iso(self):
        """Test the iso method"""
        g1 = nx.DiGraph()
        g1.add_edges_from([(0, 1), (1, 2)])
        poset1 = POSet(path=g1)

        g2 = nx.DiGraph()
        g2.add_edges_from([(0, 1), (1, 2), (0, 2)])
        poset2 = POSet(path=g2)

        g3 = nx.DiGraph()
        g3.add_edges_from([(0, 2), (2, 1)])
        poset3 = POSet(path=g3)

        self.assertTrue(self.poset.iso(poset1))
        self.assertTrue(self.poset.iso(poset2))
        self.assertFalse(self.poset.iso(poset3))
        self.assertFalse(poset1.iso(poset3))


if __name__ == "__main__":
    unittest.main()
