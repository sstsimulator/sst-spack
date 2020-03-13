# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ramulator(MakefilePackage):
    """
    Ramulator is a fast and cycle-accurate DRAM simulator that supports a wide array of commercial, as well as academic, DRAM standards.
    """

    git = "https://github.com/CMU-SAFARI/ramulator"

    version('sst',
      git="git@github.com:CMU-SAFARI/ramulator.git",
      commit="7d2e72306c6079768e11a1867eb67b60cee34a1c")

    patch('ramulator_sha_7d2e723_gcc48Patch.patch', when="@sst")
    patch('ramulator_sha_7d2e723_libPatch.patch', when="@sst")
    
    def install(self, spec, prefix):
      install_tree("", prefix)

    def build(self, spec, prefix):
      if spec.satisfies("platform=darwin"):
        make("libramulator.a")
      else:
        make("libramulator.so")

