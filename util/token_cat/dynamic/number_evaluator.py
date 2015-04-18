from collections import defaultdict
import re

from util.enum import enum
from util.tokcat.dynamic.open_class_type_evaluator import OpenClassTypeEvaluator


NumberType = enum('NumberType: INT FLOAT')


NumberPolarity = enum('NumberPolarity: NEG NONNEG')


FILTERS = {
    'number_type': [
        ('int',   NumberType.INT),
        ('float', NumberType.FLOAT),
    ],
    'number_polarity': [
        ('neg', NumberPolarity.NEG),
        ('pos', NumberPolarity.NONNEG),
    ],
}


class NumberEvaluator(OpenClassTypeEvaluator):
    def __init__(self):
        self._float_re = re.compile('[0-9]+(\\.[0-9]+)')

        self._filter2dimension = {}
        self._filter2value = {}
        for dimension, filters in FILTERS.iteritems():
            for filter_name, filter_value in filters:
                assert filter_name not in self._filter2dimension
                self._filter2dimension[filter_name] = dimension
                self._filter2value[filter_name] = filter_value

    def _get_number_type(self, s):
        if '.' in s:
            return NumberType.FLOAT

        return NumberType.INT

    def _get_number_polarity(self, s):
        if float(s) < 0:
            return NumberPolarity.NEG
        
        return NumberPolarity.NONNEG

    def _dim2value_from_str(self, s):
        if not self._float_re.match(s):
            return None

        number_type = self._get_number_type(s)
        number_polarity = self._get_number_polarity(s)

        return {
            'number_type': number_type,
            'number_polarity': number_polarity,
        }

    def is_match(self, expr, s):
        # Get dimension -> actual value.
        dim2valuewehave = self._dim2value_from_str(s)
        if dim2valuewehave is None:
            return False

        # Get dimension -> possible values.
        #
        # All expressions are already checked for validity in the setup stage.
        dim2possiblevalues = defaultdict(list)
        for filter_name in expr.filters():
            dim = self._filter2dimension[filter_name]
            value = self._filter2value[filter_name]
            dim2possiblevalues[dim].append(value)

        for dim, value_we_have in dim2value_we_have.iteritems():
            if value_we_have not in dim2possiblevalues[dim]:
                return False

        return True

    def is_valid_expression(self, expr):
        if expr.args:
            return False

        for filter_name in expr.filters():
            if filter_name not in self._filter2dimension:
                return False

        return True
