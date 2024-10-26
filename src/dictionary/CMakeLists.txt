# Generate pos_matcher_impl.inc
set(pos_matcher_impl_inc "${CMAKE_CURRENT_BINARY_DIR}/pos_matcher_impl.inc")

add_custom_command(
    OUTPUT "${pos_matcher_impl_inc}"
    COMMAND ./gen_pos_matcher_code.sh "${pos_matcher_impl_inc}"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    COMMENT "Generating pos_matcher_impl.inc"
)

add_custom_target(gen_pos_matcher_impl_inc DEPENDS "${pos_matcher_impl_inc}")

# Generate pos_map.inc
set(pos_map_inc "${CMAKE_CURRENT_BINARY_DIR}/pos_map.inc")

add_custom_command(
    OUTPUT "${pos_map_inc}"
    COMMAND ./gen_pos_map.sh "${pos_map_inc}"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    COMMENT "Generating pos_map.inc"
)

add_custom_target(gen_pos_matcher_code DEPENDS "${pos_map_inc}")

add_library(mozc_dictionary
    single_kanji_dictionary.cc
    user_dictionary_storage.cc
    file/codec.cc
    file/codec_factory.cc
    file/codec_util.cc
    file/dictionary_file_builder.cc
    file/dictionary_file.cc
    user_pos.cc
    text_dictionary_loader.cc
    suppression_dictionary.cc
    user_dictionary.cc
    user_dictionary_session_handler.cc
    system/codec.cc
    system/system_dictionary.cc
    system/system_dictionary_builder.cc
    system/system_dictionary_benchmark.cc
    system/value_dictionary.cc
    dictionary_impl.cc
    user_dictionary_importer.cc
    user_dictionary_session.cc
    user_dictionary_util.cc
    suffix_dictionary.cc
)

target_include_directories(mozc_dictionary PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)
