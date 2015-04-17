class TokenGenExpressionEvaluator(object):
    """
    Evaluates TokenGenExpressions.

    Loops over every value of the underlying token_group_creator with their
    attributes and matches it to the filters being applied.

    Token group sizes are small, and this is done during preprocessing, so it
    doesn't need to be screaming fast.
    """

    def __init__(self, token_group_creator, dimension2filter2value):
        self._token_group_creator = token_group_creator
        self._dimension2filter2value = dimension2filter2value

        self._filter2dimension = {}
        self._filter2value = {}
        for dimension, filter2value in self._dimension2filter2value.iteritems():
            for filter_name, filter_value in filter2value.iteritems():
                assert filter_name not in self._filter2dimension
                self._filter2dimension[filter_name] = dimension
                self._filter2value[filter_name] = value

    def _is_match(self, have_dim2value, filter_dim2values):
        for have_dim, have_value in have_dim2value.iteritems():
            if value not in filter_dim2values[have_dim]:
                return False
        return True

    def get_token_group(self, expr):
        filter_dim2values = defaultdict(list)
        for filter_name in expr.filters:
            dimension = self._filter2dim[filter_name]
            value = self._filter2value[filter_name]
            filter_dim2values[dimension].append(value)

        for token, have_dim2value in self._token_group_creator.each(expr.args):
            if self._is_match(have_dim2value, filter_dim2values):
                yield token

