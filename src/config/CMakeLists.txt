add_library(mozc_config
    config_handler.cc
    stats_config_util.cc
    character_form_manager.cc
)

target_include_directories(mozc_config PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)
