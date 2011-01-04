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
                result.add(o.name)
        elif type(ast_obj) is ast.ImportFrom:
            # XXX: cant't handle relaive imports
            if not ast_obj.module: continue
            result.add(ast_obj.module)
            for n in ast_obj.names:
                result.add('{0}.{1}'.format(ast_obj.module, n.name))
    # XXX: get file name without extension
    return mod_name, sorted(list(result))

def parse_files(*paths):
    result = {}
    for top_dir, fnames in paths:
        for fname in fnames:
            raw_mod_name, raw_import_names = parse_file(fname)
            dn = os.path.dirname(fname)
            part = dn.rsplit(top_dir)[-1]
            if part.startswith(os.path.sep):
                part = part[1:]
            part = part.replace(os.path.sep, '.')
            full_modname = '{0}.{1}'.format(part, raw_mod_name)
            if full_modname in result:
                result[full_modname].extend(
                    raw_import_names)
            else:
                result[full_modname] = raw_import_names

    # add dirname prefixes
    for mod_name, imports in result.items():
        new_imports = []
        for i in imports:
            if '{0}.__init__'.format(i) in result:
                new_imports.append('{0}.__init__'.format(i))
            if mod_name.startswith(i):
                continue
            elif any(map(lambda x: i in x, result.keys())):
                for k in result.keys():
                    if i in k:
                        new_imports.append(k)
                        break
            else:
                new_imports.append(i)
        result[mod_name] = new_imports

    # filter non modules
    for mod_name, imports in result.items():
        new_imports = []
        for i in imports:
            if '{0}.__init__'.format(i) in result:
                new_imports.append('{0}.__init__'.format(i))
            elif not any(map(lambda x: i.startswith(x) and len(i) > len(x), result.keys())):
                new_imports.append(i)
        result[mod_name] = new_imports


    return result

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
    valid_paths = {}
    for p in paths:
        if not p:
            print('Empty path', file=sys.stderr)
            continue
        if not os.path.exists(p):
            print('{0} does not exists.'.format(p), file=sys.stderr)
            continue
        abs_path = os.path.abspath(p)
        top_dir = os.path.basename(os.path.dirname(abs_path))

        if os.path.isdir(abs_path):
            files = traverse_dir(abs_path)
            valid_paths[top_dir] = files
        else:
            valid_paths[top_dir] = abs_path
    return parse_files(*list(valid_paths.items()))


if __name__ == '__main__':
    for k,v_list in parse(*sys.argv[1:]).items():
        print('{0}:'.format(k))
        for v in v_list:
            print('\t{0}'.format(v))
