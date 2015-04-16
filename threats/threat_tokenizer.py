class ThreatTokenizer(object):
    """
    Tokenization for the narrow goal of matching threat phrases.
    """

    def __init__(self):
        self.expand = {
            "'s": 'is',
            "'d": 'would',
        }

    def tokenize(self, text):
        """
        Text -> tokens.
        """
        ss = text.lower().split()
        rr = []
        for s in ss:
            last_two = s[-2:]
            split_out = self.expand.get(last_two)
            if split_out is None:
                rr.append(s[:-2])
                rr.append(split_out)
            else:
                rr.append(s)
        return rr
