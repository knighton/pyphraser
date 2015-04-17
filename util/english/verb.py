from util.english.base import LingNumber, LingPerson, Tense
from util.misc.combinatorics import each_choose_one_from_each_list


VerbFieldType = enum('VerbFieldType: LEMMA PRES_PART PAST_PART FINITE_PRES FINITE_PAST')


class VerbInfo(object):
    """
    Info about a specific conjugation, participle, lemma, etc.
    """

    OPTIONS_PER_FIELD = [
        list(LingNumber.values),
        list(LingPerson.values),
        list(VerbFieldType.values),
    ]

    def __init__(self, number, person, verb_field_type):
        self.number = number
        self.person = person
        self.verb_field_type = verb_field_type

    def to_d(self):
        return {
            'number': self.number,
            'person': self.person,
            'verb_field_type':  self.verb_field_type,
        }


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

    def _make_index(self, person, number):
        assert LingPerson.is_valid(person)
        assert LingNumber.is_valid(number)
        p = person - LingPerson.first
        n = number - Number.first
        return n * len(LingPerson.values) + p

    def present(self, person, number):
        return self._presents[self._make_index(person, number)]

    def past(self, person, number):
        return self._pasts[self._make_index(person, number)]

    def _each_field_with_noneable_attrs(self):
        """
        (nothing) -> yields (word, number, person, verb field type).
        """
        yield self._lemma, None, None, VerbFieldType.LEMMA
        yield self._pres_part, None, None, VerbFieldType.PRES_PART
        yield self._past_part, None, None, VerbFieldType.PAST_PART

        numbers = sorted(LingNumber.values)
        persons = sorted(LingPerson.values)
        for i, s in enumerate(self._presents):
            number = numbers[i / 3]
            person = persons[i % 3]
            yield s, number, person, VerbFieldType.FINITE_PRES,

        for i, s in enumerate(self._pasts):
            number = numbers[i / 3]
            person = persons[i % 3]
            yield s, number, person, VerbFieldType.FINITE_PAST

    def each_field_with_attrs(self):
        for aa in self._each_field_with_noneable_attrs():
            word = aa[0]

            options_per_field = []
            for i, a in enumerate(aa[1:]):
                if a is None:
                    options = VerbInfo.OPTIONS_PER_FIELD[i]
                else:
                    options = [a]
                options_per_field.append(options)

            for aa_without_nones in \
                    each_choose_one_from_each_list(options_per_field):
                yield word, VerbInfo(*aa_without_nones)


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

    def _conjugate_regular(self, s):
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
