import re


class Expression(object):
    """
    Configuration for generating token groups.

    Passed from TokenGroupOracle to one of its evaluators for processing.

    Expressions are
    * a keyword, that is the first token (verb, personal pronoun, etc.)
    * a list of "arguments" (following words without +).  Open class.  Used for
      verb lemma.
    * a list of "filters" (following words prefixed with +).  Closed class.
      Filters filter what matches the expression.  Each filter belongs to a
      dimension.  Multiple filters for a dimension mean any of them must match.
      To match, a result must match the filter(s) for each dimension present.
    """

    ARG_RE = re.compile('^[a-z0-9]+$')

    def __init__(self, key, args, filters):
        self.key = key
        self.args = args
        self.filters = filters

    @staticmethod
    def init_from_string(text):
        ss = text.split()
        key = ss[0]
        args = []
        filters = []
        for s in ss[1:]:
            if s.startswith('+'):
                s = s[1:]
                assert ARG_RE.match(s)
                filters.append(s)
            else:
                assert ARG_RE.match(s)
                args.append(s)
        return Expression(key, args, filters)
