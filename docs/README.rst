============
pybundler2
============
A python module for generating "installer" scripts for software environments.

:Version:
	0.1.0 as of (9 Nov 2015)
:Authors:
	Shonte Amato-Grill (`github`_)
:License:
	MIT
:Python:
	2.7 (working)
:OS:
	Linux, (Windows support planned)
:Status:
	Under Development

.. _github: https://github.com/shonteag

Intent
======
To build a python module, capable of "bundling" an entire directory into a single
file, capable of "installing itself" when executed by the user.  It should be
capable of handling all types of files, directory structures, and pathing schema.


Installation & Setup
====================
**Installation**
Typical python module installation.

1) download tarball or source code
2) extract to ``site-packages``
3) ``$ python setup.py install``

**Testing**
If installed from source, included test suite can be run with ``$ nosetests``

Use
===
pybundler has two command-line entry points:
1) ``$ pybundler-bundle``
2) ``$ pybundler-build``

**bundle**
Considered step 1, ``pybundler-bundle`` command takes as main argument a directory path.
Following said path, pybundler will create a ``.bundle`` file, of json format, detailing
all necessary properties of the directory, for execution of the ``build`` command.

**build**
Considered step 2, ``pybundler-build`` command takes a ``.bundle`` file as main argument,
and uses the details within to compile a "install" file (usually a bash script) which will
recreate the original target directory on a system.

At present time, only a LINUX BASH template is included. Windows BATCH format is planned
future functionality, but as of yet, unimplemented.


