# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SstCore(AutotoolsPackage):
    """The Structural Simulation Toolkit (SST) core
       provides a parallel discrete event simulation (PDES)
       framework for performing architecture simulations
       of existing and proposed HPC systems"""

    homepage = "https://github.com/sstsimulator"
    git      = "https://github.com/sstsimulator/sst-core.git"

    version('9.1',     url="https://github.com/sstsimulator/sst-core/releases/download/v9.1.0_Final/sstcore-9.1.0.tar.gz",
            sha256="cfeda39bb2ce9f32032480427517df62e852c0b3713797255e3b838075f3614d")
    version('devel',   branch='devel')
    version('master',  branch='master', preferred=True)

    variant("pdes",   default=True, description="Build support for parallel discrete event simulation")
    variant("zoltan", default=False, description="Use Zoltan for partitioning parallel runs")
    variant("hdf5",   default=False, description="Build support for HDF5 statistic output")
    variant("zlib",   default=False, description="Build support for ZLIB compression")

    depends_on("python")
    depends_on("mpi", when="+pdes")
    depends_on("zoltan", when="+zoltan")
    
    @when('@devel')
    @when('@master')
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('autogen.sh')

    def configure_args(self):
      args = []
      if "+zoltan" in self.spec:
        args.append("--with-zoltan=%s" % self.spec["zoltan"].prefix)
      if "+hdf5" in self.spec:
        args.append("--with-hdf5=%s" % self.spec["hdf5"].prefix)
      if "+zlib" in self.spec:
        args.append("--with-zlib=%s" % self.spec["zlib"].prefix)

      if "+pdes" in self.spec:
        args.append("--enable-mpi")
      else:
        args.append("--disable-mpi")

      args.append("--with-python=%s" % self.spec["python"].prefix)

      return args
