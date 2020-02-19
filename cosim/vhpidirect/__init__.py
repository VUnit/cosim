"""
VHPIDIRECT VUnit co-simulation bridge
"""

import re
from os import linesep, makedirs
from pathlib import Path
from shutil import copyfile
from vunit import ROOT as SROOT  # type: ignore

ROOT = Path(SROOT)


class VHPIDIRECT:
    """
    VHPIDIRECT VUnit co-simulation bridge class

    :param srcs: optional alternative location of the sources
    """

    def __init__(self, srcs=None):
        self._srcs = Path(srcs) if srcs is not None else Path(__file__).parent

    def bridge(self, features=None):
        """
        Get lists of files to register the bridge with ``vu.add_builtins``

        :param features: struct,``{'string': <VAL>, 'integer': <VAL> }``, to provide
                         bridges for the external VHDL API. Accepted values are
                         ``True``, ``False``, ``None`` or ``['path/to/custom/file']``.
        """
        funcs = {
            "string": {
                "write_char : procedure": "write_char",
                "read_char : function": "read_char",
                "get_ptr : function": "get_string_ptr",
            },
            "integer_vector": {
                "write_integer : procedure": "write_integer",
                "read_integer : function": "read_integer",
                "get_ptr : function": "get_intvec_ptr",
            },
        }

        api = {"string": True, "integer_vector": True}
        for key in api:
            if key in features:
                val = features[key]
                if val is not True:
                    api[key] = val
                else:
                    dname = self._srcs / "vhdl" / ("%s.vhd" % key)
                    api[key] = [str(dname)]

                    try:
                        makedirs(str(dname.parent), 0o755)
                    except FileExistsError:
                        pass

                    attrs = linesep
                    for fkey, fval in funcs[key].items():
                        attrs += '  attribute foreign of %s is "VHPIDIRECT %s";%s' % (
                            fkey,
                            fval,
                            linesep,
                        )

                    # Instead of providing separate VHDL sources, in this bridge we patch
                    # the reference API definition sources from VUnit/vunit
                    with (
                        ROOT
                        / "vunit"
                        / "vhdl"
                        / "data_types"
                        / "src"
                        / "api"
                        / ("external_%s_pkg.vhd" % key)
                    ).open() as sfptr:
                        with dname.open("w") as dfptr:
                            dfptr.write(
                                re.sub("(end package;)", attrs + r"\1", sfptr.read())
                            )
        return api

    @property
    def include(self):
        """
        Get path to include directories containing C sources/headers
        """
        return [str(self._srcs / "c")]

    def verscript(self, file=None):
        """
        Get argument to add a custom version-script file to GHDL

        :param file: provide a custom file instead of the one provided with the bridge
        """
        return "-Wl,-Wl,--version-script=%s" % (
            file if file is not None else str(self._srcs / "c" / "grt.ver")
        )

    @staticmethod
    def post_func(results):
        """
        Optional post-func to copy runtime args for each test/executable to output subdir 'cosim'
        """
        report = results.get_report()
        cosim_args_dir = Path(report.output_path) / "cosim"

        try:
            makedirs(str(cosim_args_dir))
        except FileExistsError:
            pass

        for key, item in report.tests.items():
            copyfile(
                str(Path(item.path) / "ghdl" / "args.json"),
                str(
                    cosim_args_dir / ("%s.json" % re.search(r"lib\.(.+)\.all", key)[1])
                ),
            )
