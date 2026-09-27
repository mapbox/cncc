import os
import runpy
import sys
import tempfile
import textwrap

import clang.cindex


def libclang():
    candidates = [
        os.environ.get('CNCC_LIBCLANG'),
        '/Library/Developer/CommandLineTools/usr/lib/libclang.dylib',
        '/usr/lib/llvm-14/lib/libclang.so',
        '/usr/lib/libclang.so',
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return path
    raise SystemExit('set CNCC_LIBCLANG to libclang')


clang.cindex.Config.set_library_file(libclang())

BAD = textwrap.dedent('''\
    namespace myNamespace {
    class myClass { int myMember; };
    }
    int main() { return 0; }
''')
GOOD = textwrap.dedent('''\
    namespace a {
    class MyClass { int member_; };
    }
    int main() { return 0; }
''')
STYLE = textwrap.dedent('''\
    class_decl: '^([A-Z][a-z0-9]+)+$'
    field_decl: '^[a-z]+_$'
    namespace: '^[a-z]$'
''')


def run(script, style, files):
    sys.argv = ['cncc', '--style', style] + files
    try:
        runpy.run_path(script, run_name='__main__')
    except SystemExit as exc:
        return exc.code
    return None


def main():
    script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cncc')
    tmp = tempfile.mkdtemp()
    bad = os.path.join(tmp, 'bad.cc')
    good = os.path.join(tmp, 'good.cc')
    style = os.path.join(tmp, 'style')
    with open(bad, 'w') as f:
        f.write(BAD)
    with open(good, 'w') as f:
        f.write(GOOD)
    with open(style, 'w') as f:
        f.write(STYLE)

    # A later clean file used to hide violations in an earlier file.
    code = run(script, style, [bad, good])
    if code != 1:
        raise SystemExit('bad then good exited %s, expected 1' % code)
    if run(script, style, [good]) != 0:
        raise SystemExit('a clean file should exit 0')
    if run(script, style, [bad]) != 1:
        raise SystemExit('a violating file should exit 1')
    print('ok')


if __name__ == '__main__':
    main()
