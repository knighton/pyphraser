from util.english.base import LingNumber, LingPerson
from util.english.verb import VerbFieldType
from util.token_cat.precompute.closed_class_type_evaluator import ClosedClassTypeEvaluator


FILTERS = {
    'number': [
        ('sing', LingNumber.SING),
        ('plur', LingNumber.PLUR),
    ],
    'person': [
        ('1st', LingPerson.FIRST),
        ('2nd', LingPerson.SECOND),
        ('3rd', LingPerson.THIRD),
    ],
    'verb_field_type': [
        ('lemma',    VerbFieldType.LEMMA),
        ('prespart', VerbFieldType.PRES_PART),
        ('pastpart', VerbFieldType.PAST_PART),
        ('pres',     VerbFieldType.FINITE_PRES),
        ('past',     VerbFieldType.FINITE_PAST),
    ],
}


class VerbEvaluator(ClosedClassTypeEvaluator):
    def __init__(self, conjugator):
        self._conjugator = conjugator
        self._filters = FILTERS
        super(VerbExpressionEvaluator, self).__init__()

    def _get_filters(self):
        return self._filters

    def _each_token_with_attrs(self, args):
        lemma = args[0]
        assert len(args) == 1
        spec = self._conjugator.conjugate(lemma)
        for token, verb_info in spec.each_field():
            yield token, verb_info.to_d()
