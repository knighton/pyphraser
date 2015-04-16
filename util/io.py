def lines_from_table(rows, headers=None, indent='', space_between_columns=' '):
    if headers is not None:
        rows = [headers] + rows
    
    if not rows:
        return ''

    sss = []
    max_lens = map(len, rows[0])
    for row in rows:
        ss = []
        for i, a in enumerate(row):
            s = str(a)
            max_lens[i] = max(max_lens[i], len(s))
            ss.append(s)
        sss.append(ss)

    lines = []
    for ss in sss:
        line = []
        line.append(indent)
        for i, s in enumerate(ss):
           line.append(s)
           if i + 1 < len(ss):
               line.append(' ' * (max_lens[i] - len(s)))
               line.append(space_between_columns)
        line = ''.join(line)
        lines.append(line)

    return lines


def print_func(a):
    print '%s' % a
