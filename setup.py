"""
PyPI setup script
"""

from pathlib import Path
from os.path import relpath
from glob import glob
from setuptools import setup

ROOT = Path(__file__).parent / "cosim"


def find_files():
    """
    Find all files to be packaged
    """
    return [
        relpath(item, "cosim")
        for item in (
            list(glob(str(ROOT / "vhpidirect" / "c" / "*")))
            + list(glob(str(ROOT / "xyce" / "c" / "*")))
            + list(glob(str(ROOT / "xyce" / "vhdl" / "*")))
            + list(glob(str(ROOT / "websim" / "vhdl" / "*")))
            + list(glob(str(ROOT / "websim" / "app" / "*")))
            + list(glob(str(ROOT / "websim" / "app" / "public" / "*")))
            + list(
                glob(str(ROOT / "websim" / "app" / "src" / "**" / "*"), recursive=True)
            )
        )
        if Path(item).is_file()
    ]


setup(
    name="vunit_cosim",
    # version=version(),
    packages=["tests.acceptance", "tests.lint", "cosim", "cosim.vhpidirect"],
    package_data={"cosim": find_files()},
    zip_safe=False,
    url="https://github.com/VUnit/cosim",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    python_requires=">=3.6",
    # install_requires=["vunit_hdl>4.4.0"],
    description=(
        "Resources for interfacing VHDL and foreign languages with VUnit,"
        "an open source unit testing framework"
    ),
)
