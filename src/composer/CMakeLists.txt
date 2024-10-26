add_library(mozc_composer
    table.cc
    key_event_util.cc
    internal/composition.cc
    internal/transliterators.cc
    internal/composition_input.cc
    internal/special_key.cc
    internal/char_chunk.cc
    internal/converter.cc
    internal/mode_switching_handler.cc
    composer.cc
    key_parser.cc
)

target_include_directories(mozc_composer PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)
