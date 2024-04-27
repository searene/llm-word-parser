TARGET_DIR=/tmp/llm-word-parser
rm -rf ${TARGET_DIR}
mkdir ${TARGET_DIR}
cp -r __init__.py jp_helper ${TARGET_DIR}
pushd ${TARGET_DIR} || exit
zip -r ../llm-word-parser.ankiaddon *
rm -rf ${TARGET_DIR:?}/*
mv ../llm-word-parser.ankiaddon ${TARGET_DIR}

echo "The addon has been packaged to ${TARGET_DIR}/llm-word-parser.ankiaddon"
popd || exit
