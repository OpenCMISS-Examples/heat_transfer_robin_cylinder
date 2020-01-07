

=================
Example Name Here
=================

Short synopsis of the example.

Building the example
====================

If this not a pure Python example place the instructions here on how to configure and build with CMake::

  git clone https://github.com/you/your-example.git # maybe your example is somewhere else like: OpenCMISS-Examples
  mkdir build
  cmake -DOpenCMISSLibs_DIR=/path/to/opencmisslib/install ../your-example
  make  # cmake --build . will also work here and is much more platform agnostic.

Running the example
===================

Explain how the example is run::

  cd build
  ./src/fortran/XXXXXXXX

or maybe it is a Python only example::

  source /path/to/opencmisslibs/install/virtaul_environments/oclibs_venv_pyXY_release/bin/activate
  python src/python/XXXXXXXX.py

where the XY in the path are the Python major and minor versions respectively.

Verifying the example
=====================

Explain here how to compare the expected output with the actual output, and where the expected output can be found.

Prerequisites
=============

Are there any external sources that are required over and above CMake, OpenCMISS libraries.  Sources like meshes which might be stored outside of the example itself.

License
=======

A line on the license applicable to this example.
