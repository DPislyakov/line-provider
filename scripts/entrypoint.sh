#!/bin/bash

echo "Starting service"
aerich init-db || exit 1
echo "DB inited"
aerich upgrade || exit 1
echo "DB upgraded"
python ./src/main.py
