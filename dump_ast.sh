#!/usr/bin/env bash

clang++-3.6 -Xclang -ast-dump -fsyntax-only test.cc |tail -n 37
