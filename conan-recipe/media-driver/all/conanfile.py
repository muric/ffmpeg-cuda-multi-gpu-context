from conan import ConanFile, tools
from conan.tools.cmake import CMake, CMakeToolchain
from conan.tools import CppInfo
from conan.tools.files import (
    copy, get, export_conandata_patches
)

import os

class MediaDriverConan(ConanFile):
    name = "media-driver"
    description = "media driver iHD for vaapi ffmpeg support"
    settings = "os", "compiler", "build_type", "arch"
    #package_type = "library" 
    # media driver not implemented static build 
    # https://github.com/intel/media-driver/issues/702
    options = {"enable_kernels": [True,False],
                "gen8": [True,False],
                "gen9": [True,False],
                "enable_nonfree_kenels":[True,False]
    }
    default_options = {
        "enable_kernels": True,
        "gen8": False,
        "gen9": False,
        "enable_nonfree_kenels": True,
    }
    _source_folder = "source_dir"

    def generate(self):
        libva = self.dependencies["libva"]
        igdgmm = self.dependencies["igdgmm"]
        tc = CMakeToolchain(self)
        tc.variables["PKG_CONFIG_USE_CMAKE_PREFIX_PATH"] = True
        tc.variables["BUILD_TYPE"] =  self.settings.build_type
        tc.variables["CMAKE_PREFIX_PATH"] = self.build_folder + "/" +  self._source_folder + ";" + libva.package_folder + ";" + igdgmm.package_folder
        tc.variables["CFLAGS"] ="-Wno-error"
        tc.variables["CXXFLAGS"] ="-Wno-error"
        if self.options.enable_kernels:
            tc.variables["ENABLE_KERNELS"] = "ON"
        else:
            tc.variables["ENABLE_KERNELS"] = "OFF"
        if self.options.gen8:
            tc.variables["GEN8"] = "ON"
        else:
            tc.variables["GEN8"] = "OFF"
        if self.options.gen9:
            tc.variables["GEN9"] = "ON"
        else:
            tc.variables["GEN9"] = "OFF"
        if self.options.enable_nonfree_kenels:
            tc.variables["ENABLE_NONFREE_KERNELS"] = "ON"
        else:
            tc.variables["ENABLE_NONFREE_KERNELS"] = "OFF"
        tc.variables["PKG_CONFIG_USE_CMAKE_PREFIX_PATH"] = True
        tc.generate() 

    def requirements(self):
        self.requires("libva/2.14@self-muradyan/stable")
        self.requires("igdgmm/22.1.2@self-muradyan/stable")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination=self._source_folder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder=self._source_folder)
        cmake.build()

    def package(self):
        copy(self, "*.h", self.build_folder, os.path.join(self.package_folder + "/include/")) #copy headers
        copy(self, "*.so", self.build_folder, os.path.join(self.package_folder + "/lib/"),keep_path=False) # copy shared lib
        copy(self, "*.a", self.build_folder, os.path.join(self.package_folder + "lib/"),keep_path=False) # copy static lib
        #copy("*.h", dst="include", keep_path=False)
        #copy("*.so", dst="lib", keep_path=False)
        #copy("*.a", dst="lib", keep_path=False)
        cmake = CMake(self)
        cmake.install()
        

    def package_info(self):
        self.cpp_info.libs = ["iHD"]

