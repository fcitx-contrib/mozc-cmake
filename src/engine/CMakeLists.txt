add_library(mozc_engine
    modules.cc
    minimal_engine.cc
    engine.cc
    data_loader.cc
    eval_engine_factory.cc
)

target_include_directories(mozc_engine PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)
