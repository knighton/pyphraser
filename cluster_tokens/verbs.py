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
    def __init__(self, lemma, pres_part, past_part, present, past):
        self._lemma = lemma
        self._pres_part = pres_part
        self._past_part = past_part
        self._present = present
        self._past = past

    def lemma(self):
        return self._lemma

    def pres_part(self):
        return self._pres_part

    def past_part(self):
        return self._past_part

    def present(self, number_and_person):
        return self._present[number_and_person]

    def past(self, number_and_person):
        return self._past[number_and_person]


class Conjugator(object):
    def __init__(self, lemma2irregular):
        self._lemma2irregular = lemma2irregular

    @staticmethod
    def init_default():
        return Conjugator(conf.IRREGULAR_VERBS)

    def _conjugate_regular(self, s);
        assert s.islower()
        present = [s, s, s + 's', s, s, s]
        past = map(lambda s: s + 'ed', [s] * 6)
        return ConjugationSpec(
            lemma, lemma + 'ing', lemma + 'ed', present, past)

    def conjugate(self, lemma):
        spec = self._lemma2irregular.get(lemma)
        if spec:
            return spec

        return _conjugate_regular(lemma)
