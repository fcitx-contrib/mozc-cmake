add_library(mozc_prediction
    number_decoder.cc
    dictionary_prediction_aggregator.cc
    result.cc
    suggestion_filter.cc
    single_kanji_prediction_aggregator.cc
    dictionary_predictor.cc
    user_history_predictor.cc
    predictor.cc
    "${CMAKE_CURRENT_BINARY_DIR}/user_history_predictor.pb.cc"
)

target_include_directories(mozc_prediction PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)
