"""Utility functions"""

import pandas as pd


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
    assert (
        not intersection
    ), f"Overlapping elements found such as {next(iter(intersection))}"


def check_subset(subset: list | set, superset: list | set):
    """Check the subset is a subset of the superset"""
    extra = set(superset) - set(subset)
    assert not extra, f"Extra elements found such as {next(iter(extra))}"
