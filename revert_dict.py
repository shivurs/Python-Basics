def revert_dict(d):
    d2 = {}
    keys = d.keys()
    vals = d.values()
    for i in vals:
        d2[i] = ''
        for j in keys:
            d2[i] = j
    return d2
