import random
import numpy as np

QUERY_INST = ['PATH_COUNT', 'DISTINCT_NODE_COUNT']
GRAPH_INST = ['CONTAINS_EDGE', 'IS_NODE_CONNECTED', 'SHORTEST_PATH_LENGTH']
PATH_INST = ['PATH_ADD', 'PATH_REMOVE', 'PATH_GET_ID', 'CONTAINS_PATH']
PATH_ID_INST = ['PATH_REMOVE_BY_ID', 'PATH_GET_BY_ID',
                'PATH_SIZE', 'PATH_DISTINCT_NODE_COUNT', 'CONTAINS_PATH_ID']
SPECIAL_INST = ['PATH_CONTAINS_NODE', 'COMPARE_PATHS']

ALL_INST = []
ALL_INST.extend(QUERY_INST)
ALL_INST.extend(GRAPH_INST)
ALL_INST.extend(PATH_INST)
ALL_INST.extend(PATH_ID_INST)
ALL_INST.extend(SPECIAL_INST)

linear_instr = ['PATH_GET_ID', 'CONTAINS_PATH',
                'PATH_GET_BY_ID', 'COMPARE_PATHS']
graph_change = ['PATH_ADD', 'PATH_REMOVE', 'PATH_REMOVE_BY_ID']

linear_instr_cnt = 0
graph_change_cnt = 0


nodes = np.random.uniform(-2147483648, 2147483647, 500)
nodes = np.unique(nodes)
nodes = np.int32(nodes[:250]).tolist()

paths = []


def fill_instr(instr):
    if instr in QUERY_INST:
        pass
    elif instr in GRAPH_INST:
        x = random.choice(nodes)
        y = random.choice(nodes)
        instr+=' %d %d' % (x, y)
        pass
    elif instr in PATH_INST:
        p = []
        for i in range(200):
            x = random.choice(nodes)
            instr += ' %d' % x
            p.append(x)
        paths.append(p)
    elif instr in PATH_ID_INST:
        instr += ' %d' % (random.randint(1, max(len(paths), 20)))
    else:
        if instr == 'PATH_CONTAINS_NODE':
            x = random.randint(1, max(len(paths), 20))
            y = random.choice(nodes)
            instr += ' %d %d' % (x, y)
        elif instr == 'COMPARE_PATHS':
            x = random.randint(1, max(len(paths), 20))
            y = random.randint(1, max(len(paths), 20))
            instr += ' %d %d' % (x, y)
    return instr


for i in range(1000):
    instr = random.choice(ALL_INST)
    if instr in graph_change:
        graph_change_cnt = graph_change_cnt+1
    if graph_change_cnt >= 20:
        while (instr in linear_instr) or (instr in graph_change):
            instr = random.choice(ALL_INST)
    if instr in linear_instr:
        linear_instr_cnt = linear_instr_cnt+1
    if linear_instr_cnt >= 20:
        while (instr in linear_instr) or (instr in graph_change):
            instr = random.choice(ALL_INST)
    assert (instr in ALL_INST)
    print(fill_instr(instr))
