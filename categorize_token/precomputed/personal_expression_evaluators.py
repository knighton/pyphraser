from copy import deepcopy

from categorize_token.internal.type_expression_evaluator import TypeExpressionEvaluator


PERS_PRO_FILTERS = {
    'case': [
        ('subj', PersProCase.SUBJ),
        ('obj',  PersProCase.OBJ),
        ('refl', PersProCase.REFL),
    ],
    'poss': [
        ('notpos', Poss.NO),
        ('pos',    Poss.YES),
    ],
    'number': [
        ('sing', Number.SING),
        ('plur', Number.PLUR),
    ],
    'person': [
        ('1st', Person.FIRST),
        ('2nd', Person.SECOND),
        ('3rd', Person.THIRD),
    ],
    'personhood': [
        ('thing',  Personhood.NO),
        ('person', Personhood.YES),
    ],
    'gender': [
        ('male', Gender.MALE),
        ('female', Gender.FEMALE),
        ('neuter', Gender.NEUTER),
    ],
}


POS_DET_FILTERS = deepcopy(PERS_PRO_FILTERS)
del POS_DET_FILTERS['case']
del POS_DET_FILTERS['poss']


class PersonalPronounExpressionEvaluator(TypeExpressionEvaluator):
    def __init__(self, personals_mgr):
        self._personals_mgr = personals_mgr
        self._filters = PERS_PRO_FILTERS
        super(PersonalPronounExpressionEvaluator, self).__init__()

    def get_filters(self):
        return self._filters

    def each_with_attrs(self, args):
        assert not args
        for token, ppi in self._personals_mgr.each_pronoun_with_attrs():
            yield token, ppi.to_d()


class PossessiveDeterminerExpressionEvaluator(TypeExpressionEvaluator):
    def __init__(self, personals_mgr):
        self._personals_mgr = personals_mgr
        self._filters = POS_DET_FILTERS
        super(PossessiveDeterminerExpressionEvaluator, self).__init__()

    def get_filters(self):
        return self._filters

    def each_with_attrs(self, args):
        assert not args
        for token, pdi in self._personals_mgr.each_determiner_with_attrs():
            yield token, pdi.to_d()

