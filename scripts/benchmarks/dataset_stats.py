"""Compute statistics for the benchmark dataset."""

from gosybench.evaluate import GOSyBench
from gosybench.logger import setup_logger
from gosybench.metrics import TreeMetrics

logger = setup_logger(__package__)


def main():
    gosybench = GOSyBench(
        project="GOSyBench-stats",
        describe=TreeMetrics(),
    )
    gosybench.evaluate(None)


if __name__ == "__main__":
    main()
