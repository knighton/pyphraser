from copy import deepcopy

from util.token_cat.precompute.closed_class_type_evaluator import ClosedClassTypeEvaluator
from util.english.base import LingGender, LingNumber, LingPerson, LingPersonhood
from util.english.personal import PersProCase, Poss


BASE_FILTERS = {
    'case': [
        ('subj', PersProCase.SUBJ),
        ('obj',  PersProCase.OBJ),
        ('refl', PersProCase.REFL),
    ],
    'poss': [
        ('np',  Poss.NO),
        ('pos', Poss.YES),
    ],
    'number': [
        ('sing', LingNumber.SING),
        ('plur', LingNumber.PLUR),
    ],
    'person': [
        ('1st', LingPerson.FIRST),
        ('2nd', LingPerson.SECOND),
        ('3rd', LingPerson.THIRD),
    ],
    'personhood': [
        ('thing',  LingPersonhood.NO),
        ('person', LingPersonhood.YES),
    ],
    'gender': [
        ('male',   LingGender.MALE),
        ('female', LingGender.FEMALE),
        ('neuter', LingGender.NEUTER),
    ],
}


PERS_PRO_FILTERS = deepcopy(BASE_FILTERS)
del PERS_PRO_FILTERS['poss']


POS_PRO_FILTERS = deepcopy(BASE_FILTERS)
del POS_PRO_FILTERS['poss'] 


POS_DET_FILTERS = deepcopy(BASE_FILTERS)
del POS_DET_FILTERS['case']
del POS_DET_FILTERS['poss']


class PersProEvaluator(ClosedClassTypeEvaluator):
    """
    Personal pronoun expression evaluator.
    """

    def __init__(self, personals_mgr):
        self._personals_mgr = personals_mgr
        self._filters = PERS_PRO_FILTERS
        super(PersProEvaluator, self).__init__()

    def _get_filters(self):
        return self._filters

    def _each_token_with_attrs(self, args):
        assert not args
        for token, ppi in self._personals_mgr.each_pronoun_with_attrs():
            if ppi.poss == Poss.YES:
                d = ppi.to_d()
                del d['poss']
                yield token, ppi.to_d()


class PosProEvaluator(ClosedClassTypeEvaluator):
    """
    Possessive pronoun expression evaluator.
    """

    def __init__(self, personals_mgr):
        self._personals_mgr = personals_mgr
        self._filters = POS_PRO_FILTERS
        ClosedClassTypeEvaluator.__init__(self)

    def _get_filters(self):
        return self._filters

    def _each_token_with_attrs(self, args):
        assert not args
        for token, ppi in self._personals_mgr.each_pronoun_with_attrs():
            if ppi.poss == Poss.NO:
                d = ppi.to_d()
                del d['poss']
                yield token, ppi.to_d()


class PosDetEvaluator(ClosedClassTypeEvaluator):
    """
    Possessive determiner expression evaluator.
    """

    def __init__(self, personals_mgr):
        self._personals_mgr = personals_mgr
        self._filters = POS_DET_FILTERS
        super(PosDetEvaluator, self).__init__()

    def _get_filters(self):
        return self._filters

    def _each_token_with_attrs(self, args):
        assert not args
        for token, pdi in self._personals_mgr.each_determiner_with_attrs():
            yield token, pdi.to_d()
