# coding: utf-8

from zlib import crc32
from itertools import chain

def dot(graph):
    tmpl = \
'''digraph Dependencies {{
{style}
{unknown_style}

{data}
overlap=false
label="Dependencies"
fontsize=8;
}}
'''
    style = '{v}[label="{lb}", shape=box, style=filled, color=blue];\n'
    style_buff = ''
    for i in graph.keys():
        style_buff += style.format(lb=i, v=crc32(bytes(i, encoding='utf-8')))

    unknown_style = '{v}[label="{lb}"];\n'
    unknown_style_buff = ''
    for i in set(chain(*graph.values())):
        unknown_style_buff += unknown_style.format(lb=i, v=crc32(bytes(i, encoding='utf-8')))

    s = '{source}->{destination};\n'
    buff = ''
    for k, v_list in graph.items():
        k_key = crc32(bytes(k, encoding='utf-8'))
        for v in v_list:
            dest_key = crc32(bytes(v, encoding='utf-8'))
            buff += s.format(source=k_key,
                             destination=dest_key)

    return tmpl.format(data=buff, style=style_buff,
unknown_style=unknown_style_buff)


if __name__ == '__main__':
    print(dot( {'a': ['b', 'c'], 'b': ['c', ], 'c': ['a', ]} ))
