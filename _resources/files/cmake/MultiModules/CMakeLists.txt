cmake_minimum_required(VERSION 3.15)

project(
    ProjectName_project
    LANGUAGES CXX
    VERSION 0.0.0
)

#ProjectName

option(ProjectName_BUILD_STATIC "build modules as static objects or union build" ON)
option(ProjectName_BUILD_SAMPLES "Build samples project" ON)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin/lib)
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/lib)
set(ProjectName_EXPORT_HEADER ${CMAKE_CURRENT_SOURCE_DIR}/include/projectname_export.h)
set(ProjectName_EXPORT_PATH ${CMAKE_CURRENT_SOURCE_DIR}/include/)

include(GenerateExportHeader)

if(${ProjectName_BUILD_STATIC})
    message(STATUS "Build ProjectName_Lib as static libs")
    add_library(ProjectName_Lib INTERFACE)

    add_subdirectory(subOne)
    target_link_libraries(ProjectName_Lib INTERFACE subOne_Lib)

    # ???
    generate_export_header(
        ProjectName_Lib 
        EXPORT_FILE_NAME ${ProjectName_EXPORT_HEADER} 
        EXPORT_MACRO_NAME ProjectName_Lib_EXPORT
    )
else()
    message(STATUS "Build ProjectName_Lib as union Dll")
    add_library(ProjectName_Lib SHARED)

    add_subdirectory(RenderEngine)
    
    generate_export_header(ProjectName_Lib EXPORT_FILE_NAME ${ProjectName_EXPORT_HEADER})
	target_sources(ProjectName_Lib PUBLIC ProjectName_Lib.h)
endif()
add_library(libs::SimpleProjectName_Lib ALIAS ProjectName_Lib)

if(${ProjectName_BUILD_SAMPLES})
    add_subdirectory(Samples)
endif()

