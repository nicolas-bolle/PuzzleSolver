"""Terrible python code for reading puzzles from the Kanoodle booklet pdf
Running this file outputs a toml??? with the puzzles??? TODO

Just janky image segmentation with lots of magic numbers
With just 162 puzzles this unreliable code isn't worth it, but it was good to try image analysis
This shows that for it to be practical I'd have to learn a lot of new techniques
"""

import easyocr
import numpy as np
from pdf2image import convert_from_path
from tqdm.auto import tqdm

from data_structures.utils import check_disjoint

FILE_NAME = "kanoodle_booklet.pdf"


# some magic numbers, and there's plenty more in the code :)
dpi = 500

padding = 20

width_char = 42
i_stride_small = 61
j_stride_small = 61
i_stride_big = 463
j_stride_big = 788

width_num = 110
i_offset_num = -150
j_offset_num = -30


def parse_page(page, reader) -> dict:
    """Attempt to parse a page into the puzzles it contains"""
    # TODO what's the right format for the return?
    image = np.array(page)

    # grayscale and threshold for piece recognition
    A_char = np.array(image).mean(axis=2)
    A_char = np.array((A_char <= 50) * 255, dtype="uint8")

    # grayscale and threshold for puzzle number recognition
    A_num = np.array(image).mean(axis=2)
    A_num = np.array((A_num <= 200) * 255, dtype="uint8")

    # from now on if anything fails, just assume it's not possible to parse this page
    try:
        # figure out the "base" point
        A_base = A_char[:500, :500].copy()
        A_base[:200, :] = 0
        A_base[:, :200] = 0
        i_base_raw, j_base_raw = sorted(
            list(zip(*np.where(A_base == 255))), key=lambda t: t[0] + t[0]
        )[0]
        i_base = int(i_base_raw) + 19
        j_base = int(j_base_raw) + 3

        # iterate over puzzles
        _puzzles = {}
        for I in range(2):
            for J in range(3):
                # parse the puzzle number
                num = _parse_num(
                    A_num,
                    reader,
                    i_base,
                    j_base,
                    I,
                    J,
                )

                # parse the chars
                grid = np.full(shape=(5, 11), fill_value="", dtype=object)
                for i in range(5):
                    for j in range(11):
                        grid[i, j] = _parse_char(
                            A_char,
                            reader,
                            i_base,
                            j_base,
                            I,
                            J,
                            i,
                            j,
                        )

                # record this puzzle
                _puzzles[num] = grid

        # final checks
        assert len(_puzzles.keys()) == 6

        return _puzzles

    except:
        return {}


def _parse_num(A_num, reader, i_base, j_base, I, J) -> int:
    i_min = i_base + i_stride_big * I + i_offset_num
    i_max = i_min + width_num
    j_min = j_base + j_stride_big * J + j_offset_num
    j_max = j_min + width_num

    img = A_num[
        i_min - padding : i_max + padding, j_min - padding : j_max + padding
    ].copy()
    img[:padding, :] = 0
    img[-padding:, :] = 0
    img[:, :padding] = 0
    img[:, -padding:] = 0

    result = reader.readtext(img, detail=0)
    assert len(result) == 1
    return int(result[0])


def _parse_char(A_char, reader, i_base, j_base, I, J, i, j) -> str:
    i_min = i_base + i_stride_big * I + i_stride_small * i
    i_max = i_min + width_char
    j_min = j_base + j_stride_big * J + j_stride_small * j
    j_max = j_min + width_char

    img = A_char[
        i_min - padding : i_max + padding, j_min - padding : j_max + padding
    ].copy()
    img[:padding, :] = 0
    img[-padding:, :] = 0
    img[:, :padding] = 0
    img[:, -padding:] = 0

    result = reader.readtext(img, detail=0)
    s = "".join(result)
    s = "".join(c for c in s if c in "ABCDEFGHIJKL")
    s = s.replace("EE", "E")  # one-off issue
    if len(s) > 1:
        print(s)
    assert len(s) <= 1

    return s


if __name__ == "__main__":
    # parse pdf to images
    pages = convert_from_path(FILE_NAME, dpi=dpi)

    # set up OCR reader
    reader = easyocr.Reader(["en"])

    # parse the pages
    puzzles = {}
    for page in tqdm(pages):
        _puzzles = parse_page(page, reader)
        check_disjoint(puzzles.keys(), _puzzles.keys())
        puzzles.update(_puzzles)

    # TODO outputting puzzles somewhere
