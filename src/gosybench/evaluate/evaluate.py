"""Class for evaluating the performance of a model."""

from typing import Callable, List

from pydantic import BaseModel

from gosybench.logger import setup_logger
from gosybench.metrics import GraphEval, TreeMetrics

from .task import Task, _load_default_tasks

logger = setup_logger(__package__)


class GOSyBench(BaseModel):
    """Evaluating the performance of a model for KG extraction."""

    tasks: List[Task] = _load_default_tasks()
    project: str = "GOSyBench"
    describe: Callable | None = TreeMetrics()
    metrics: Callable | None = GraphEval()

    def evaluate(self, f: Callable):
        """Run the evaluation."""
        logger.info("Running evaluation")
        for task in self.tasks:
            if self.describe:
                logger.info(f"Describing task {task}")
                self.describe(task.tree)
                logger.info(f"Done describing task {task}")
            logger.info(f"Running task {task} with method {f}")
            result = task.run(f)
            logger.info(f"Finished task {task}. Time: {result['time']:0.5f}s")
            if self.describe:
                logger.info(f"Describing task {task}")
                self.describe(result["tree"])
                logger.info(f"Done describing task {task}")
            if self.metrics:
                logger.info(f"Calculating metrics for task {task}")
                self.metrics(task.tree.graph, result["tree"].graph)
                logger.info(f"Done calculating metrics for task {task}")
        logger.info("Done evaluating")


if __name__ == "__main__":
    gosybench = GOSyBench(
        project="test",
        describe=TreeMetrics(),
        metrics=GraphEval(),
    )

    import networkx as nx

    from gosybench.basetypes import STree

    test_method = lambda x: STree(graph=nx.DiGraph())

    gosybench.evaluate(test_method)
