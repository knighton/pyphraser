from categorize_token.closed_class.closed_class_type_evaluator import ClosedClassTypeEvaluator


FILTERS = {
    'number': [
        ('sing', Number.SING),
        ('plur', Number.PLUR),
    ],
    'person': [
        ('1st', Person.FIRST),
        ('2nd', Person.SECOND),
        ('3rd', Person.THIRD),
    ],
    'tense': [
        ('pres', Tense.PRES),
        ('past', Tense.PAST),
    ],
    'usage': [
        ('lemma',    VerbUsage.LEMMA),
        ('prespart', VerbUsage.PRES_PART),
        ('pastpart', VerbUsage.PAST_PART),
        ('finite',   VerbUsage.FINITE),
    ],
}


class VerbEvaluator(ClosedClassTypeEvaluator):
    def __init__(self, conjugator, filters):
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
