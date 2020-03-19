# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SstMacro(AutotoolsPackage):
    """The Structural Simulation Toolkit Macroscale Element Library simulates
    large-scale parallel computer architectures for the coarse-grained study
    of distributed-memory applications. The simulator is driven from either a
    trace file or skeleton application. SST/macro's modular architecture can
    be extended with additional network models, trace file formats, software
    services, and processor models.
    """

    homepage = "http://sst.sandia.gov/about_sstmacro.html"
    git      = "https://github.com/sstsimulator/sst-macro.git"

    version('master',  branch='master', preferred=True)
    version('devel', branch='devel')

    depends_on('autoconf@1.68:', type='build', when='@devel')
    depends_on('automake@1.11.1:', type='build', when='@devel')
    depends_on('libtool@1.2.4:', type='build', when='@devel')
    depends_on('m4', type='build', when='@devel')
    depends_on('autoconf@1.68:', type='build', when='@master')
    depends_on('automake@1.11.1:', type='build', when='@master')
    depends_on('libtool@1.2.4:', type='build', when='@master')
    depends_on('m4', type='build', when='@master')

    depends_on('binutils', type='build')
    depends_on('zlib', type=('build', 'link'))
    depends_on('otf2', when='+otf2')
    depends_on('llvm+clang@5:9', when='+skeletonizer')
    depends_on('mpi', when='+pdes-mpi')
    depends_on('sst-core@devel',   when='@devel +core')
    depends_on('sst-core@master',  when='@master +core')

    variant('pdes-threads', default=True, description='Enable thread-parallel PDES simulation')
    variant('pdes-mpi', default=False, description='Enable distributed PDES simulation')
    variant('core',     default=False, description='Use SST Core for PDES')
    variant('otf2',     default=False, description='Enable OTF2 trace emission and replay support')
    variant('skeletonizer', default=False, description='Enable Clang source-to-source autoskeletonization')

    variant('static', default=True, description='Build static libraries')
    variant('shared', default=True, description='Build shared libraries')

    variant('werror', default=False, description='Build with all warnings as errors')
    variant('warnings', default=False, description='Build with all possible warnings')

    # force out-of-source builds
    build_directory = 'spack-build'

    #this is not working with multiple decorators
    #TODO: make @when restrictions work
    #@when('@devel')
    #@when('@master')
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./bootstrap.sh')

    def configure_args(self):
        args = ['--disable-regex']

        spec = self.spec
        args.append(
            '--enable-static=%s' % ('yes' if '+static' in spec else 'no'))
        args.append(
            '--enable-shared=%s' % ('yes' if '+shared' in spec else 'no'))

        if spec.satisfies("@8.0.0:") or spec.satisfies("@devel") or spec.satisfies("@master"):
            args.extend([
                '--%sable-otf2' %
                  ('en' if '+otf2' in spec else 'dis'),
                '--%sable-multithread' %
                  ('en' if '+pdes-threads' in spec else 'dis')
            ])

            if '+skeletonizer' in spec:
                args.append('--with-clang=' + spec['llvm'].prefix)

        if spec.satisfies("@10:") or spec.satisfies("@devel") or spec.satisfies("@master"):
            if "+warnings" in spec:
              args.append("--with-warnings")
            if "+werror" in spec:
              args.append("--with-werror")

        if '+core' in spec:
            args.append('--with-sst-core=%s' % spec['sst-core'].prefix)

        # Optional MPI support
        needCoreMpi = False
        if "+core" in spec:
          if "+pdes-mpi" in spec["sst-core"]:
            needCoreMpi = True
        if '+pdes-mpi' in spec or needCoreMpi:
            env['CC'] = spec['mpi'].mpicc
            env['CXX'] = spec['mpi'].mpicxx
            env['F77'] = spec['mpi'].mpif77
            env['FC'] = spec['mpi'].mpifc

        return args
