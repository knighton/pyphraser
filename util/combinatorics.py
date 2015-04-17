def each_choose_one_from_each_list(aaa):
    """given a list of lists, yields all combinations of one of each."""
    if not all(aaa):
        return

    zz = map(lambda aa: len(aa) - 1, aaa)
    ii = [0] * len(aaa)
    while True:
        yield map(lambda (aa, i): aa[i], zip(aaa, ii))
        has_next = False
        for pos in range(len(ii)):
            if ii[pos] == zz[pos]:
                ii[pos] = 0
            else:
                has_next = True
                ii[pos] += 1
                break
        if not has_next:
            break
