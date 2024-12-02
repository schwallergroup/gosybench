"""Class for evaluating the performance of a model."""

from typing import Callable, List

from pydantic import BaseModel
from task import Task, _load_default_tasks

from gosybench.logger import setup_logger
from gosybench.metrics import GraphEval, TreeMetrics

logger = setup_logger(__package__)


class GOSyBench(BaseModel):
    """Evaluating the performance of a model for KG extraction."""
    tasks: List[Task] = _load_default_tasks()
    describe: Callable | None = TreeMetrics()
    metrics: Callable | None = lambda x: None

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
            logger.info(f"Running task {task}. Time: {result['time']}")
            if self.metrics:
                logger.info(f"Calculating metrics for task {task}")
                self.metrics(task.tree)
                logger.info(f"Done calculating metrics for task {task}")


if __name__ == "__main__":
    gosybench = GOSyBench()
    geval = GraphEval()

    import networkx as nx

    method = lambda x: nx.DiGraph()

    gosybench.evaluate(method)
