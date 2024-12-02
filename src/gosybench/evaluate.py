"""Class for evaluating the performance of a model."""

from typing import Callable, List

from logger import setup_logger
from metrics import TreeMetrics
from pydantic import BaseModel
from task import Task, _load_default_tasks

logger = setup_logger()


class GOSyBench(BaseModel):
    tasks: List[Task] = _load_default_tasks()
    metrics: TreeMetrics = TreeMetrics()

    def evaluate(self, f: Callable):
        """Run the evaluation."""
        logger.info("Running evaluation")
        for task in self.tasks:
            logger.info(f"Running task {task}")
            self.metrics(task.tree)
            task.run(f)


if __name__ == "__main__":
    gosybench = GOSyBench()

    import networkx as nx

    method = lambda x: nx.DiGraph()

    gosybench.evaluate(method)
