from conan import ConanFile
from conan import tools
from conan.tools.layout import basic_layout
from conan.tools.files import (
    chdir, copy, get, export_conandata_patches
)
from conan.tools.system.package_manager import Apt
import os

class LibVAConan(ConanFile):
    name = "libva"
    description = "VA-API (Video Acceleration API)"
    settings = "os", "compiler", "build_type", "arch"
    package_type = "library"
    options = {"disable_x11": [True, False], 
            "shared": [True, False],
            "wayland": [True, False],
            "static": [True, False]
    } #--disable-x11, --enable-shared
    default_options = {"disable_x11": False,
                        "shared": True,
                        "wayland": False,
                        "static": False 
    }
    def system_requirements(self):
        Apt(self).install(["pkg-config","meson","libdrm-dev","automake","libtool"])


    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        self.run("make")

    def package(self):
        self.run("make install")

    def generate(self):
        with chdir(self, self.build_folder):
            prefix = tools.unix_path(self.package_folder) if self.settings.os == 'Windows' else self.package_folder
            args = "--prefix=%s" % prefix
            args = args + (' --disable-x11' if self.options.disable_x11 else ' --enable-x11')
            args = args + (' --enable-shared' if self.options.shared else ' --disable-shared')
            args = args + (' --enable-static' if self.options.static else ' --disable-static')
            args = args + (' --enable-wayland' if self.options.wayland else ' --disable-wayland')
            self.run("./autogen.sh %s" % args)

    def package_info(self):
        if self.options.shared:
            libs = ['va']
            if self.options.disable_x11:
                libs.append['va-x11']
            if self.options.wayland:
                libs.append['va-drm']
            self.cpp_info.libs = libs
        else:
            libs = ['libva.a']
            if self.options.disable_x11:
                libs.append['libva-x11.a']
            if self.options.wayland:
                libs.append['libva-drm.a']
            self.cpp_info.libs = libs
        self.cpp_info.includedirs = ['include']
