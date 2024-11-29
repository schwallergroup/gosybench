"""Class for evaluating the performance of a model."""

from pydantic import BaseModel
from typing import Callable, List
from typing import List
from task import Task, _load_default_tasks
from logger import setup_logger

logger = setup_logger()


class GOSyBench(BaseModel):
    tasks: List[Task] = _load_default_tasks()

    def evaluate(self, f: Callable):
        """Run the evaluation."""
        logger.info("Running evaluation")
        for task in self.tasks:
            logger.info(f"Running task {task}")
            task.run(f)


if __name__ == "__main__":
    import networkx as nx

    gosybench = GOSyBench()
    method = lambda x: nx.DiGraph()
    gosybench.evaluate(method)