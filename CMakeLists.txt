cmake_minimum_required(VERSION 3.10)
project(mre)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

find_package(ament_cmake_ros REQUIRED)
find_package(drake REQUIRED)

## OPTION 1
# Uncomment to use version of Pybind11 shipped with ROS 2
find_package(pybind11_vendor)
find_package(pybind11 REQUIRED)

## OPTION 2
# HACK to use Drake's pybind11 version (edit/comment to use)
# list(APPEND CMAKE_MODULE_PATH "/home/sloretz/bigssd/dbg-drake/lib/cmake/pybind11")
# include(/home/sloretz/bigssd/dbg-drake/lib/cmake/pybind11/pybind11-config.cmake)

###
# Python bindings
###
pybind11_add_module(mre SHARED
  module_mre.cpp
)
target_link_libraries(mre PRIVATE
  drake::drake
)

# Sets PYTHON_INSTALL_DIR
_ament_cmake_python_get_python_install_dir()

install(
  TARGETS mre
  DESTINATION "${PYTHON_INSTALL_DIR}"
)
### End Python bindings

ament_package()

