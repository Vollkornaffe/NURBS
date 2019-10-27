cmake_minimum_required (VERSION 3.0)
project (CircularNURBS)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
find_package (Eigen3 3.3 REQUIRED NO_MODULE)
add_library (CircularNURBS SHARED cpp_src/core.cpp)
target_link_libraries (CircularNURBS Eigen3::Eigen)

set(pydest "NOT_SET" CACHE PATH "Target directory for the python modules, e.g. ~/blender-2.80/2.80/python/lib/python3.7")

set(libdest "/usr/local/lib/CircularNURBS" CACHE PATH "Target directory for the library, make sure to include this in LD_LIBRARY_PATH")

if (pydest STREQUAL "NOT_SET")
  message( SEND_ERROR "Need to specify the pydest" )
endif()

install(FILES
  ${CMAKE_SOURCE_DIR}/python_src/CircularNURBS_blender.py
  ${CMAKE_SOURCE_DIR}/python_src/CircularNURBS_interface.py
  DESTINATION ${pydest}
)
install(TARGETS CircularNURBS
  DESTINATION ${libdest})
