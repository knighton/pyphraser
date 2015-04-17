import re


class Expression(object):
    """
    Configuration for generating token groups.

    Passed from TokenGroupOracle to one of its evaluators for processing.

        '(perspro +2nd) (to be +past) right (number +int +pos) times'

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
        self._key = key
        self._args = args
        self._filters = filters

        assert self._filters == sorted(self._filters)
        self._to_s = None

    @staticmethod
    def init_from_string(text):
        ss = text.split()

        key = ss[0]

        args = []
        i = 1
        while i < len(ss):
            s = ss[i]
            if s.startswith('+'):
                break
            assert ARG_RE.match(s)
            args.append(s)

        filters = []
        while i < len(ss):
            s = ss[i]
            assert s.startswith('+')
            s = s[1:]
            assert ARG_RE.match(s)
            filters.append(s)
        filters.sort()

        return Expression(key, args, filters)

    def to_canonical_str(self):
        if self._to_s:
            return self._to_s

        ss = [self._key]
        for arg in self._args:
            ss.append(arg)
        for flag in self._filters:
            ss.append('+' + flag)
        self._to_s = ' '.join(ss)
        return self._to_s
