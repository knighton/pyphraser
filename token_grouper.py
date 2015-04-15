class TokenGrouper(object):
    """
    Munges tokens according to what token group they are in.

    Tokens -> encode() -> munged tokens -> decode() -> pretty tokens.
    """

    def __init__(self):
        self._token_groups = []
        self._token2x = {}

        self._names = []
        self._name2x = {}

    def add_token_group(self, display_name, instances):
        """
        Add a new token group to the list of tokens I will convert.

        * Display name is a lowercase string with spaces.
        * Instances is a list of tokens.
        """
        assert display_name not in self._name2x
        for token in instances:
            assert token not in self._token2x
            assert isinstance(token, basestring)

        x = len(self._token_groups)

        self._token_groups.append(instances)
        for token in instances:
            self._token2x[token] = x

        self._names.append(display_name)
        self._name2x[display_name] = x

    def encode(self, tokens):
        """
        List of tokens -> list of munged tokens.

        A munged token is either (a) the original token string if not part of a
        token group, or (b) the index if it is.
        """
        rr = []
        for token in tokens:
            assert isinstance(token, basestring)
            x = self._token2x.get(token)
            if x is None:
                rr.append(token)
            else:
                rr.append(x)
        return rr

    def decode(self, munged_tokens):
        """
        List of munged tokens -> list of pretty tokens.

        A pretty token is either (a) the original token if string, or (b) the
        display name associated with the index if it's an index.
        """
        rr = []
        for a in munged_tokens:
            if isinstance(a, basestring):
                rr.append(a)
            elif isinstance(a, int):
                rr.append(self._names[x])
            else:
                assert False
        return rr
