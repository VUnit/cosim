# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2019, Lars Asplund lars.anders.asplund@gmail.com

"""
PEP8 check
"""

import unittest
from subprocess import check_call
from sys import executable
from glob import glob
from pathlib import Path


def get_files_and_folders():
    """
    Return all files and folders which shall be arguments to pycodestyle and pylint
    """
    root = Path(__file__).parent.parent.parent
    ret = list(glob(str(root / "**" / "*.py"), recursive=True))
    ret.remove(str(root / "docs" / "conf.py"))
    return ret


class TestMyPy(unittest.TestCase):
    """
    Run MyPy static type analysis
    """

    @staticmethod
    def test_mypy():
        check_call([executable, "-m", "mypy", "cosim"])


class TestPycodestyle(unittest.TestCase):
    """
    Test that all python code follows PEP8 Python coding standard
    """

    @staticmethod
    def test_pycodestyle():
        check_call(
            [
                executable,
                "-m",
                "pycodestyle",
                "--show-source",
                "--show-pep8",
                "--max-line-length=120",
                # W503 mutually exclusive with W504
                # E722 bare except checked by pylint
                "--ignore=E402,W503,E722,E501,E203",
            ]
            + get_files_and_folders()
        )


class TestPylint(unittest.TestCase):
    """
    Check that there are no pylint errors or warnings
    """

    @staticmethod
    def test_pylint():
        check_call(
            [
                executable,
                "-m",
                "pylint",
                "--rcfile=" + str(Path(__file__).parent / "pylintrc"),
            ]
            + get_files_and_folders()
        )
