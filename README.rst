

======================================
Template OpenCMISS example - barebones
======================================

This example shows the barebones required for an examplar Fortran example.  For more detailed information refer to the `master <https://github.com/OpenCMISS-Examples/template_example/tree/master>`_ branch.

CMake files
===========

The *CMakeLists.txt* file in the root directory uses the following *find_package* command::

  find_package(OpenCMISSLibs 1.3.0 COMPONENTS iron REQUIRED CONFIG)

What is different here from the basic template in the `master <https://github.com/OpenCMISS-Examples/template_example/tree/master>`_ branch is that we have made use of the *COMPONENTS* option to indicate that only the Iron library is required for this example.

Remember
========

Replace this file with a description about your example using the `README.template.rst <README.template.rst>`_ file as a starting point.
