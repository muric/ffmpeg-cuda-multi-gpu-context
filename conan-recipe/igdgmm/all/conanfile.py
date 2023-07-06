from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools.files import (
    chdir, mkdir, get, export_conandata_patches
)

import os

class IgdgmmConan(ConanFile):
    name = "igdgmm"
    description = "Intel(R) Graphics Memory Management Library"
    settings = "os", "compiler", "build_type", "arch"
    #options = {"shared": [True,False]} #--disable-x11, --enable-shared
    #default_options = {}
    _source_folder = "source_dir"

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination=self._source_folder)

    def generate(self):
        with chdir(self, self.build_folder):
            tc = CMakeToolchain(self)
            tc.variables["PKG_CONFIG_USE_CMAKE_PREFIX_PATH"] = True
            tc.variables["BUILD_TYPE"] =  self.settings.build_type
            tc.variables["CMAKE_PREFIX_PATH"] = self.build_folder + "/" +  self._source_folder
            tc.variables["CFLAGS"] ="-Wno-error"
            tc.variables["CXXFLAGS"] ="-Wno-error"
            tc.generate()
        
    def build(self):
        with chdir(self, self.build_folder):
            #with chdir(self,self._source_folder):
            cmake = CMake(self)
            cmake.configure(build_script_folder=self._source_folder)
            cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["igdgmm"]
