# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GoblinHmcSim(MakefilePackage):
    """
    The Goblin HMC-Sim is a Hybrid Memory Cube Functional Simulation Environment
    """

    git = "https://github.com/tactcomplabs/gc64-hmcsim"

    version('1.0',
      url="https://github.com/tactcomplabs/gc64-hmcsim/archive/sst-8.0.0-release.tar.gz",
      sha256="8a5e6b701865a581f15965d3ddd8c7d301b15f4b63543c444058e9c3688fd2c8")
    
    def install(self, spec, prefix):
      install_tree("", prefix)

    def build(self, spec, prefix):
      make()
