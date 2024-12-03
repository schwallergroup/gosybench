"""Metrics for quality of extraction."""

import networkx as nx
from pydantic import BaseModel

from gosybench.logger import setup_logger

logger = setup_logger(__package__)


class GraphEval(BaseModel):
    """Evaluate the quality of a graph extraction."""

    def __call__(self, gt, og):
        """Evaluate the extraction."""
        loc = self.compare_porder(gt, og)
        pat = self.compare_path_exact(gt, og)
        prun = self.compare_path_exact_pruned(gt, og)

        return dict(
            path_sim_in=pat[0],
            path_sim_out=pat[1],
            local_sim_in=loc[0],
            local_sim_out=loc[1],
            ploc_sim_in=prun[0],
            ploc_sim_out=prun[1],
        )

    def compare_porder(self, gt, G):
        """Compare the partial order of the graphs."""
        c0 = self._compare_porder_0(gt, G)
        c1 = self._compare_porder_0(G, gt)
        logger.debug(f"Partial order similarity: {c0}, {c1}")
        return c0, c1

    def compare_path_exact(self, gt, G):
        """Compare the paths in the graphs."""
        c0 = self._compare_path_exact_0(gt, G)
        c1 = self._compare_path_exact_0(G, gt)
        logger.debug(f"Path similarity: {c0}, {c1}")
        return c0, c1

    def compare_path_exact_pruned(self, gt, G):
        """Compare the paths in the pruned graphs."""
        pG = self._prune(G)
        pgtG = self._prune(gt)

        c0 = self._compare_path_exact_0(pgtG, pG)
        c1 = self._compare_path_exact_0(pG, pgtG)
        logger.debug(f"Pruned path similarity: {c0}, {c1}")
        return c0, c1

    def _compare_path_exact_0(self, G, gt_G):
        """How many paths in G are also in gt_G"""
        if len(G) == 0 or len(gt_G) == 0:
            return 0

        quant = []
        subgraphs = self._get_paths(G)
        for path in subgraphs:
            if len(path) > 1:
                sg = G.subgraph(path)
                v = self._subgraph_in_gt_exact(sg, gt_G)
                quant.append(v)
                logger.debug(f"Path: {path}, in gt: {v}")

        if len(quant) == 0:
            return 0
        
        logger.debug(f"{quant}")

        return sum(quant) / len(quant)

    @staticmethod
    def _subgraph_in_gt_exact(subgraph, gt_G):
        """Check if the subgraph is present in the host graph."""
        def node_match(n1, n2):
            return n1 == n2

        def edge_match(e1, e2):
            return e1 == e2

        sg = gt_G.subgraph(subgraph.nodes)
        if nx.is_isomorphic(sg, subgraph, node_match=node_match, edge_match=edge_match):
            return True

        # subg_gt = gt_G.subgraph(subgraph.nodes)
        # if len(subg_gt) == len(subgraph):
        #     return True
        return False

    @staticmethod
    def _prune(G):
        """Drop all nodes with outdeg==0."""
        pruned = G.copy()
        for node in G.nodes:
            if G.out_degree(node) == 0:
                pruned.remove_node(node)
        return pruned

    @staticmethod
    def _get_paths(G):
        """Get all simple paths in the graph."""
        paths = []
        for n0 in G.nodes:
            for n1 in G.nodes:
                if n0 != n1:
                    if nx.has_path(G, n0, n1):
                        ps = nx.all_simple_paths(G, source=n0, target=n1)
                        paths += list(ps)
        return paths

    def _compare_porder_0(self, G, gt_G):
        """Compare the partial order of the graphs."""
        if len(G) == 0 or len(gt_G) == 0:
            return 0

        quant = []
        subgraphs = self._get_paths(G)

        for path in subgraphs:
            if len(path) > 2:
                sg = POSet(path=G.subgraph(path))
                gt_sg = POSet(path=gt_G.subgraph(path))
                quant.append(sg.iso(gt_sg))

        if len(quant) == 0:
            return 0

        return sum(quant) / len(quant)


class POSet(BaseModel):
    """A partially ordered set."""

    path: nx.DiGraph

    class Config:
        arbitrary_types_allowed = True

    def gt(self, a, b):
        """Check if a is greater than b."""
        return nx.has_path(self.path, a, b)

    def iso(self, _poset):
        """Check if this poset contains _poset."""
        if len(_poset.path.nodes) == 0:
            return False

        # If nodes in _poset not contained in self
        if set(self.path.nodes).intersection(_poset.path.nodes) != set(
            _poset.path.nodes
        ):
            return False

        # Else, check that the gt relation is preserved for each edge in _poset
        for i in _poset.path.nodes:
            for j in _poset.path.nodes:
                if i != j:
                    if not self.gt(i, j) == _poset.gt(i, j):
                        return False
        return True


if __name__ == "__main__":
    gt = nx.DiGraph()
    gt.add_edge(0, 1)
    gt.add_edge(1, 2)
    gt.add_edge(2, 3)
    gt.add_edge(3, 4)
    gt.add_edge(4, 5)

    og = nx.DiGraph()
    og.add_edge(1, 0)
    og.add_edge(1, 2)

    G1 = nx.DiGraph()
    G1.add_edges_from([(0, 1), (1, 2), (2, 3), (1, 4), (4, 3)])

    G2 = nx.DiGraph()
    G2.add_edges_from(
        [(0, 1), (1, 2), (2, 3), (1, 4), (2, 4), (4, 5)]
    )

    ge = GraphEval()
    ge(G1,G2)
