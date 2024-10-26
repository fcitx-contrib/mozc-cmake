add_library(mozc_storage
    encrypted_string_storage.cc
    lru_storage.cc
    registry.cc
    louds/louds_trie.cc
    louds/bit_vector_based_array_builder.cc
    louds/louds_trie_builder.cc
    louds/simple_succinct_bit_vector_index.cc
    louds/bit_vector_based_array.cc
    louds/louds.cc
    louds/bit_stream.cc
    tiny_storage.cc
    existence_filter.cc
)

target_include_directories(mozc_storage PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
)
