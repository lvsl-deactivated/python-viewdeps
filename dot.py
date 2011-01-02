# coding: utf-8

def dot(graph):
    tmpl = \
'''digraph Dependencies {{

{data}
overlap=false
label="Dependencies"
fontsize=8;
}}
'''
    s = '{source}->{destination};\n'
    buff = ''
    for k, v_list in graph.items():
        for v in v_list:
            buff += s.format(source=k, destination=v)
    return tmpl.format(data=buff)


if __name__ == '__main__':
    print(dot( {'a': ['b', 'c'], 'b': ['c', ], 'c': ['a', ]} ))
