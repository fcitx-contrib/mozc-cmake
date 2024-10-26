add_library(mozc_session
    internal/session_output.cc
    internal/key_event_transformer.cc
    internal/candidate_list.cc
    internal/keymap.cc
    internal/ime_context.cc
    key_info_util.cc
    session_usage_stats_util.cc
    session_converter.cc
    session_handler_tool.cc
    session_handler.cc
    session_watch_dog.cc
    session.cc
    session_usage_observer.cc
    session_observer_handler.cc
    session_server.cc
)

target_include_directories(mozc_session PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)
