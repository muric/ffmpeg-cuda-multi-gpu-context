from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.files import (copy,
    export_conandata_patches)
import os

class ffnvcodecConan(ConanFile):
    name = "ffnvcodec"
    version = "12.0.16.0"
    settings = "os", "compiler", "arch", "build_type"
    description = "Nvidia codec headers for ffmpeg"
    build_policy = "missing"

#    def export_sources(self):
#        export_conandata_patches(self)
    
    def source(self):
        git = Git(self)
        git.clone(url="https://git.videolan.org/git/ffmpeg/nv-codec-headers.git", target=".")
        git.checkout("c5e4af74850a616c42d39ed45b9b8568b71bf8bf")

    def build(self):
        self.run("make PREFIX=%s" % self.package_folder)
        self.output.info("Header only package, skipping build")

    def package(self):
        copy(self, "*.h", self.build_folder, os.path.join(self.package_folder))
        #copy(self, "*.pc", self.build_folder, os.path.join(self.package_folder, "lib/pkgconfig"))

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        #self.cpp_info.libs = ["lib"]
