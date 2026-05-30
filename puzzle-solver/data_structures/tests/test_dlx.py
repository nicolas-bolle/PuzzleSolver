"""dlx.py unit tests"""

import numpy as np
import pytest

from data_structures.dlx import ArrayDLX, RowSparseGeneralizedDLX


def test_row_sparse_generalized_dlx_basic_problem():
    """Basic exact cover problem"""
    row_names = ["A", "B", "C", "D", "E", "F", "G"]
    col_names = list(range(len(row_names)))
    entries = {
        "A": [0, 3, 6],
        "B": [0, 3],
        "C": [3, 4, 6],
        "D": [2, 4, 5],
        "E": [1, 2, 5, 6],
        "F": [6],
        "G": [1],
    }

    dlx = RowSparseGeneralizedDLX(
        row_names=row_names,
        col_names_primary=col_names,
        col_names_secondary=[],
        entries=entries,
    )

    solutions_desired = {"ADG", "BDFG"}
    solutions_actual = {"".join(soln) for soln in dlx.generate_solutions()}

    assert solutions_actual == solutions_desired


def test_row_sparse_generalized_dlx_data_checks():
    """Confirm data checks are working"""
    # row names
    with pytest.raises(AssertionError) as e:
        RowSparseGeneralizedDLX(
            row_names=["row", "row"],
            col_names_primary=["col1"],
            col_names_secondary=["col2"],
            entries={},
        )
    assert str(e.value) == "Elements are not distinct"

    # column names
    with pytest.raises(AssertionError) as e:
        RowSparseGeneralizedDLX(
            row_names=["row"],
            col_names_primary=["col1", "col1"],
            col_names_secondary=["col2"],
            entries={},
        )
    assert str(e.value) == "Elements are not distinct"

    with pytest.raises(AssertionError) as e:
        RowSparseGeneralizedDLX(
            row_names=["row"],
            col_names_primary=["col1"],
            col_names_secondary=["col2", "col2"],
            entries={},
        )
    assert str(e.value) == "Elements are not distinct"

    with pytest.raises(AssertionError) as e:
        RowSparseGeneralizedDLX(
            row_names=["row"],
            col_names_primary=["col1"],
            col_names_secondary=["col1"],
            entries={},
        )
    assert str(e.value) == "Overlapping elements found such as 'col1'"

    # entries
    with pytest.raises(AssertionError) as e:
        RowSparseGeneralizedDLX(
            row_names=["row"],
            col_names_primary=["col1"],
            col_names_secondary=["col2"],
            entries={"row1": ["col1"]},
        )
    assert str(e.value) == "Extra elements found such as 'row1'"

    with pytest.raises(AssertionError) as e:
        RowSparseGeneralizedDLX(
            row_names=["row"],
            col_names_primary=["col1"],
            col_names_secondary=["col2"],
            entries={"row": ["col3"]},
        )
    assert str(e.value) == "Extra elements found such as 'col3'"

    # successful init
    RowSparseGeneralizedDLX(
        row_names=["row"],
        col_names_primary=["col1"],
        col_names_secondary=["col2"],
        entries={"row": ["col1"]},
    )


def test_array_dlx_basic_problem():
    """Basic exact cover problem"""
    A = [
        [1, 0, 0, 1, 0, 0, 1],  # A
        [1, 0, 0, 1, 0, 0, 0],  # B
        [0, 0, 0, 1, 1, 0, 1],  # C
        [0, 0, 1, 0, 1, 1, 0],  # D
        [0, 1, 1, 0, 0, 1, 1],  # E
        [0, 0, 0, 0, 0, 0, 1],  # F
        [0, 1, 0, 0, 0, 0, 0],  # G
    ]
    A = np.array(A)

    row_names = ["A", "B", "C", "D", "E", "F", "G"]
    dlx = ArrayDLX(A=A, row_names=row_names)

    solutions_desired = {"ADG", "BDFG"}
    solutions_actual = {"".join(sorted(soln)) for soln in dlx.generate_solutions()}

    assert solutions_actual == solutions_desired


def test_array_dlx_secondary_problem():
    """Exact problem with secondary constraints.
    The secondary columns are optional to cover, and won't be covered if not necessary.
    """
    A = [
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 1, 1, 0],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
    ]
    A_secondary = [
        [0],
        [0],
        [0],
        [0],
        [1],
        [1],
        [1],
    ]
    A = np.array(A)
    A_secondary = np.array(A_secondary)

    row_names = ["A", "B", "C", "D", "E", "F", "G"]

    dlx = ArrayDLX(A=A, row_names=row_names, A_secondary=A_secondary)

    solutions_desired = {"AB", "CD", "CE"}
    solutions_actual = {"".join(sorted(soln)) for soln in dlx.generate_solutions()}

    assert solutions_actual == solutions_desired


def test_array_dlx_data_checks():
    """Confirm data checks are working"""
    # array checks
    with pytest.raises(AssertionError) as e:
        ArrayDLX(A=[[]], row_names=["row"])
    assert str(e.value) == "A must be a np.ndarray"

    with pytest.raises(AssertionError) as e:
        ArrayDLX(A=np.array([[]]), row_names=["row"], A_secondary=[[]])
    assert str(e.value) == "A_secondary must be a np.ndarray"

    with pytest.raises(AssertionError) as e:
        ArrayDLX(A=np.array([]), row_names=["row"])
    assert str(e.value) == "A must be two dimensional"

    with pytest.raises(AssertionError) as e:
        ArrayDLX(A=np.array([[]]), row_names=["row"], A_secondary=np.array([]))
    assert str(e.value) == "A_secondary must be two dimensional"

    with pytest.raises(AssertionError) as e:
        ArrayDLX(A=np.array([[0, 0]]), row_names=["row"], A_secondary=np.array([[1]]))
    assert str(e.value) == "Row 'row' is trivial: does not include any primary columns"

    with pytest.raises(AssertionError) as e:
        ArrayDLX(
            A=np.array([[0, 0], [0, 0]]),
            row_names=["row1", "row2"],
            A_secondary=np.array([[0]]),
        )
    assert str(e.value) == "A has 2 rows while A_secondary has 1 rows"

    # name checks
    with pytest.raises(AssertionError) as e:
        ArrayDLX(
            A=np.array([[0, 0], [0, 0]]),
            row_names=["row"],
            A_secondary=np.array([[0], [0]]),
        )
    assert str(e.value) == "1 rows specified, expected 2"

    with pytest.raises(AssertionError) as e:
        ArrayDLX(
            A=np.array([[0, 0], [0, 0]]),
            row_names=["row1", "row2"],
            col_names=["col"],
            A_secondary=np.array([[0], [0]]),
        )
    assert str(e.value) == "1 columns specified, expected 2"

    with pytest.raises(AssertionError) as e:
        ArrayDLX(
            A=np.array([[0, 0], [0, 0]]),
            row_names=["row1", "row2"],
            col_names=["col1", "col2"],
            A_secondary=np.array([[0], [0]]),
            col_names_secondary=["col3", "col4"],
        )
    assert str(e.value) == "2 secondary columns specified, expected 1"

    # successful init
    ArrayDLX(
        A=np.array([[1, 0], [0, 1]]),
        row_names=["row1", "row2"],
        col_names=["col1", "col2"],
        A_secondary=np.array([[1], [0]]),
        col_names_secondary=["col3"],
    )


def test_array_dlx_defaults():
    """Check defaults are as expected"""
    # column names
    dlx = ArrayDLX(
        A=np.array([[1, 0, 0]]), A_secondary=np.array([[0, 0]]), row_names=["row"]
    )
    assert dlx.col_names == ["primary_0", "primary_1", "primary_2"]
    assert dlx.col_names_secondary == ["secondary_0", "secondary_1"]

    # secondary constraints
    dlx = ArrayDLX(A=np.array([[1, 0, 0]]), row_names=["row"])
    assert isinstance(dlx.A_secondary, np.ndarray)
    assert dlx.A_secondary.shape == (1, 0)


def test_array_dlx_translation():
    """Confirm we define the the DLX fields correctly"""
    dlx = ArrayDLX(
        A=np.array([[1, 0], [0, 1]]),
        row_names=["row1", "row2"],
        col_names=["col1", "col2"],
        A_secondary=np.array([[1], [0]]),
        col_names_secondary=["col3"],
    )

    assert dlx.row_names == ["row1", "row2"]
    assert dlx.col_names_primary == ["col1", "col2"]
    assert dlx.col_names_secondary == ["col3"]

    entries_target = {"row1": ["col1", "col3"], "row2": ["col2"]}
    assert dlx.entries == entries_target
