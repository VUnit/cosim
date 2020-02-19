> **This repository is in a very early planning phase. Although the VHPIDIRECT bridge for GHDL is functional, breaking changes are being discussed in [VUnit/vunit#603](https://github.com/VUnit/vunit/issues/603)**.

   <p align="center">
     <a title="Visit vunit.github.io"
        href="https://vunit.github.io/cosim"
     ><img src="https://img.shields.io/website/http/vunit.github.io/cosim/index.html.svg?longCache=true&style=flat-square&label=vunit.github.io%2Fcosim"
     /></a><!--
     -->
     <a title="Join the chat at https://gitter.im/VUnit/vunit"
        href="https://gitter.im/VUnit/vunit"
     ><img src="https://img.shields.io/gitter/room/VUnit/vunit.svg?longCache=true&style=flat-square&logo=gitter&logoColor=4db797&color=4db797"
     /></a><!--
     -->
     <a title="'docs' workflow Status"
        href="https://github.com/VUnit/cosim/actions?query=workflow%3Adocs"
     ><img alt="'docs' workflow Status" src="https://img.shields.io/github/workflow/status/VUnit/cosim/docs?longCache=true&style=flat-square&label=docs"
     /></a><!--
     -->
     <a title="'push' workflow Status"
        href="https://github.com/VUnit/cosim/actions?query=workflow%3Apush"
     ><img alt="'push' workflow Status" src="https://img.shields.io/github/workflow/status/VUnit/cosim/push?longCache=true&style=flat-square&label=push"
     /></a>
   </p>

# Interfacing VHDL and foreign languages with [VUnit](https://github.com/VUnit/vunit)

Three main approaches are used to co-simulate (co-execute) VHDL sources along with software applications written in a different language (typically C/C++):

- Verilog Procedural Interface (VPI), also known as Program Language Interface (PLI) 2.0.
- VHDL Procedural Interface (VHPI), or specific implementations, such as Foreign Language Interface (FLI).
- Generation of C/C++ models/sources through a transpiler.

This repository aims to gather resources to use these techniques with VUnit. The content is organised in **bridges**, **examples** and **utils**:

- Bridges contain VHDL packages, (optionally) matching C headers and Python classes. Each bridge provides the glue logic between a VHDL API (or another bridge) and some other API in VHDL and/or C (bindings).
- Examples are working demo projects that use some utils and/or bridges. Dockerfiles are included in the examples that require additional FOSS tools.
- Utils contains helper functions in Python (based on `ctypes`, `base64`, `numpy` and `Pillow`) which are useful for interacting with C-alike executables.
