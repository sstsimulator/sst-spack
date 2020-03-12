# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class Hybridsim(MakefilePackage):
    """
    HybridSim provides cycle-accurate simulation of a non-volatile memory system augmented with a DRAM based cache. It uses DRAMSim2 for the DRAM model and NVDIMMSim for the non-volatile memory model
    """

    git = "https://github.com/jimstevens2001/HybridSim"

    version('2.0',     
      url="https://github.com/jimstevens2001/HybridSim/archive/v2.0.1.tar.gz",
      sha256="57b82ac929acd36de84525e4d61358f1ab6532f5b635ca3f560e563479921937")

    depends_on("dramsim2")
    depends_on("nvdimmsim")
    patch("makefile.patch", when="@2.0")
    
    def install(self, spec, prefix):
      install_tree("", prefix)

    def build(self, spec, prefix):
      #os.chdir("..")
      symlink(spec["dramsim2"].prefix, "DRAMSim2")
      #os.mkdir("NVDIMMSim")
      #os.chdir("NVDIMMSim")
      #symlink(spec["nvdimmsim"].prefix, "src")
      symlink(spec["nvdimmsim"].prefix, "NVDIMMSim")
      #os.chdir("..")
      #os.chdir("spack-src")
      if spec.satisfies("platform=darwin"):
        make("libhybridsim.dylib")
      else:
        make("libhybridsim.so")
