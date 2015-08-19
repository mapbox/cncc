# Customizable Naming Convention Checker

CNCC is a customizable naming conventions checker for C++.
In using the Clang frontend CNCC works directly on the language's abstract syntax tree (AST).
This is quite similar to what `clang-format` does but way more simple and for naming conventions only.

In short, CNCC supports user-defined pattern validation based on AST nodes: you can specify patterns for variables, class names, namespace names, and so on.

## Example

You provide a style file containing regular expressions for validating AST nodes, such as:
camel-case for class names, members should have an underscore appended, and so on.

```
class_decl: '^([A-Z][a-z]+)+$'
field_decl: '^[a-z]+_$'
var_decl: '^[a-z][a-z0-9]*$'
namespace: '^[a-z]?$'
```

CNCC then checks the AST's nodes against the provided rules, issuing warnings to `stderr` and returning with a appropriate status code for easy integration:

    test.cc:4:11: "myNamespace" does not conform to pattern "^[a-z]?$" associated with namespace
    test.cc:6:7: "myClass" does not conform to pattern "^([A-Z][a-z]+)+$" associated with class_decl
    test.cc:11:9: "myMember" does not conform to pattern "^[a-z]+_$" associated with field_decl
    test.cc:19:24: "myMember" does not conform to pattern "^[a-z]+_$" associated with field_decl

For all available nodes see the [official libclang documentation](http://clang.llvm.org/doxygen/group__CINDEX.html#gaaccc432245b4cd9f2d470913f9ef0013) or the [Python wrapper documentation](https://github.com/llvm-mirror/clang/blob/aca4fe314a55cacae29e1548cb7bfd2119c6df4c/bindings/python/clang/cindex.py#L599) and look for `CursorKind`.

## Requirements

* python2
* python-clang
* python-yaml

## Usage

For standalone files, with default compiler invocation:

    cncc --style=examples/small.style examples/test.cc

CNCC defaults to reading a `.cncc.style` file in your home directory if no style file was given.

    cncc examples/test.cc

Sometimes compilation gets more involved.
Use CMake or Bear in order to create a `compile_command.json` compilation database.
In it compiler invocation flags and arguments are stored for each file involved in the build process.
This does not require you to build your program.

    mkdir build
    cd build
    ccmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_EXPORT_COMPILE_COMMANDS=1
    cncc --style=~/.cncc.style --dbdir . ../main.cc

## License

Copyright © 2015 Daniel J. Hofmann

Distributed under the MIT License (MIT).
