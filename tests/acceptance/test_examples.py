"""
Verify that all example run scripts work correctly
"""

import sys
from os import environ
from pathlib import Path
from subprocess import call
import unittest
import pytest
from vunit.sim_if.common import has_simulator, simulator_check

ROOT = Path(__file__).parent.parent.parent


@unittest.skipIf(
    not has_simulator()
    or simulator_check(lambda simclass: not simclass.supports_vhpi()),
    "A simulator/backend that supports interfacing with external C code is required",
)
class TestExamples(unittest.TestCase):
    """
    Verify that example projects run correctly
    """

    def setUp(self):
        self.output_path = str(Path(__file__).parent / "examples_run_out")
        self.report_file = str(Path(self.output_path) / "xunit.xml")

    def check(self, run_file, args=None, vhdl_standard="2008", exit_code=0):
        """
        Run external run file and verify exit code
        """
        args = args if args is not None else []
        new_env = environ.copy()
        new_env["VUNIT_VHDL_STANDARD"] = vhdl_standard
        retcode = call(
            [sys.executable, run_file, "--output-path=%s" % self.output_path]
            + (args if args else []),
            env=new_env,
        )
        self.assertEqual(retcode, exit_code)

    def test_copy(self):
        self.check(
            str(ROOT / "examples" / "copy" / "run.py"),
            args=["--clean", "--xunit-xml=%s" % self.report_file],
        )

    def test_buffer(self):
        self.check(
            str(ROOT / "examples" / "buffer" / "run.py"),
            args=["--clean", "--xunit-xml=%s" % self.report_file],
        )

    @pytest.mark.xfail
    def test_buffer_dyn(self):
        self.check(
            str(ROOT / "examples" / "buffer" / "run.py"),
            args=["--build", "--xunit-xml=%s" % self.report_file],
        )
        self.check(
            str(ROOT / "examples" / "buffer" / "corun.py"), args=["tb_external_string"],
        )
        self.check(
            str(ROOT / "examples" / "buffer" / "corun.py"),
            args=["tb_external_byte_vector"],
        )
        self.check(
            str(ROOT / "examples" / "buffer" / "corun.py"),
            args=["tb_external_integer_vector"],
        )
