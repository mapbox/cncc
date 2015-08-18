#!/usr/bin/env bash

clang++ -Xclang -ast-dump -fsyntax-only test.cc |tail -n 37
