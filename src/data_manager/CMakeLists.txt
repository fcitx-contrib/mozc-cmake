add_library(mozc_data_manager
    data_manager.cc
    serialized_dictionary.cc
    dataset_writer.cc
    dataset_reader.cc
    oss/oss_data_manager.cc
    connection_file_reader.cc
    "${CMAKE_CURRENT_BINARY_DIR}/dataset.pb.cc"
)

target_compile_definitions(mozc_data_manager PRIVATE -DMOZC_DATASET_MAGIC_NUMBER_LENGTH=7)

target_include_directories(mozc_data_manager PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)
