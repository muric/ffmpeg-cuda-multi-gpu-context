set(project ffmpeg_lib)

set(${PROJECT_NAME}_SOURCES
    decode.cpp)

#include cuda to enable cuda context in hw_contex_cuda
include_directories(${CUDAToolkit_INCLUDE_DIRS})

add_library(
    ${PROJECT_NAME} SHARED
    ${${PROJECT_NAME}_HEADERS}
)

target_link_libraries(
    INTERFACE CUDA::cuda_driver
    PUBLIC CONAN_PKG::ffmpeg
    PUBLIC CONAN_PKG::spdlog
)
