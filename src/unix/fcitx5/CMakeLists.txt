add_library(mozc MODULE
    fcitx_key_translator.cc
    fcitx_key_event_handler.cc
    surrounding_text_util.cc
    mozc_connection.cc
    mozc_response_parser.cc
    mozc_engine.cc
    mozc_engine_factory.cc
    mozc_state.cc
    mozc_client_pool.cc
    ${GENERATED_PROTO_SRCS}
)

target_include_directories(mozc PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_BINARY_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "/Library/Input Methods/Fcitx5.app/Contents/include/Fcitx5/Module"
)

target_link_libraries(mozc
    Fcitx5::Core
    libprotoc
    mozc_base
    mozc_client
    mozc_ipc
    mozc_session
    mozc_composer
    mozc_config
    absl::flags_parse
)
