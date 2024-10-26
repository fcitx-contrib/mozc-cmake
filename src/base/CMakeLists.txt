# Generate character_set.inc
set(character_set_inc "${CMAKE_CURRENT_BINARY_DIR}/character_set.inc")

add_custom_command(
    OUTPUT "${character_set_inc}"
    COMMAND python "${CMAKE_CURRENT_SOURCE_DIR}/gen_character_set.py" --jisx0201file JIS0201.TXT --jisx0208file JIS0208.TXT --output "${character_set_inc}"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/data/unicode"
    COMMENT "Generating character_set.inc"
)

add_custom_target(gen_character_set DEPENDS "${character_set_inc}")

# Generate config_file_stream_data.inc
set(config_file_stream_data_inc "${CMAKE_CURRENT_BINARY_DIR}/config_file_stream_data.inc")

set(keymap_files
    atok.tsv
    chromeos.tsv
    kotoeri.tsv
    mobile.tsv
    ms-ime.tsv
    overlay_henkan_muhenkan_to_ime_on_off.tsv
)

list(TRANSFORM keymap_files PREPEND "keymap/")

set(composition_table
    12keys-halfwidthascii.tsv
    12keys-hiragana.tsv
    12keys-hiragana_intuitive.tsv
    50keys-hiragana.tsv
    flick-halfwidthascii.tsv
    flick-halfwidthascii_ios.tsv
    flick-hiragana.tsv
    flick-hiragana_intuitive.tsv
    flick-number.tsv
    godan-hiragana.tsv
    hiragana-romanji.tsv
    kana.tsv
    notouch-hiragana.tsv
    qwerty_mobile-halfwidthascii.tsv
    qwerty_mobile-hiragana.tsv
    romanji-hiragana.tsv
    toggle_flick-halfwidthascii.tsv
    toggle_flick-halfwidthascii_ios.tsv
    toggle_flick-hiragana.tsv
    toggle_flick-hiragana_intuitive.tsv
    toggle_flick-number.tsv
)

list(TRANSFORM composition_table PREPEND "preedit/")

add_custom_command(
    OUTPUT "${config_file_stream_data_inc}"
    COMMAND python "${CMAKE_CURRENT_SOURCE_DIR}/gen_config_file_stream_data.py" --output "${config_file_stream_data_inc}" ${composition_table} ${keymap_files}
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/data"
    COMMENT "Generating config_file_stream_data.inc"
)

add_custom_target(gen_config_file_stream_data DEPENDS "${config_file_stream_data_inc}")

# Generate version_def.h
set(version_def_h "${CMAKE_CURRENT_BINARY_DIR}/version_def.h")

add_custom_command(
    OUTPUT "${version_def_h}"
    COMMAND ./gen_version_def.sh "${CMAKE_CURRENT_BINARY_DIR}/mozc_version.txt" "${version_def_h}"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    COMMENT "Generating version_def.h"
)

add_custom_target(gen_version_def DEPENDS "${version_def_h}")

# Build mozc_base
add_library(mozc_base
    mmap.cc
    strings/internal/double_array.cc
    strings/internal/utf8_internal.cc
    strings/internal/japanese_rules.cc
    strings/unicode.cc
    strings/japanese.cc
    system_util.cc
    environ.cc
    file/recursive.cc
    file/temp_dir.cc
    encryptor.cc
    update_util.cc
    log_file.cc
    init_mozc.cc
    url.cc
    hash.cc
    password_manager.cc
    stopwatch.cc
    singleton.cc
    file_stream.cc
    unverified_sha1.cc
    process.cc
    number_util.cc
    process_mutex.cc
    text_normalizer.cc
    clock.cc
    unverified_aes256.cc
    config_file_stream.cc
    container/serialized_string_array.cc
    clock_mock.cc
    run_level.cc
    multifile.cc
    util.cc
    codegen_bytearray_stream.cc
    random.cc
    vlog.cc
    file_util.cc
    cpu_stats.cc
    crash_report_handler.cc
    version.cc
    mac/mac_process.mm
    mac/mac_util.mm
)

target_include_directories(mozc_base PRIVATE
    "${PROJECT_SOURCE_DIR}"
    "${PROJECT_SOURCE_DIR}/third_party/abseil-cpp"
    "${PROJECT_BINARY_DIR}"
)

target_link_libraries(mozc_base ${LIBS})
