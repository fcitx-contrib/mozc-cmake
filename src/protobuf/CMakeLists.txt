add_executable(protoc custom_protoc_main.cc)
target_include_directories(protoc PRIVATE "${PROJECT_SOURCE_DIR}/third_party/protobuf/src")
target_link_libraries(protoc libprotoc)
