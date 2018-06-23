Buildbm is a simple package manager for BareMetal system.


This project is inspired by Buildroot.

https://buildroot.org/


How to Build
============

Install Kconfiglib and SCons

    $ pip install kconfiglib scons

Create your toolchain config to toolchain directory.
And modify toolchain/Kconfig to use your toolchain.

Customize system config for your convinient.
    $ menuconfig
(menuconfig command is included in Kconfiglib)

Go!
    $ scons

This SConstruct generates 'build/<target>/libbuildbm.a'.

Link 'libbuildbm.a' to your baremetal system, and enjoy!

Your toolchain must support libc (including printf,malloc,libm) ,
libbuildbm.a depends on libc, but libbuildbm.a does not include libc.



Add your favorite package to Buildbm
====================================

Build package directory in packages.

Add BMconfig and package.py in your package direcotry.
and add the 'BMconfig' path to packages/BMconfig.

'BMconfig' defines config flags for your package,
BMconfig syntax is same as Linux Kconfig

https://www.kernel.org/doc/Documentation/kbuild/kconfig-language.txt


'package.py' defines source file list in your package.
Many baremetal system uses special Makefile.
Therefore, in most cases default Makefile cannot use for baremetal system.

You should define source file list, cflags or preprocessor flags yourself.

'package.py' can define some global variables.
these variables are used in build process.

Follows are description for these variables.

 - PACKAGE_NAME : name of your package. This should be unique in all packages.
 - PACKAGE_URL : The URL of source file
 - INSTALL_HEADERS : header file list to build other package. 
   The files specifined in this variable are installed to build/<target>/include.
 - SOURCES : c/c++ files to build.
 - DEPENDENCIES : The package list used by this package
 - CFLAGS : package specific cflags
 - CXXFLAGS : packages specific c++flags

