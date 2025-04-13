import os
import sys


def get_base_path() -> str:
    """Get the base path for resources in both PyInstaller and normal modes"""
    if getattr(sys, "frozen", False):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def absolute_path(file=__file__, path=".") -> str:
    """
    Converts a relative path to an absolute path
    :param path: Relative path
    :return: Absolute path
    """
    return os.path.abspath(os.path.join(os.path.dirname(file), path))


def get_resource_path(relative_path=".") -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = get_base_path()
    return os.path.join(base_path, relative_path)


def check_database_path(dir="database", db="history.db") -> str:
    """Get database path that works in both PyInstaller and normal modes"""
    base_path = get_base_path()
    db_dir = os.path.join(base_path, dir)

    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    database_path = os.path.join(db_dir, db)
    return f"sqlite:///{database_path}"
