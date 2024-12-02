"""Definition of a GosyBench Task."""

import os
from typing import Callable, List, Optional

import networkx as nx
from basetypes import STree
from gosybench.logger import setup_logger
from pydantic import BaseModel

logger = setup_logger(__package__)


class Task(BaseModel):
    """Definition of a GosyBench Task."""

    name: str = "Default Task"
    description: str = "Default Description"
    dataset: str = "GOSyBench"
    path: str
    tree: STree

    class Config:
        """Model configuration."""

        arbitrary_types_allowed = True
        json_encoders = {"Task": lambda v: v.dict()}

    def __str__(self):
        return f"{self.name} ({self.dataset})"

    def __repr__(self):
        return f"{self.name} ({self.dataset})"

    @classmethod
    def from_pickle(cls, path: str):
        """Load a task from a directory."""
        tree = STree.from_pickle(os.path.join(path, "gt_graph.pickle"))
        logger.debug(f"Loaded task from {path}")
        return cls(
            name=os.path.basename(path),
            path=path,
            tree=tree,
        )

    def run(self, f: Callable):
        """Run the task.
        f: function to run on the task.
            takes as input the path to the task, returns a SynTree.
        """
        results = f(self.path)
        return results


def _load_default_tasks() -> List[Task]:
    """Load the default tasks for GOSyBench."""
    tpath = os.path.join(os.path.dirname(__file__), "data/papers/")

    tasks = []
    for f in os.listdir(tpath):
        if "ja074300t" not in f:
            continue
        try:
            path = os.path.join(tpath, f)
            tasks.append(Task.from_pickle(path))
        except FileNotFoundError:
            continue

    return tasks


if __name__ == "__main__":
    _load_default_tasks()
