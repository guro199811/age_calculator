import os


def absolute_path(file=__file__, path=".") -> str:
    """
    Converts a relative path to an absolute path
    :param path: Relative path
    :return: Absolute path
    """
    return os.path.abspath(os.path.join(os.path.dirname(file), path))
