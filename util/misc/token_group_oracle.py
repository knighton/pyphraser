class TokenGroupOracle(object):
    """
    Holds knowledge about how to turn token group names into lists of tokens.
    """

    def __init__(self):
        to_be = """
            am
            are
            is
        """.split()

        first_person_subjects = """
            i
            we
        """.split()

        # No "her" because it would be shared across token groups.
        # No "it" because it would be shared acorss token groups.
        nonher_nonfirst_person_objects = """
            u
            you
            him
            it
            them
            yall
        """.split()

        # No "her" because it would be shared across token groups.
        nonher_nonfirst_possessive_pronouns = """
            your
            his
            its
            it's
            yall's
            their
        """.split()

        # No "it" because it would be shared acorss token groups.
        third_person_subject = """
            he
            she
            one
            they
        """.split()

        self._verb2list = {
            'be': to_be,
        }

        self._key2list = {
            'first person subject': first_person_subjects,
            'nonher nonfirst person object': nonher_nonfirst_person_objects,
            'nonher nonfirst possessive pronoun':
                nonher_nonfirst_possessive_pronouns,
            'third person subject': third_person_subject,
        }

        self._check()

    def _check(self):
        for key in self._verb2list:
            assert key
            assert isinstance(key, str)
        for key in self._key2list:
            assert key
            assert not key.startswith('to ')

        seen = set()
        for ss in self._verb2list.itervalues():
            for s in ss:
                assert s not in seen
                seen.add(s)
        for ss in self._key2list.itervalues():
            for s in ss:
                assert s not in seen
                seen.add(s)

    def _eval_regular_verb(self, lemma):
        ss = [lemma, lemma + 's']
        self._verb2list[lemma] = ss
        return ss

    def _eval_verb(self, lemma):
        ss = self._verb2list.get(lemma)
        if ss:
            return ss

        return self._eval_regular_verb(lemma)

    def get_token_group(self, text):
        """
        Token group name -> list of strings that comprise the group.

        Asserts if it doesn't know what to do with the name.
        """
        ss = self._key2list.get(text)
        if ss:
            return ss

        if text.startswith('to '):
            return self._eval_verb(text[3:])

        assert False  # Don't know what to do with it.
