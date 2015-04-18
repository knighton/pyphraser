def lines_from_table(
        aaa, column_names=None, indent='', space_between_columns=' '):
    """
    list of list of stringable -> list of lines
    """
    if column_names is not None:
        dashes = []
        for column_name in column_names:
            s = str(column_name)
            dashes.append('-' * len(s))
        aaa = [column_names, dashes] + aaa
    
    if not aaa:
        return []

    sss = []
    max_lens = map(len, aaa[0])
    for aa in aaa:
        ss = []
        for i, a in enumerate(aa):
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
