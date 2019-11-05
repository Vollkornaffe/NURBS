cmake_minimum_required (VERSION 3.0)
project (CyclicNURBS)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
find_package (Eigen3 3.3 REQUIRED NO_MODULE)
add_library (CyclicNURBS SHARED cpp_src/core.cpp)
target_link_libraries (CyclicNURBS Eigen3::Eigen)

# this is a really ugly solution, but it should work
# the problem is that the binary code isn't reloaded after a change
# the workaround is to name the liraries different each time
if (NOT DEFINED CACHE{RELOAD_COUNTER})
  set(RELOAD_COUNTER "0" CACHE INTERNAL "")
else()
  math(EXPR RELOAD_COUNTER "${RELOAD_COUNTER} + 1")
  set(RELOAD_COUNTER ${RELOAD_COUNTER} CACHE INTERNAL "")
endif()
message("Reload counter at ${RELOAD_COUNTER}")
set_target_properties(CyclicNURBS PROPERTIES SUFFIX ".so.${RELOAD_COUNTER}")

configure_file(python_src/CyclicNURBS.py.in CyclicNURBS.py @ONLY)
configure_file(python_src/CyclicNURBS_path.py.in CyclicNURBS_path.py @ONLY)

install(FILES
  ${CMAKE_SOURCE_DIR}/python_src/CyclicNURBS_blender.py
  ${CMAKE_SOURCE_DIR}/python_src/CyclicNURBS_interface.py
  ${CMAKE_SOURCE_DIR}/python_src/CyclicNURBS_data.py
  ${CMAKE_BINARY_DIR}/CyclicNURBS_path.py
  ${CMAKE_BINARY_DIR}/CyclicNURBS.py
  DESTINATION ${CMAKE_INSTALL_PREFIX}/CyclicNURBS
)
install(TARGETS CyclicNURBS
  DESTINATION ${CMAKE_INSTALL_PREFIX}/CyclicNURBS)
