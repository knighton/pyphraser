class TokenGroupManager(object):
    def __init__(self):
        self._irregular_verbs = {
            'be': ['am', 'are', 'is'],
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

    def _eval_regular_verb(self, lemma):
        return [lemma, lemma + 's']

    def _eval_verb(self, lemma):
        ss = self._irregular_verbs.get(lemma)
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

        assert False  # Invalid token group name.
