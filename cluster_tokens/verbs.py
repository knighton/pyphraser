NumberAndPerson = enum(
    'NumberAndPerson: SING_1ST SING_2ND SING_3RD PLUR_1ST PLUR_2ND PLUR_3RD',
    start=0)


class ConjugationSpec(object):
    """
    All the ways a verb can conjugate.

    Conjugations:
    * Lemma
    * Present participle
    * Past participle
    * Present: 2 persons x 3 numbers
    * Past: 2 persons x 3 numbers

    For example,

        (be, being, been, [am are is are are are],
        [was were was were were were])
    """

    def __init__(self, lemma, pres_part, past_part, presents, pasts):
        self._lemma = lemma
        self._pres_part = pres_part
        self._past_part = past_part
        self._presents = presents
        self._pasts = pasts

    def lemma(self):
        return self._lemma

    def pres_part(self):
        return self._pres_part

    def past_part(self):
        return self._past_part

    def present(self, number_and_person):
        return self._presents[number_and_person]

    def past(self, number_and_person):
        return self._pasts[number_and_person]


class StringTransform(object):
    """
    Transformations to do on a string.
    """

    def __init__(self, append):
        self.append = append

    def transform(self, s):
        return s + self.append


class ConjugationSpecDerivation(object):
    """
    The information needed to derive a conjugation spec from a lemma.
    """

    def __init__(self, pres_part, past_part, presents, pasts):
        self._pres_part = pres_part
        self._past_part = past_part
        self._presents = presents
        self._pasts = pasts

    def derive(self, lemma):
        pres_part = self._pres_part.transform(lemma)
        past_part = self._past_part.transform(lemma)
        presents = map(lambda t: t.transform(lemma), self._presents)
        pasts = map(lambda t: t.transform(lemma), self._pasts)
        return ConjugationSpec(lemma, pres_part, past_part, presents, pasts)


class Conjugator(object):
    """
    Conjugates verbs.
    """

    def __init__(self, lemma2irregular, regular_derivation):
        self._lemma2irregular = lemma2irregular
        self._cache_lemma2regular = {}

        self._regular_derivation = regular_derivation

    @staticmethod
    def init_default():
        irregular_verbs = {
            'be': ConjugationSpec(
                'be', 'being', 'been', 'am are is are are are'.split(),
                'was were was were were were'.split()),
        }

        t = lambda s: StringTransform(s)
        regular_derivation = ConjugationSpecDerivation(
            t('ing'), t('ed'), map(t, ['', '', 's', '', '', '']),
            map(t, ['ed'] * 6))

        return Conjugator(irregular_verbs, regular_derivation)

    def _conjugate_regular(self, s);
        return self._regular_derivation.derive(s)

    def conjugate(self, lemma):
        """
        Lemma -> ConjugationSpec.
        """
        r = self._lemma2irregular.get(lemma)
        if r:
            return r

        r = self._cache_lemma2regular.get(lemma)
        if r:
            return r

        assert lemma.islower()
        return self._conjugate_regular(lemma)
