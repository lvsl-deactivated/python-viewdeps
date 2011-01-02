# coding utf-8
from tokenize import tokenize
from token import tok_name, NAME
import ast
from io import BytesIO
import os
import sys
import fnmatch

def parse_file(fname):
    with open(fname, encoding='utf-8') as f:
        mod_name = fname.split(os.path.sep)[-1].split('.')[0]
        try:
            code = f.read()
        except UnicodeDecodeError as e:
            print('{0} unable read file: {1}'.format(fname, e))
            return mod_name, []
        try:
            tree = ast.parse(code, filename=fname)
        except Exception as e:
            print('Unable to parse {0} error: {1}'.format(fname, e), file=sys.stderr)
            return mod_name, []
    result = set()
    for ast_obj in ast.walk(tree):
        if type(ast_obj) is ast.Import:
            for o in ast_obj.names:
                result.add(o.name.split('.')[0])
        elif type(ast_obj) is ast.ImportFrom:
            # XXX: cant't handle relaive imports
            if not ast_obj.module: continue
            result.add(ast_obj.module.split('.')[0])
    # XXX: get file name without extension
    return mod_name, sorted(list(result))

def parse_files(*fnames):
    result = []
    for fname in fnames:
        result.append(parse_file(fname))
    return dict(result)

def traverse_dir(path):
    result = []
    to_exclude = []
    for dirname, dirnames, filenames in os.walk(path):
        for subdir in dirnames:
            if '.' in subdir:
                to_exclude.append(subdir)
        if dirname in to_exclude:
            print('{0} ecluded'.format(dirname),
                file=sys.stderr)
            continue
        result.extend( [os.path.join(dirname, fn) for fn in filenames
                        if not fn.startswith('.') and fn.endswith('.py')] )
    return result

def parse(*paths):
    result = []
    valid_paths = []
    for p in paths:
        if not p:
            print('Empty path', file=sys.stderr)
            continue
        if not os.path.exists(p):
            print('{0} does not exists.'.format(p), file=sys.stderr)
            continue
        abs_path = os.path.abspath(p)
        if os.path.isdir(abs_path):
            files = traverse_dir(abs_path)
            valid_paths.extend(files)
        else:
            valid_paths.append(abs_path)
    return parse_files(*valid_paths)


if __name__ == '__main__':
    for k,v_list in parse(*sys.argv[1:]).items():
        print('{0}:'.format(k))
        for v in v_list:
            print('\t{0}'.format(v))
