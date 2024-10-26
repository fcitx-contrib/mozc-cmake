# Generate usage_stats_list.inc
set(usage_stats_list_inc "${CMAKE_CURRENT_BINARY_DIR}/usage_stats_list.inc")

add_custom_command(
    OUTPUT "${usage_stats_list_inc}"
    COMMAND python "${CMAKE_CURRENT_SOURCE_DIR}/gen_stats_list.py" --output "${usage_stats_list_inc}" "${PROJECT_SOURCE_DIR}/data/usage_stats/stats.def"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    COMMENT "Generating usage_stats_list.inc"
)

add_custom_target(gen_stats_list DEPENDS "${usage_stats_list_inc}")

add_library(mozc_usage_stats
    usage_stats.cc
    usage_stats_uploader.cc
    "${CMAKE_CURRENT_BINARY_DIR}/usage_stats.pb.cc"
)

target_include_directories(mozc_usage_stats PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_SOURCE_DIR}/third_party/protobuf/src"
    "${PROJECT_BINARY_DIR}"
)
