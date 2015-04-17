from english.personal import PersonalsManager
from english.verb import Conjugator



class ExpressionEvaluator(object):
    """
    Turns magic config language into groups of tokens.
    """

    def __init__(self, conjugator, personals_mgr):
        self._key2handler = {
            'perspro': PersonalPronounEvaluator(conjugator),
            'posdet':  PossessiveDeterminerEvaluator(personals_mgr),
            'to':      VerbExpressionEvaluator(personals_mgr),
        }

    def init_default():
        conjugator = Conjugator.init_default()
        personals_mgr = PersonalsManager.init_default()
        return ExpressionEvaluator(conjugator, personals_mgr)

    def get_token_group(self, text):
        """
        Token group name -> list of strings that comprise the group.

        Asserts if it doesn't know what to do with the name.
        """
        expr = Expression.init_from_string(text)
        return self._key2handler[expr.key].get_token_group(expr)
