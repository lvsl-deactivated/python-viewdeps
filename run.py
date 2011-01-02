#!/usr/bin/env python3


if __name__ == "__main__":
    from subprocess import call
    from datetime import datetime
    import sys
    import os

    import dot
    import parse

    if len(sys.argv) < 2:
        sys.exit('Usage: {0} dirs or files'.format(sys.argv[0]))


    try:
        retcode = call('which neato > /dev/null 2>&1', shell=True)
        if retcode != 0:
            sys.exit('Unable to locate `neato`')
    except OSError as e:
        sys.exit('Execution failed: {0}'.format(e))

    if not os.path.isdir('_data'):
        os.mkdir('_data')

    data = parse.parse(*sys.argv[1:])
    dot_str = dot.dot(data)

    f_name = datetime.now().strftime('%Y-%m-%d_%H%S')

    with open('_data/{0}.dot'.format(f_name), 'w', encoding='utf-8') as dot_file:
        dot_file.write(dot_str)

    cmd = 'neato -Tpng _data/{fn}.dot > _data/{fn}.png'
    try:
        retcode = call(cmd.format(fn=f_name), shell=True)
        if retcode != 0:
            sys.exit('neato fails')
    except OSError as e:
        sys.exit('Execution failed: {0}'.format(e))


