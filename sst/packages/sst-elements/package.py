# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SstElements(AutotoolsPackage):
    """SST Elements implements a range of components for performing
       architecture simulation from node-level to system-level using
       the SST discrete event core
    """

    homepage = "https://github.com/sstsimulator"
    git      = "https://github.com/sstsimulator/sst-elements.git"

    version('9.1',    
      url="https://github.com/sstsimulator/sst-elements/releases/download/v9.1.0_Final/sstelements-9.1.0.tar.gz",
      sha256="e19b05aa6e59728995fc059840c79e476ba866b67887ccde7eaf52a18a1f52ca"
    )
    version('devel',   branch='devel')
    version('master',  branch='master', preferred=True)

    variant("pin",       default=False, description="Enable the Ariel CPU model")
    variant("dramsim2",  default=False, description="Build with DRAMSim2 support")
    variant("nvdimmsim", default=False, description="Build with NVDimmSim support")
    variant("hybridsim", default=False, description="Build with HybridSim support")
    variant("goblin",    default=False, description="Build with GoblinHMCSim support")
    variant("hbm",       default=False, description="Build with HBM DRAMSim2 support")
    variant("ramulator", default=False, description="Build with Ramulator support")

    depends_on("python")
    depends_on("sst-core")
    depends_on("sst-core@devel", when="@devel")
    depends_on("sst-core@master", when="@master")

    depends_on("intel-pin@2.14", when="+pin")
    depends_on("dramsim2@2.2",   when="+dramsim2")
    depends_on("hybridsim@2.0",  when="+hybridsim")
    depends_on("nvdimmsim@2.0",  when="+nvdimmsim")
    depends_on("goblin-hmc-sim", when="+goblin")
    depends_on("ramulator@sst",  when="+ramulator")
    depends_on("hbm-dramsim2",   when="+hbm")

    #normally wouldn't need to specify indirect deps
    #but we do in this case so they are available in the spec
    depends_on("dramsim2@2.2",   when="+hybridsim")
    depends_on("nvdimmsim@2.0",  when="+hybridsim")

    depends_on('autoconf@1.68:', type='build', when='@devel')
    depends_on('automake@1.11.1:', type='build', when='@devel')
    depends_on('libtool@1.2.4:', type='build', when='@devel')
    depends_on('m4', type='build', when='@devel')
    depends_on('autoconf@1.68:', type='build', when='@master')
    depends_on('automake@1.11.1:', type='build', when='@master')
    depends_on('libtool@1.2.4:', type='build', when='@master')
    depends_on('m4', type='build', when='@master')

    # force out-of-source builds
    build_directory = 'spack-build'

    #multiple decorators is not working
    #TODO: make @when restrictions on this
    #@when('@devel')
    #@when('@master')
    def autoreconf(self, spec, prefix):
      bash = which('bash')
      bash('autogen.sh')

    def configure_args(self):
      args = []
      if '+pdes-mpi' in self.spec["sst-core"]:
        env['CC'] = spec['mpi'].mpicc
        env['CXX'] = spec['mpi'].mpicxx
        env['F77'] = spec['mpi'].mpif77
        env['FC'] = spec['mpi'].mpifc

      if "+pin" in self.spec:
        args.append("--with-pin=%s" % self.spec["intel-pin"].prefix)

      if "+dramsim2" in self.spec or "+hybridsim" in self.spec:
        args.append("--with-dramsim=%s" % self.spec["dramsim2"].prefix)

      if "+nvdimmsim" in self.spec or "+hybridsim" in self.spec:
        args.append("--with-nvdimmsim=%s" % self.spec["nvdimmsim"].prefix)

      if "+hybridsim" in self.spec:
        args.append("--with-hybridsim=%s" % self.spec["hybridsim"].prefix)

      if "+goblin" in self.spec:
        args.append("--with-goblin-hmcsim=%s" % self.spec["goblin-hmc-sim"].prefix)

      if "+hbm" in self.spec:
        args.append("--with-hbmdramsim=%s" % self.spec["hbm-dramsim2"].prefix)

      if "+ramulator" in self.spec:
        args.append("--with-ramulator=%s" % self.spec["ramulator"].prefix)

      args.append("--with-sst-core=%s" % self.spec["sst-core"].prefix)
      return args
