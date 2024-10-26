add_library(mozc_converter
    quality_regression_util.cc
    key_corrector.cc
    connector.cc
    segmenter.cc
    pos_id_printer.cc
    lattice.cc
    immutable_converter_interface.cc
    gen_segmenter_bitarray.cc
    node_list_builder.cc
    segments.cc
    converter.cc
    immutable_converter.cc
    nbest_generator.cc
    candidate_filter.cc
)

target_include_directories(mozc_converter PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)
