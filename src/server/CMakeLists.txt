add_executable(mozc_server
    mozc_server.cc
    mozc_server_main.cc
    ${GENERATED_PROTO_SRCS}
)

target_include_directories(mozc_server PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)

target_link_libraries(mozc_server
    mozc_base
    mozc_session
    mozc_ipc
    mozc_composer
    mozc_converter
    mozc_config
    mozc_storage
    mozc_engine
    mozc_usage_stats
    mozc_transliteration
    mozc_dictionary
    mozc_prediction
    mozc_rewriter
    mozc_client
    mozc_data_manager
    absl::flags_parse
    libprotoc
)
