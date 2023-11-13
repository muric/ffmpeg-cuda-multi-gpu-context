from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.files import (copy,
    export_conandata_patches)
import os

class amfConan(ConanFile):
    name = "amf"
    version = "v1.4.30"
    settings = "os", "compiler", "arch", "build_type"
    description = "AMF codec headers for ffmpeg"
    build_policy = "missing"
    amf_header = "amf/public/include/"

    def source(self):
        git = Git(self)
        git.clone(url="https://github.com/GPUOpen-LibrariesAndSDKs/AMF.git", target=".")
        git.checkout("a118570647cfa579af8875c3955a314c3ddd7058")

    def build(self):
        self.output.info("Header only package, skipping build")

    def package(self):
        copy(self, "*", os.path.join(self.build_folder, self.amf_header), os.path.join(self.package_folder,"include","AMF"))

    def package_info(self):
        self.cpp_info.includedirs = ["include"]

    def package_id(self):
        self.info.clear()