# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class HbmDramsim2(MakefilePackage):
    """
    HBM Simulator based on DRAMSim2; a small source-code change with HBM configuration.
    """

    git = "https://github.com/tactcomplabs/HBM"

    version('1.0',
      url="https://github.com/tactcomplabs/HBM/archive/hbm-1.0.0-release.tar.gz",
      sha256="0efad11c58197edb47ad1359f8f93fb45d882c6bebcf9f2143e0df7a719689a0")
    
    def install(self, spec, prefix):
      install_tree("", prefix)

    def build(self, spec, prefix):
      make()
