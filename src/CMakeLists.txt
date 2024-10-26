cmake_minimum_required(VERSION 3.27)

project(fcitx5-mozc)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Fcitx5Core 5.1.11 REQUIRED)
find_package(Fcitx5Module REQUIRED COMPONENTS Clipboard)

set(LIBS)
if(APPLE)
    find_library(COCOA_LIB Cocoa REQUIRED)
    find_library(IOKIT_LIB IOKit REQUIRED)
    list(APPEND LIBS
        ${COCOA_LIB}
        ${IOKIT_LIB}
    )
endif()

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(third_party/abseil-cpp)

set(protobuf_INSTALL OFF)
set(protobuf_BUILD_TESTS OFF)
set(protobuf_BUILD_PROTOC_BINARIES OFF)
set(protobuf_BUILD_LIBPROTOC ON)
add_subdirectory(third_party/protobuf)

add_subdirectory(protobuf)
set(PROTOC_EXECUTABLE "${PROJECT_BINARY_DIR}/protobuf/protoc")

add_custom_target(gen) # Dummy target to force data generation before binary build
set(PROTO_SRCS
    data_manager/dataset
    ipc/ipc
    prediction/user_history_predictor
    protocol/candidate_window
    protocol/commands
    protocol/config
    protocol/engine_builder
    protocol/renderer_command
    protocol/renderer_style
    protocol/segmenter_data
    protocol/state
    protocol/user_dictionary_storage
    usage_stats/usage_stats
)


list(TRANSFORM PROTO_SRCS APPEND ".pb.cc" OUTPUT_VARIABLE GENERATED_PROTO_SRCS)
list(TRANSFORM GENERATED_PROTO_SRCS PREPEND "${PROJECT_BINARY_DIR}/")

foreach(PROTO_SRC ${PROTO_SRCS})
    get_filename_component(PROTO_NAME ${PROTO_SRC} NAME)
    set(target_name "gen_${PROTO_NAME}_proto")
    set(proto_cc "${PROJECT_BINARY_DIR}/${PROTO_SRC}.pb.cc")
    set(proto_h "${PROJECT_BINARY_DIR}/${PROTO_SRC}.pb.h")

    add_custom_command(
        OUTPUT "${proto_cc}" "${proto_h}"
        COMMAND ${PROTOC_EXECUTABLE} --cpp_out=${PROJECT_BINARY_DIR} "${PROTO_SRC}.proto"
        DEPENDS "${PROTO_SRC}.proto"
        WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
        COMMENT "Generating ${PROTO_SRC}.pb.cc and ${PROTO_SRC}.pb.h"
    )
    add_custom_target(${target_name} DEPENDS "${proto_cc}" "${proto_h}")
    add_dependencies(${target_name} protoc)
    add_dependencies(gen ${target_name})
endforeach()

# add_subdirectory(protocol)

# Mozc requires char to be unsigned, as it's used as array index.
add_compile_options(-funsigned-char)

# Build libmozc.so
add_subdirectory(base)
add_subdirectory(client)
add_subdirectory(ipc)
add_subdirectory(usage_stats)
add_subdirectory(dictionary)
add_subdirectory(prediction)
add_subdirectory(session)
add_subdirectory(composer)
add_subdirectory(config)

add_subdirectory(converter)
add_subdirectory(storage)
add_subdirectory(engine)
add_subdirectory(transliteration)
add_subdirectory(rewriter)
add_subdirectory(data_manager)

# Force data generation before binary build
add_dependencies(gen
    gen_character_set
    gen_config_file_stream_data
    gen_pos_matcher_code
    gen_pos_matcher_impl_inc
    gen_stats_list
    gen_version_def
)

add_dependencies(mozc_base gen)
add_dependencies(mozc_client gen)
add_dependencies(mozc_ipc gen)
add_dependencies(mozc_usage_stats gen)
add_dependencies(mozc_dictionary gen)
add_dependencies(mozc_prediction gen)
add_dependencies(mozc_session gen)
add_dependencies(mozc_composer gen)
add_dependencies(mozc_config gen)
add_dependencies(mozc_converter gen)
add_dependencies(mozc_storage gen)
add_dependencies(mozc_engine gen)
add_dependencies(mozc_transliteration gen)
add_dependencies(mozc_rewriter gen)
add_dependencies(mozc_data_manager gen)

# message(FATAL_ERROR "${GENERATED_PROTO_SRCS}")
add_subdirectory(unix/fcitx5)
add_subdirectory(server)
