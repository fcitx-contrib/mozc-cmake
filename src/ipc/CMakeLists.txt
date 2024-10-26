add_library(mozc_ipc
    ipc_mock.cc
    named_event.cc
    process_watch_dog.cc
    ipc.cc
    unix_ipc.cc
    ipc_path_manager.cc
    "${CMAKE_CURRENT_BINARY_DIR}/ipc.pb.cc"
)

target_include_directories(mozc_ipc PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)
