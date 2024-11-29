"""Definition of a GosyBench Task."""

from typing import List, Optional

import networkx as nx
from pydantic import BaseModel
import os
import pickle
from typing import Callable
import logging


class Task(BaseModel):
    """Definition of a GosyBench Task."""

    name: str = "Default Task"
    description: str = "Default Description"
    dataset: str = "Default Dataset"
    model: str = "Default Model"
    metric: str = "Default Metric"
    score: Optional[float] = None
    path: str
    graph: nx.DiGraph

    class Config:
        """Model configuration."""

        arbitrary_types_allowed = True
        json_encoders = {
            "Task": lambda v: v.dict()
        }

    def __str__(self):
        return f"{self.name} ({self.dataset})"

    def __repr__(self):
        return f"{self.name} ({self.dataset})"

    @classmethod
    def from_pickle(cls, path: str):
        """Load a task from a directory."""
        with open(os.path.join(path, "gt_graph.pickle"), "rb") as f:
            data = pickle.load(f)
            logging.info(f"Loaded task from {path}")
        return cls(graph=data, path=path, name=os.path.basename(path))

    def run(self, f: Callable):
        """Run the task.
        f: function to run on the task.
            takes as input the path to the task, returns a SynTree.
        """
        results = f(self.path)

        # TODO: Run evaluation metrics on this

        return results



def _load_default_tasks() -> List[Task]:
    """Load the default tasks for GOSyBench."""

    tpath = os.path.join(os.path.dirname(__file__), "data/papers/")

    tasks = []
    for f in os.listdir(tpath):
        try:
            path = os.path.join(tpath, f)
            tasks.append(Task.from_pickle(path))
        except FileNotFoundError:
            pass

    return tasks

if __name__ == "__main__":
    print(_load_default_tasks())