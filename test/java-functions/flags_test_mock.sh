#!/bin/sh
. `dirname $0`/common.sh mock

assert "$1" "-XX:OnOutOfMemoryError=kill -9 %p"; shift
assert "$1" "-Xmx2048m"; shift
assert "$1" "-classpath"; shift
assert "$1" "jars"; shift
assert "$1" "-Dfoo.bar=baz"; shift
assert "$1" "arg1 arg2 \"' \$(echo eval-me)"; shift
assert "$1" "com.example.Main"; shift
assert "$1" "some command"; shift
assert "$1" "help"; shift
echo "PASS"
