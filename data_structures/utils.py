"""Utility functions"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def check_distinct(objs: list | set):
    """Check the objects in the list are all distinct"""
    counts = pd.Series(list(objs)).value_counts().sort_values(ascending=False)
    if not counts.empty:
        top_obj = counts.index[0]
        top_count = counts.iloc[0]
        assert top_count == 1, f"Expected 1 count for '{top_obj}', found {top_count}"


def check_disjoint(objs1: list | set, objs2: list | set):
    """Check the two lists are disjoint"""
    intersection = set(objs1) & set(objs2)
    assert not intersection, (
        f"Overlapping elements found such as '{next(iter(intersection))}'"
    )


def check_subset(subset: list | set, superset: list | set):
    """Check the subset is a subset of the superset"""
    extra = set(subset) - set(superset)
    assert not extra, f"Extra elements found such as '{next(iter(extra))}'"


def visualize_color_grid(
    color_grid: np.ndarray,
) -> tuple[Figure, Axes]:
    """Helper function to turn a np array of color strings into a pyplot figure"""
    fig, ax = plt.subplots(figsize=(1, 1))

    for i in range(color_grid.shape[0]):
        for j in range(color_grid.shape[1]):
            ax.add_patch(
                plt.Rectangle(
                    (i, j), 1, 1, facecolor=color_grid[i, j], edgecolor="black"
                )
            )

    ax.set_xlim(0, color_grid.shape[0])
    ax.set_ylim(0, color_grid.shape[1])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)

    return fig, ax
