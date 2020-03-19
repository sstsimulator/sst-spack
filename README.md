![SST](http://sst-simulator.org/img/sst-logo-small.png)

# Structural Simulation Toolkit (SST) Spack Packages

#### Copyright (c) 2009-2018, Sandia National Laboratories
owned subsidiary of Honeywell International, Inc., for the U.S. Department of
Energy's National Nuclear Security Administration under contract DE-NA0003525.

## Basic Usage
Make sure you have downloaded [Spack](https://github.com/spack/spack) and added it to your path.
The easiest way to do this is often (depending on your SHELL):
````
> source spack/share/spack/setup-env.sh
````

To get the most up-to-date version of the SST Spack packages, after downloading the sst-spack GitHub repository, you simply need to run
````
> spack repo add sst-spack/sst
````
To validate that Spack now sees the repo with the SST packages, run:
````
> spack repo list
````
This should now list your newly downloaded Spack repo.
You can display information about how to install the individual packages with, e.g.:
````
> spack info sst-core
````
This will print all the information about variants and dependencies of the package.
For detailed instructions on how to use Spack, see the [Owner's Manual](https://spack.readthedocs.io).

A basic installation of a package is done as:
````
> spack install sst-core +pdes-mpi
````
which tells Spack to install the core with PDES support using MPI.
For downstream packages like sst-elements, sst-core and all dependencies will be automatically installed.
We can visualize this with either `spack spec` or `spack graph`, e.g.
````
> spack spec sst-elements +pin +hybridsim
Input spec
--------------------------------
sst-elements+hybridsim+pin

Concretized
--------------------------------
sst-elements@master%gcc@7.4.0~dramsim2~goblin~hbm+hybridsim~nvdimmsim+pin~ramulator arch=linux-centos7-haswell
    ^autoconf@2.69%gcc@7.4.0 arch=linux-centos7-haswell
    ^automake@1.16.1%gcc@7.4.0 arch=linux-centos7-haswell
    ^dramsim2@2.2%gcc@7.4.0 arch=linux-centos7-haswell
    ^hybridsim@2.0%gcc@7.4.0 patches=e266e00e3777feb1d9b3691f6a5a88d1d99c5aa0e0811fcf5461d55e0ac4a7bd arch=linux-centos7-haswell
        ^nvdimmsim@2.0%gcc@7.4.0 arch=linux-centos7-haswell
    ^intel-pin@2.14%gcc@7.4.0 arch=linux-centos7-haswell
    ^libtool@2.4.6%gcc@7.4.0 arch=linux-centos7-haswell
    ^python@2.7%gcc@7.4.0+bz2+ctypes+dbm~debug+libxml2+lzma~nis~optimizations+pic+pyexpat+pythoncmd+readline+shared+sqlite3+ssl~tix~tkinter~ucs4~uuid+zlib arch=linux-centos7-haswell
    ^sst-core@master%gcc@7.4.0~hdf5+pdes-mpi~zlib~zoltan arch=linux-centos7-haswell
        ^openmpi@3.1.5%gcc@7.4.0~cuda+cxx_exceptions fabrics=none ~java~legacylaunchers~memchecker~pmi schedulers=none ~sqlite3~thread_multiple+vt arch=linux-centos7-haswell
````
This shows what will be installed along with the specification of all the dependencies.
If any of the dependencies are missing, Spack will download and install them.
Note here that the default compiler for this Spack is GCC 7.4.
If we wish to use a different compiler, we can specify it as, e.g:
````
> spack install sst-elements +pin +hybridsim %clang@9.1.0
````
To make sure your desired compiler is known to Spack, you can check:
````
> spack compiler list
==> Available compilers
-- clang centos7-x86_64 -----------------------------------------
clang@7.0.0

-- gcc centos7-x86_64 -------------------------------------------
gcc@7.4.0  gcc@4.8.5
````
All compilers in the path are usually located by running `spack compiler find` and automatically added.

## Testing and Developing with Spack
Spack has historically been much more suited to *deployment* of mature packages than active testing or developing.
However, recent features have improved support for development.
Future releases are likely to make this even easier and incorporate Git integration.

### Testing
A common pattern in testing is validating a successful build of feature branches.
Spack provides the `dev-build` feature for building and installing from a custom source folder.
For example:
````
> git clone git@github.com:sstsimulator/sst-core.git -b devel src
> spack dev-build -d src sst-core@devel +pdes-mpi 
````
is equivalent to just running
````
> spack install sst-core@devel +pdes-mpi
````
For validating a complete build of the "core" packages (sst-core, sst-elements, sst-macro) with any combination of branches, one can simply run:
````
> git clone git@github.com:sstsimulator/sst-core.git -b feature-core sst-core-src
> git clone git@github.com:sstsimulator/sst-macro.git -b devel sst-macro-src
> git clone git@github.com:sstsimulator/sst-elements.git -b feature-elems sst-elements-src
> spack dev-build -d sst-core-src sst-core@devel core-variants... %compiler
> spack dev-build -d sst-macro-src sst-macro@devel macro-variants... ^sst-core@devel core-variants... %compiler
> spack dev-build -d sst-elements-src sst-elements@devel elem-variants... ^sst-core@devel core-variants... %compiler
````
Here `%compiler` is a spec like `gcc@7.4.0`.
`core-variants...` is the desired sst-core spec like `+pdes-mpi +zoltan`.
Note the the `^` syntax used here to ensure that sst-elements and sst-macro depend on a precise variant of sst-core.
For example:
````
> spack dev-build -d sst-macro-src sst-macro@devel +otf2 +core ^sst-core+pdes-mpi+zoltan
````
Because we are doing feature branch testing, we use `@devel` to build the branches as-if they were the `devel` branch.

### Developing
The above commands will do a full build and install of the packages.
If doing development, you may wish to merely set up a build environment.
This allows you to modify the source and re-build.
In this case, you can stop after configuring:
````
> spack dev-build -d sst-core-src -u configure sst-core@devel +otf2 +core ^sst-core+pdes-mpi+zoltan
````
This sets up a development environment for you in `sst-core-src`, which you can use (Bash example shown):
````
> cd sst-core-src
> source spack-build-env.txt
> cd spack-build
> make
````
Before sourcing the Spack development environment, you may wish to save your current environment:
````
> declare -px > myenv.sh
````
When done with Spack, you can then restore your original environment:
````
source myenv.sh
````

## Configuring Default Spack Packages
Spack assumes nothing is available on your system, including even basic utilities like Perl and M4.
This leads to Spack "bootstrapping" for each new install (and each compiler!) many, many packages.
It is recommended to set up a `packages.yaml` file in a `$HOME.spack` folder that identifies your default local packages.
Below is an example file with the most important packages for efficient SST development:
````
packages:
 zlib:
  paths:
    zlib: /usr
  buildable: False
 libtool:
  paths:
   libtool@2.4.6: /opt/local
  buildable: False
 cmake:
  paths:
   cmake@3.15: /opt/local
  buildable: False
 pkg-config:
  paths:
   pkg-config: /opt/local
 m4:
  paths:
    m4: /usr
  buildable: False
 numactl:
  paths:
   numactl@2.0.12: /opt/local
   buildable: False
 hwloc:
  paths:
   hwloc@2.0.2: /usr
   hwloc@1.11: /opt/local
   buildable: False
 python:
  paths:
   python@2.7: /usr
   python@3.6: /opt/local
  variants: +shared
  buildable: False
````
The paths would need to be updated for your system.
If you *never* want Spack to re-build a library (which is often the case for C libraries like hwloc),
you need the `buildable: False` entry.
In most cases a single version suffices, but you may need multiple versions to resolve conflicts (as was the caes here for Python and hwloc).
In other cases, you may need to identify the Spack variants supported by your local installation.
In this case, we had to inform Spack that our Python has shared libraries.
With the `packages.yaml`, our Spack dependency graph for `spack graph sst-core +pdes-mpi` is:
````
o  sst-core
|\
| o  openmpi
| |\
| | |\
| o | |  zlib
|  / /
o | |  python
 / /
 o |  numactl
  /
  o  hwloc
````
In this case, the only dependency Spack will build is `openmpi` (recommended due to the compiler dependence).
Without the `packages.yaml`, a huge dependency graph would be built:
````
o  sst-core
|\
o |  python
|\ \
| |\ \
| | |\ \
| | | |\ \
| | | | |\ \
| | | | | |\ \
| | | | | | |\ \
| | | | | | | |\ \
| | | | | | | | |\ \
| | | | | | | | | |\ \
| | | | | | | | | | |\ \
| | o | | | | | | | | | |  sqlite
| |/| | | | | | | | | | |
|/| | | | | | | | | | | |
| | |/ / / / / / / / / /
| | | | o | | | | | | |  openssl
| |_|_|/| | | | | | | |
|/| | | | | | | | | | |
| | | | | | | | | | | o  openmpi
| |_|_|_|_|_|_|_|_|_|/|
|/| | | | | | | | | | |
| | | | | | | | | | | |\
| | | | | | | | | | | | o  hwloc
| | | | |_|_|_|_|_|_|_|/|
| | | |/| | | | | | | |/|
| | | | | | | | | | | | |\
| | | | | | | o | | | | | |  gettext
| | |_|_|_|_|/| | | | | | |
| |/| | | | |/| | | | | | |
| | | | | |/| | | | | | | |
| | | | | | | |\ \ \ \ \ \ \
| | | | | | | | |\ \ \ \ \ \ \
| | | | | | | | | |_|_|_|_|/ /
| | | | | | | | |/| | | | | |
| | | | | | | | | | |/ / / /
| | | | | | | | | |/| | | |
| | | | | | | | o | | | | |  libxml2
| |_|_|_|_|_|_|/| | | | | |
|/| |_|_|_|_|_|/| | | | | |
| |/| | |_|_|_|/| | | | | |
| | | |/| | | | | | | | | |
o | | | | | | | | | | | | |  zlib
 / / / / / / / / / / / / /
 o | | | | | | | | | | | |  xz
  / / / / / / / / / / / /
  | | | | | | | | | | | o  libpciaccess
  | | |_|_|_|_|_|_|_|_|/|
  | |/| | | | | | | | | |
  | | | | | | | | | | | |\
  | | | | | | | | | | | o |  util-macros
  | | | | | | | | | | |  /
  | | | | | o | | | | | |  tar
  | | | | | |/ / / / / /
  | | | | | | | | | o |  numactl
  | | | | | | | | | |\|
  | | | | | | | | | |\ \
  | | | | | | | | | | |\ \
  | | | | | | | | | | o | |  automake
  | | | |_|_|_|_|_|_|/| | |
  | | |/| | | | | | | | | |
  | | | | | | | | | | |/ /
  | | | | | | | | | | o |  autoconf
  | | | |_|_|_|_|_|_|/| |
  | | |/| | | | | | |/ /
  | | o | | | | | | | |  perl
  | | | |_|_|_|/ / / /
  | | |/| | | | | | |
  | | o | | | | | | |  gdbm
  | |/ / / / / / / /
  |/| | | | | | | |
  o | | | | | | | |  readline
  | |/ / / / / / /
  |/| | | | | | |
  o | | | | | | |  ncurses
  |/ / / / / / /
  o | | | | | |  pkgconf
   / / / / / /
   | | | | | o  libtool
   | | | | |/
   | | | | o  m4
   | | | | o  libsigsegv
   | | | |
   | | o |  bzip2
   | | o |  diffutils
   | |/ /
   | o |  libiconv
   |  /
   o |  libffi
    /
    o  expat
    o  libbsd
````

