cmake_minimum_required(VERSION 3.20)

set(CONDA_ENV_PATH "/home/abigale/miniconda3/envs/cudf_dev")

set(CMAKE_C_COMPILER "${CONDA_ENV_PATH}/bin/gcc")
set(CMAKE_CXX_COMPILER "${CONDA_ENV_PATH}/bin/g++")
set(CMAKE_CUDA_COMPILER "${CONDA_ENV_PATH}/bin/nvcc")

set(CMAKE_CUDA_COMPILER_FORCED TRUE)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CUDA_STANDARD 20)
set(CMAKE_CUDA_STANDARD_REQUIRED ON)

add_definitions(-DLIBCUDACXX_ENABLE_EXPERIMENTAL_MEMORY_RESOURCE)
set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -lcuda -lcudart -lcupti -lcurand -lcudadevrt --expt-extended-lambda --expt-relaxed-constexpr -rdc=true")
set(CMAKE_CUDA_SEPARABLE_COMPILATION ON)
set(CMAKE_CUDA_ARCHITECTURES 80)


project(contains_bench LANGUAGES CXX CUDA)

find_library(CUDA_CUDART_LIBRARY NAMES cudart PATHS ${CONDA_ENV_PATH}/lib REQUIRED)
find_library(CUDA_CUDADEVRT_LIBRARY NAMES cudadevrt PATHS ${CONDA_ENV_PATH}/lib REQUIRED)
find_library(CUDA_CURAND_LIBRARY NAMES curand PATHS ${CONDA_ENV_PATH}/lib REQUIRED)
set(CUDA_LIBRARIES ${CUDA_CUDART_LIBRARY} ${CUDA_CUDADEVRT_LIBRARY} ${CUDA_CURAND_LIBRARY})

set(CUDA_LIBRARIES ${CUDA_CUDART_LIBRARY} ${CUDA_CUDADEVRT_LIBRARY} ${CUDA_CURAND_LIBRARY})

list(PREPEND CMAKE_PREFIX_PATH "${CONDA_ENV_PATH}")
list(PREPEND CMAKE_LIBRARY_PATH "${CONDA_ENV_PATH}/lib")
list(PREPEND CMAKE_INCLUDE_PATH "${CONDA_ENV_PATH}/include")

set(ENV{PKG_CONFIG_PATH} "${CONDA_ENV_PATH}/lib/pkgconfig:$ENV{PKG_CONFIG_PATH}")

find_package(PkgConfig REQUIRED)
find_library(cudf_library NAMES cudf PATHS ${CONDA_ENV_PATH}/lib REQUIRED)
find_library(rmm_library NAMES rmm PATHS ${CONDA_ENV_PATH}/lib REQUIRED)
find_library(rapids_logger_library NAMES rapids_logger PATHS ${CONDA_ENV_PATH}/lib REQUIRED)

message(STATUS "Found cudf at: ${cudf_library}")

# Create executable
add_executable(contains_bench src/bench.cpp)

target_include_directories(contains_bench PRIVATE
    ${CONDA_ENV_PATH}/include
)

# Link libraries
target_link_libraries(contains_bench PRIVATE
  ${cudf_library}
  ${rmm_library}
  ${rapids_logger_library}
  ${CUDA_LIBRARIES}
)

add_executable(contains_test src/test.cpp)

target_include_directories(contains_test PRIVATE
    ${CONDA_ENV_PATH}/include
)

# Link libraries
target_link_libraries(contains_test PRIVATE
  ${cudf_library}
  ${rmm_library}
  ${rapids_logger_library}
  ${CUDA_LIBRARIES}
)

add_executable(contains_baseline src/heterogeneous_baseline.cpp)

target_include_directories(contains_baseline PRIVATE
    ${CONDA_ENV_PATH}/include
)

# Link libraries
target_link_libraries(contains_baseline PRIVATE
  ${cudf_library}
  ${rmm_library}
  ${rapids_logger_library}
  ${CUDA_LIBRARIES}
)