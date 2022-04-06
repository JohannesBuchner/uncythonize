#!/usr/bin/env python3
import re

def pyx_to_py(text: str, debug=False):
    """Only support validr's usage."""
    lines = []
    types = ['bint', 'str', 'int', 'float', 'dict', 'list', 'size_t', 'unsigned long']
    
    for i, line in enumerate(text.splitlines(keepends=True), 1):
        origin = line
        if line.lstrip().startswith('cdef class'):
            line = line.replace('cdef class', 'class')
        if line.lstrip().startswith('cimport'):
            line = line.replace('cimport', 'import')
            if len(lines) > 0 and line == lines[-1]:
                line = line.replace('import', '# cimport')
                line = '\n'
        for pre in ['cpdef inline', 'cdef inline', 'cpdef', 'cdef']:
            for pre_type in types + ['']:
                t = (pre + ' ' + pre_type).strip()
                if line.lstrip().startswith(t) and line.rstrip().endswith(':'):
                    line = line.replace(t, 'def')
        for pre in ['cdef', 'cpdef']:
            for t in types:
                cdef_t = '{} {} '.format(pre, t)
                if line.lstrip().startswith(cdef_t):
                    if '=' in line:
                        line = line.replace(cdef_t, '')
                    else:
                        line = re.sub(r'(\s*)(\S.*)', r'\1# \2', line)
        if re.match(r'\s*\w*def\s\w+\(.*(,|\):)', line) or re.match(r'\s+.*=.*(\):$|,$)', line):
            line = re.sub(r'(bint|str|int|float|dict|list|size_t|np\.[a-z0-9]*_t\w[\[\]:, ]|np\.[a-z0-9]*_t)\s(\w+)', r'\2', line)
        line = re.sub(r'np\.[a-z0-9]*_t[\[\]:, ]*', '', line)
        line = re.sub(r'np\.ndarray[^ ]*', '', line)
        for pre in ['cpdef inline', 'cdef inline', 'cpdef', 'cdef']:
            for pre_type in types + ['']:
                t = (pre + ' ' + pre_type).strip()
                if line.startswith(t):
                    line = line.replace(t, 'def')
                else:
                    line = line.replace(t + ' ', '')
        for t in types:
            if line.lstrip().startswith(t):
                line = line.replace(t, '')
        if origin.strip() != line.strip():
            parts = line.strip().split()
            nvars = line.count(',') + 1
            if len(parts) == nvars and not any(k in line for k in ('(', ')', '=', ':', '.', '"', "'", 'break', 'pass', 'continue', 'return')):
                # after all this stripping, only the variable name is left
                # uninitialised definitions otherwise lead to 'undefined name' errors
                line = line[:-1] + ' = ' + ', '.join(['None'] * nvars) + line[-1]
        if debug and origin != line:
            print('{:>3d}- '.format(i) + origin, end='')
            print('{:>3d}+ '.format(i) + line, end='')
        lines.append(line)
    return ''.join(lines)


def compile_pyx_to_py(filepaths, debug=False):
    """Compile *.pyx to pure python using regex and string replaces."""
    for filepath in filepaths:
        with open(filepath, encoding='utf-8') as f:
            text = f.read()
        py_filepath = filepath + '.py'
        pure_py = pyx_to_py(text, debug=debug)
        with open(py_filepath, 'w', encoding='utf-8') as f:
            f.write(pure_py)


if __name__ == "__main__":
    import sys
    compile_pyx_to_py(sys.argv[1:], debug=False)
