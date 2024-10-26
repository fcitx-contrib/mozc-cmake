add_library(mozc_transliteration
    transliteration.cc
)

target_include_directories(mozc_transliteration PRIVATE
    "${PROJECT_SOURCE_DIR}"
)
