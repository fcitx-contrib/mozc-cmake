for lang in csharp java objectivec php python ruby rust; do
  sed -i.bak "/compiler\/$lang/d" third_party/protobuf/src/file_lists.cmake
done

rm -f third_party/protobuf/src/file_lists.cmake.bak
