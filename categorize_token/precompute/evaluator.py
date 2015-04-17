from categorize_token.precompute.personal_evaluator import PersProEvaluator, PosDetEvaluator
from categorize_token.precompute.verb_evaluator import VerbEvaluator


class Evaluator(object):
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
        Expression -> list of strings
        """
        return self._key2handler[expr.key].get_token_group(expr)
