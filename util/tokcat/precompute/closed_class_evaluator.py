from util.tokcat.precompute.personal_evaluator import PersProEvaluator, PosDetEvaluator
from util.tokcat.precompute.verb_evaluator import VerbEvaluator


class ClosedClassEvaluator(object):
    """
    Turns magic config language into groups of tokens.
    """

    def __init__(self, conjugator, personals_mgr):
        self._key2handler = {
            'perspro': PersonalPronounEvaluator(conjugator),
            'posdet':  PossessiveDeterminerEvaluator(personals_mgr),
            'to':      VerbExpressionEvaluator(personals_mgr),
        }

    def get_token_group(self, expr):
        """
        Expression -> None or list of strings
        """
        handler = self._key2handler.get(expr.key())
        if not handler:
            return None

        return handler.get_token_group(expr)
