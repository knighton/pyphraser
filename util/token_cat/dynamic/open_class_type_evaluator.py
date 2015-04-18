class OpenClassTypeEvaluator(object):
    """
    Evaluator for a type that cannot be precomputed (eg, 'integers').
    """

    def is_match(self, expr, s):
        """
        (Expression, string) -> whether match
        """

    def is_valid_expression(self, expr):
        """
        Expression -> whether valid
        """
        raise NotImplementedError
