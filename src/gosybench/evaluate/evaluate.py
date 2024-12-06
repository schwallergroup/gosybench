"""Class for evaluating the performance of a model."""

from typing import Callable, List

from pydantic import BaseModel

import wandb
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

    def evaluate(self, f: Callable | None = None):
        """Run the evaluation."""
        logger.info("Running evaluation")
        results = {}
        gt_stats = {}
        with wandb.init(  # type: ignore
            project=self.project, config={"method": f.__name__ if f else None}
        ):

            for task in self.tasks:
                logger.info(f"Running task {task}")
                if self.describe:
                    logger.debug(f"Describing task {task}")
                    s = self.describe(task.tree)
                    logger.debug(f"Done describing task {task}")
                    gt_stats[task.name] = s

                if f:
                    logger.info(
                        f"Running task {task} with method {f.__name__}"
                    )
                    result = task.run(f)
                    logger.info(
                        f"Finished task {task}. Time: {result['time']:0.5f}s"
                    )
                    if self.describe:
                        logger.debug(f"Describing task {task}")
                        self.describe(result["tree"])
                        logger.debug(f"Done describing task {task}")
                    if self.metrics:
                        logger.debug(f"Calculating metrics for task {task}")
                        metrics = self.metrics(
                            task.tree.graph, result["tree"].graph
                        )
                        results[task.name] = metrics
                        logger.debug(
                            f"Done calculating metrics for task {task}"
                        )
            logger.info("Done evaluating")
            self.report_stats(gt_stats)
            if f:
                self.report(results)

    def report(self, results: dict):
        """Make a table and report to wandb."""
        table = wandb.Table(columns=["Task", "Metrics"])  # type: ignore
        for task, metrics in results.items():
            table.add_data(task, metrics)
        wandb.log({"Metrics": table})  # type: ignore

        # Calc mean
        varnames = results[list(results.keys())[0]].keys()
        means = {
            var: sum([result[var] for result in results.values()])
            / len(results)
            for var in varnames
        }
        wandb.summary.update(means)  # type: ignore

    def report_stats(self, stats: dict):
        """Make a table and report to wandb."""
        table = wandb.Table(columns=["Task", "Stats"])  # type: ignore
        for task, metrics in stats.items():
            table.add_data(task, metrics)
        wandb.log({"Metrics": table})  # type: ignore

        # Calc sum
        varnames = stats[list(stats.keys())[0]].keys()
        summ = {
            var: sum([result[var] for result in stats.values()])
            for var in varnames
            if not var.endswith("src")
        }
        wandb.summary.update(summ)  # type: ignore


if __name__ == "__main__":
    gosybench = GOSyBench(
        project="test",
        describe=None,
        metrics=GraphEval(),
    )

    import networkx as nx

    from gosybench.basetypes import STree

    test_method = lambda x: STree(graph=nx.DiGraph())

    gosybench.evaluate(test_method)
