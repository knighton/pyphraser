from collections import defaultdict
import re

from util.collections import v2k_from_k2vv
from english.personal import PersonalsManager
from english.verb import Conjugator


class TokenGenerationExpressionEvaluator(object):
    def get_token_group(self):
        raise NotImplementedError


class NumberEvaluator(TokenGenerationExpressionEvaluator):
    def get_token_group(self, expr):
        assert not expr.args
        assert not expr.filters
        return None


class VerbEvaluator(TokenGenerationExpressionEvaluator):
    def __init__(self):
        self._conjugator = Conjugator.init_default()

        self._dimension2filters = {
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

        self._filter2dimension = {}
        self._filter2value = {}
        for dimension, filters_values in self._dimension2filters.iteritems():
            for filter_name, filter_value in filters_values:
                assert filter_name not in self._filter2dimension
                self._filter2dimension[filter_name] = dimension
                self._filter2value[filter_name] = filter_value

    def get_token_group(self, expr):
        assert len(expr.args) == 1
        lemma = expr.args[0]

        dimension2filters = defaultdict(list)
        for filter_name in expr.filters:
            dim = self._filter2dimension[filter_name]
            filter_value = self._filter2value[filter_name]
            dimension2filters[dim].append(filter_value)

        spec = self._conjugator.conjugate(lemma)

        tokens = []
        for token, verb_info in spec.each_field():
            if verb_info.matches_filters(dimension2filters):
                tokens.append(token)

        return tokens


class TokenGenerationExpression(object):
    """
    Configuration for generating token groups.

    Passed from TokenGroupOracle to one of its handlers for processing.

    Expressions are
    * a keyword, that is the first token (verb, personal pronoun, etc.)
    * a list of "arguments" (following words without +).  Open class.  Used for
      verb lemma.
    * a list of "filters" (following words prefixed with +).  Closed class.
      Filters filter what matches the expression.  Each filter belongs to a
      dimension.  Multiple filters for a dimension mean any of them must match.
      To match, a result must match the filter(s) for each dimension present.
    """

    ARG_RE = re.compile('^[a-z0-9]+$')

    def __init__(self, key, args, filters):
        self.key = key
        self.args = args
        self.filters = filters

    @staticmethod
    def init_from_string(text):
        ss = text.split()
        key = ss[0]
        args = []
        filters = []
        for s in ss[1:]:
            if s.startswith('+'):
                s = s[1:]
                assert ARG_RE.match(s)
                filters.append(s)
            else:
                assert ARG_RE.match(s)
                args.append(s)
        return TokenGenerationExpression(key, args, filters)


class TokenGroupOracle(object):
    """
    Turns magic config language into groups of tokens.
    """

    def __init__(self):
        self._key2handler = {
            'number': NumberEvaluator(),
            'perspro': PersonalPronounEvaluator(),
            'posdet': PossessiveDeterminerEvaluator(),
            'to': VerbEvaluator(),
        }

    def get_token_group(self, text):
        """
        Token group name -> list of strings that comprise the group.

        Asserts if it doesn't know what to do with the name.
        """
        ss = text.split()
        expr = TokenGenerationExpression.init_from_string(ss)
        return self._key2handler[expr.key].get_token_group(expr)
