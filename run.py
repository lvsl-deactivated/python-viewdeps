#!/usr/bin/env python3

if __name__ == "__main__":
    from subprocess import call
    from datetime import datetime
    import argparse
    import sys
    import os

    import dot
    import parse

    argparser = argparse.ArgumentParser(
        description="Python-viewdeps run script.")
    argparser.add_argument('packages', metavar='module',
        type=str, nargs="+",
        help='list of packages or modules to analyze.')
    argparser.add_argument('--exclude-external', dest='exclude_externals',
        action='store_const', const=True, default=False,
        help='Exclude external modules')
    args = argparser.parse_args()
    try:
        retcode = call('which fdp > /dev/null 2>&1', shell=True)
        if retcode != 0:
            sys.exit('Unable to locate `fdp`')
    except OSError as e:
        sys.exit('Execution failed: {0}'.format(e))

    if not os.path.isdir('_data'):
        os.mkdir('_data')

    data = parse.parse(*args.packages)
    if args.exclude_externals:
        for k, v_list in data.items():
            new_v_list = []
            for v in v_list:
                if v in data.keys():
                    new_v_list.append(v)
            data[k] = new_v_list
    dot_str = dot.dot(data)
    f_name = datetime.now().strftime('%Y-%m-%d_%H%S')

    with open('_data/{0}.dot'.format(f_name), 'w', encoding='utf-8') as dot_file:
        dot_file.write(dot_str)

    cmd = 'fdp -Tsvg _data/{fn}.dot > _data/{fn}.svg'
    try:
        retcode = call(cmd.format(fn=f_name), shell=True)
        if retcode != 0:
            sys.exit('fdp fails')
    except OSError as e:
        sys.exit('Execution failed: {0}'.format(e))


