cmake_minimum_required(VERSION 3.20)

set(CONDA_ENV_PATH "/home/akkim7/micromamba/envs/cudf_dev")

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
add_executable(contains_het src/het_bench.cpp)

target_include_directories(contains_het PRIVATE
    ${CONDA_ENV_PATH}/include/rapids        # source-built CCCL, matches libcudf.so ABI
    ${CONDA_ENV_PATH}/include               # everything else
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include/cccl
)

# Link libraries
target_link_libraries(contains_het PRIVATE
  ${cudf_library}
  ${rmm_library}
  ${rapids_logger_library}
  ${CUDA_LIBRARIES}
)

# Create executable
add_executable(contains_cudf src/libcudf_bench.cpp)

target_include_directories(contains_cudf PRIVATE
    ${CONDA_ENV_PATH}/include/rapids        # source-built CCCL, matches libcudf.so ABI
    ${CONDA_ENV_PATH}/include               # everything else
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include/cccl
)

# Link libraries
target_link_libraries(contains_cudf PRIVATE
  ${cudf_library}
  ${rmm_library}
  ${rapids_logger_library}
  ${CUDA_LIBRARIES}
)

# Create executable
add_executable(contains_badhet src/badhet_bench.cpp)

target_include_directories(contains_badhet PRIVATE
    ${CONDA_ENV_PATH}/include/rapids        # source-built CCCL, matches libcudf.so ABI
    ${CONDA_ENV_PATH}/include               # everything else
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include/cccl
)

# Link libraries
target_link_libraries(contains_badhet PRIVATE
  ${cudf_library}
  ${rmm_library}
  ${rapids_logger_library}
  ${CUDA_LIBRARIES}
)

# Create executable
add_executable(contains_warp src/warp_bench.cpp)

target_include_directories(contains_warp PRIVATE
    ${CONDA_ENV_PATH}/include/rapids        # source-built CCCL, matches libcudf.so ABI
    ${CONDA_ENV_PATH}/include               # everything else
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include/cccl
)

# Link libraries
target_link_libraries(contains_warp PRIVATE
  ${cudf_library}
  ${rmm_library}
  ${rapids_logger_library}
  ${CUDA_LIBRARIES}
)

# Create executable
add_executable(contains_thread src/thread_bench.cpp)

target_include_directories(contains_thread PRIVATE
    ${CONDA_ENV_PATH}/include/rapids        # source-built CCCL, matches libcudf.so ABI
    ${CONDA_ENV_PATH}/include               # everything else
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include/cccl
)

# Link libraries
target_link_libraries(contains_thread PRIVATE
  ${cudf_library}
  ${rmm_library}
  ${rapids_logger_library}
  ${CUDA_LIBRARIES}
)

# Create executable
add_executable(contains_ncu src/ncu_bench.cpp)

target_include_directories(contains_ncu PRIVATE
    ${CONDA_ENV_PATH}/include/rapids        # source-built CCCL, matches libcudf.so ABI
    ${CONDA_ENV_PATH}/include               # everything else
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include
    ${CONDA_ENV_PATH}/targets/x86_64-linux/include/cccl
)

# Link libraries
target_link_libraries(contains_ncu PRIVATE
  ${cudf_library}
  ${rmm_library}
  ${rapids_logger_library}
  ${CUDA_LIBRARIES}
)

add_executable(contains_test src/test.cpp)

target_include_directories(contains_test PRIVATE
  ${CONDA_ENV_PATH}/include/rapids        # source-built CCCL, matches libcudf.so ABI
  ${CONDA_ENV_PATH}/include               # everything else
  ${CONDA_ENV_PATH}/targets/x86_64-linux/include
  ${CONDA_ENV_PATH}/targets/x86_64-linux/include/cccl
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
  ${CONDA_ENV_PATH}/include/rapids        # source-built CCCL, matches libcudf.so ABI
  ${CONDA_ENV_PATH}/include               # everything else
  ${CONDA_ENV_PATH}/targets/x86_64-linux/include
  ${CONDA_ENV_PATH}/targets/x86_64-linux/include/cccl
)

# Link libraries
target_link_libraries(contains_baseline PRIVATE
  ${cudf_library}
  ${rmm_library}
  ${rapids_logger_library}
  ${CUDA_LIBRARIES}
)

# Find Python and its development headers
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Get pandas include directory (for potential future use)
execute_process(
    COMMAND ${Python3_EXECUTABLE} -c "import pandas; print(pandas.__path__[0])"
    OUTPUT_VARIABLE PANDAS_PATH
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

# Create pandas benchmark executable
add_executable(pandas_bench src/pandas_bench.cpp)

target_include_directories(pandas_bench PRIVATE
    ${Python3_INCLUDE_DIRS}
)

# Link Python libraries
target_link_libraries(pandas_bench PRIVATE
    ${Python3_LIBRARIES}
)

# Set RPATH so it can find Python libraries at runtime
set_target_properties(pandas_bench PROPERTIES
    BUILD_RPATH_USE_ORIGIN TRUE
    INSTALL_RPATH "${Python3_LIBRARY_DIRS}"
)

# Find DataFrame library (if installed system-wide)
find_package(DataFrame REQUIRED)

add_executable(dataframe_bench src/dataframe_bench.cpp)

target_link_libraries(dataframe_bench PRIVATE
    DataFrame::DataFrame
)

set_target_properties(dataframe_bench PROPERTIES
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
)