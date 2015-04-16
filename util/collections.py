from collections import defaultdict


def v2k_from_k2v(k2v, strict=True):
    v2k = {}
    for k, v in k2v.iteritems():
        if not strict:
            v2k[v] = k
            continue
        if v in v2k:
            existing_k = v2k[v]
            assert existing_k == k
        v2k[v] = k
    return v2k


def v2kk_from_k2v(k2v):
    d = defaultdict(list) 
    for k, v in k2v.iteritems():
        d[v].append(k)
    return d
