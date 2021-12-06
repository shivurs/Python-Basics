def revert_dict(d):
    d_new = {}
    for (k,v) in d.items():
        d_new[v] = k
    return d_new