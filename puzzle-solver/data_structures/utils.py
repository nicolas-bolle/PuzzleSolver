"""Utility functions"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def check_distinct(obj: list):
    """Check the objects in the list are all distinct."""
    assert len(obj) == len(set(obj)), "Elements are not distinct"


def check_disjoint(obj1: list | set, obj2: list | set):
    """Check the two lists/sets are disjoint."""
    intersection = set(obj1) & set(obj2)
    assert not intersection, (
        f"Overlapping elements found such as '{next(iter(intersection))}'"
    )


def check_subset(subset: list | set, superset: list | set):
    """Check the subset is a subset of the superset"""
    extra = set(subset) - set(superset)
    assert not extra, f"Extra elements found such as '{next(iter(extra))}'"


def check_overlap(obj1: list | set, obj2: list | set):
    """Check the two lists/sets have overlap."""
    intersection = set(obj1) & set(obj2)
    assert intersection, "No common elements"


def visualize_color_grid(color_grid: np.ndarray, figsize=(1, 1)) -> tuple[Figure, Axes]:
    """Helper function to turn a np array of color strings into a pyplot figure"""
    fig, ax = plt.subplots(figsize=figsize)

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
