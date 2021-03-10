from PIL import Image
import numpy as np


PALETTE_SHORT = "@%#*+=-:. "


def resize_image(image, max_dimension):
    """
    Specify a maximum height or width to resize the image, while maintaing the aspect ratio.
    :type image: PIL.Image
    :type max_dimension: int
    :rtype: None
    """
    max_size = (max_dimension, max_dimension)
    return image.thumbnail(max_size, Image.ANTIALIAS)


def convert_to_ascii_matrix(image, palette):
    """
    Convert the greyscaled image into a matrix with ASCII characters.
    Specify the greyscale character ramp (palette)
    :type image: PIL.Image
    :type palette: str
    :rtype: List[List[str]]
    """
    matrix = np.asarray(image)  # Read image as matrix of pixel values

    rows, cols = len(matrix), len(matrix[0])
    res = [[None for _ in range(cols)] for _ in range(rows)]

    hi, lo = matrix.max(), matrix.min()
    variance = hi - lo

    for i, row in enumerate(matrix):
        for j, v in enumerate(row):
            # Scale values to corresponding palette character
            idx = ((v - lo) * (len(palette)-1)) // variance
            c = palette[idx]
            res[i][j] = c

    return res


def convert_to_string_array(matrix):
    """
    Convert the ascii matrix to a string for output
    :type matrix: List[List[str]]
    :rtype: str
    """
    res = []
    for row in matrix:
        res.append(''.join(row))
    return '\n'.join(res)
