from spack import *
from spack.pkg.builtin.intel_pin import IntelPin as ParentPin


class IntelPin(ParentPin):
    version('2.14',  
      url="https://software.intel.com/sites/landingpage/pintool/downloads/pin-2.14-71313-gcc.4.4.7-linux.tar.gz",
      sha256="1c29f589515772411a699a82fc4a3156cad95863a29741dfa6522865d4d281a1"
    )
