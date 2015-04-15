class TokenGroupCreator(object):
    """
    Holds knowledge about how to turn token group names into lists of tokens.
    """

    def __init__(self):
        to_be = """
            am
            are
            is
        """.split()

        self._verb2list = {
            'be': to_be,
        }

        first_person_subjects = """
            i
            we
        """.split()

        nonfirst_person_objects = """
            u
            you
            him
            her
            it
            them
            yall
        """.split()

        nonfirst_possessive_pronouns = """
            your
            his
            her
            its
            it's
            yall's
            their
        """.split()

        self._key2list = {
            'first person subject': first_person_subjects,
            'nonfirst person object': nonfirst_person_objects,
            'nonfirst possessive pronoun': nonfirst_possessive_pronouns,
        }

        self._check()

    def _check(self):
        for key in self._verb2list:
            assert key.startswith('to ')
        for key in self._key2list:
            assert not key.startswith('to ')

        seen = set()
        for s in self._verb2list.itervalues():
            assert s not in seen
            seen.add(s)
        for s in self._key2list.itervalues():
            assert s not in seen
            seen.add(s)

    def _eval_regular_verb(self, lemma):
        ss = [lemma, lemma + 's']
        self.verb2list[lemma] = ss
        return ss

    def _eval_verb(self, lemma):
        ss = self._verb2list.get(lemma)
        if ss:
            return ss

        return self._eval_regular_verb(lemma)

    def get_token_group(self, text):
        """
        Token group name -> list of strings that comprise the group.
        """
        ss = self._key2list.get(text)
        if ss:
            return ss

        if text.startswith('to '):
            return self._eval_verb(text[3:])

        assert False  # Don't know what to do with it.


class TokenGrouper(object):
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
