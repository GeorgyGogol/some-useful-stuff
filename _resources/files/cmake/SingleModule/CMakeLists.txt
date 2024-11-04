cmake_minimum_required(VERSION 3.15)

project(
    ThreadPoolLibProject
    LANGUAGES CXX
    VERSION 0.1.0
)

option(THREADPOOL_BUILD_STATIC "build module as static lib" ON)
option(THREADPOOL_BUILD_SAMPLES "build sample projects" ON)
option(THREADPOOL_BUILD_UTESTS "build unit test for lib" OFF)
# THREADPOOL

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin/lib)
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)
set(THREADPOOL_EXPORT_HEADER ${CMAKE_CURRENT_SOURCE_DIR}/include/ThreadPool/defines/threadpool_export.h)

include(GenerateExportHeader)

if(${THREADPOOL_BUILD_STATIC})
    message(STATUS "ThreadPool lib configured as static lib")
    add_library(ThreadPool STATIC)
else()
    message(STATUS "ThreadPool lib configured as dynamic lib")
    add_library(ThreadPool SHARED)
endif()
add_library(libs::ThreadPool ALIAS ThreadPool)
generate_export_header(ThreadPool EXPORT_FILE_NAME ${THREADPOOL_EXPORT_HEADER})

# paths
set(
    THREADPOOL_SHARED_INCLUDE_PATH
    include
)

set( 
    THREADPOOL_INCLUDE_PATH
    src
    src/storage
    include/ThreadPool
)

# sources
set( 
    THREADPOOL_SHARED_SRC_FILES
    ${THREADPOOL_EXPORT_HEADER}
    include/ThreadPool/TaskStatus.h
	include/ThreadPool/TaskMethod.h
    include/ThreadPool/Task.h
    include/ThreadPool/ThreadPool.h
    include/ThreadPoolLib.h
)

set(
    THREADPOOL_SRC_FILES
	src/Task.cpp
	src/ThreadPool.cpp
	src/storage/TaskQueue.cpp
	src/storage/TaskQueue.h
)

# links
target_include_directories(ThreadPool PUBLIC ${THREADPOOL_SHARED_INCLUDE_PATH})
target_sources(ThreadPool PUBLIC ${THREADPOOL_SHARED_SRC_FILES})

target_include_directories(ThreadPool PRIVATE ${THREADPOOL_INCLUDE_PATH})
target_sources(ThreadPool PRIVATE ${THREADPOOL_SRC_FILES})

if (${THREADPOOL_BUILD_SAMPLES})
    message(STATUS "Start configure samples for ThreadPool Library")
    add_subdirectory(samples)
endif()

if(${THREADPOOL_BUILD_UTESTS})
    message(WARNING "Unit test for ThreadPool Library is not supported on this version")
endif()

