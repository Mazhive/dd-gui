cmake_minimum_required(VERSION 3.16)
project(DdCloner)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets)

add_executable(dd_gui main.cpp)
target_link_libraries(dd_gui Qt6::Widgets)
