from dicts import cube_state, EDGES

def find_white_edges():
    white_edges = []
    for (f1, i1), (f2, i2) in EDGES:
        c1 = cube_state[f1][i1]
        c2 = cube_state[f2][i2]
        if c1 == 'w' or c2 == 'w':
            white_edges.append({
                'pos1': (f1, i1, c1),
                'pos2': (f2, i2, c2)
            })
    return white_edges