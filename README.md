![SST](http://sst-simulator.org/img/sst-logo-small.png)

# Structural Simulation Toolkit (SST) Spack Packages

#### Copyright (c) 2009-2018, Sandia National Laboratories
Sandia National Laboratories is a multimission laboratory managed and operated
by National Technology and Engineering Solutions of Sandia, LLC., a wholly 
owned subsidiary of Honeywell International, Inc., for the U.S. Department of 
Energy's National Nuclear Security Administration under contract DE-NA0003525.

## 
Make sure you have downloaded [Spack](https://github.com/spack/spack) and added it to your path.
The easiest way to do this is often (depending on your SHELL):
````
source spack/share/spack/setup-env.sh 
````

To get the most up-to-date version of the SST Spack packages, after downloading the sst-spack GitHub repository, you simply need to run
````
spack repo add sst-spack/sst
````
To validate that Spack now sees the repo with the SST packages, run:
````
spack repo list
````
This should now list your newly downloaded Spack repo.
You can display information about how to install the individual packages with, e.g.:
````
spack info sst-core
````
This will print all the information about variants and dependencies of the package.
For detailed instructions on how to use Spack, see the [Owner's Manual](https://spack.readthedocs.io).
