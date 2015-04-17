class TokenOracle(object):
    """
    Yields all possible tokens in its group with all their attributes, so the
    caller can filter them according to a token generation expression.

    Token group sizes are small, and this is done during preprocessing, so it
    doesn't need to be screaming fast.
    """

    def each_with_attrs(self, args):
        """
        yields (token, dim -> value)
        """
        raise NotImplementedError


class VerbTokenOracle(TokenOracle):
    def __init__(self, conjugator):
        self._conjugator = conjugator

    def each_with_attrs(self, args):
        lemma = args[0]
        assert len(args) == 1
        spec = self._conjugator.conjugate(lemma)
        for token, verb_info in spec.each_field():
            yield token, verb_info.to_d()


class PersonalPronounTokenOracle(TokenOracle):
    def __init__(self, personals_mgr):
        self._personals_mgr = personals_mgr

    def each_with_attrs(self, args):
        assert not args
        for token, ppi in self._personals_mgr.each_pronoun_with_attrs():
            yield token, ppi.to_d()


class PersonalPronounTokenOracle(TokenOracle):
    def __init__(self, personals_mgr):
        self._personals_mgr = personals_mgr

    def each_with_attrs(self, args):
        assert not args
        for token, pdi in self._personals_mgr.each_determiner_with_attrs():
            yield token, pdi.to_d()


