cmake_minimum_required(VERSION 3.15)

set(project ffmpeg-cuda-multi-gpu-context)

PROJECT(${project} VERSION "${CMAKE_PROJECT_VERSION}" LANGUAGES CXX)

cmake_policy(SET CMP0048 NEW)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED YES)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_compile_options(
    -Wunused
    -Wextra
    -Wpedantic
    -Wcast-align
    -Wcast-qual
    -Wconversion
    -Wctor-dtor-privacy
    -Wenum-compare
    -Wfloat-equal
    -Wnon-virtual-dtor
    -Woverloaded-virtual
    -Wredundant-decls
    -Wsign-promo
    -Wno-deprecated
    -Wno-deprecated-declarations
)

# configuration
#############################################################################################
#conan

include(conan.cmake)
conan_cmake_run(REQUIRES
        ffmpeg/5.1.3@self-muradyan/stable
        libva/2.14@self-muradyan/stable
        media-driver/22.3.1@self-muradyan/stable
        ffnvcodec/n12.0.16.0@self-muradyan/stable
        BASIC_SETUP CMAKE_TARGETS
        BUILD missing
        OPTIONS
        ffmpeg/*:fPIC=True
        ffmpeg/*:shared=False
        ffmpeg/*:postproc=False
        ffmpeg/*:zlib=False
        ffmpeg/*:bzlib=False
        ffmpeg/*:lzma=False
        ffmpeg/*:iconv=False
        ffmpeg/*:freetype=False
        ffmpeg/*:openjpeg=False
        ffmpeg/*:openh264=False
        ffmpeg/*:opus=False
        ffmpeg/*:vorbis=False
        ffmpeg/*:x264=True
        ffmpeg/*:x265=True
        ffmpeg/*:vpx=True
        ffmpeg/*:mp3lame=False
        ffmpeg/*:fdk_aac=False
        ffmpeg/*:webp=False
        ffmpeg/*:openssl=False
        ffmpeg/*:alsa=False
        ffmpeg/*:pulse=False
        ffmpeg/*:with_vaapi=True
        ffmpeg/*:with_vdpau=False
        ffmpeg/*:xcb=False
        ffmpeg/*:protocols=True
        ffmpeg/*:network=True
        ffmpeg/*:outdev_sdl=False
        ffmpeg/*:nonfree=True
        ffmpeg/*:cuda=True
        ffmpeg/*:disable_autodetect=False
        ffmpeg/*:pthreads=True
        ffmpeg/*:vpx=True
        ffmpeg/*:qsv=False
        ffmpeg/*:with_vulkan=False
        media-driver/*:enable_kernels=True
    )

set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -s")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -s")

find_package(CUDAToolkit REQUIRED)

add_subdirectory(ffmpeg-lib)
