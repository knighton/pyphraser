from collections import defaultdict


class Token(object):
    def __init__(self, s, cat_ids):
        self.s = s              # Token string.
        self.cat_ids = cat_ids  # List of indexes into _cats.

    def to_d(self):
        return {
            's': self.s,
            'cat_ids': self.cat_ids,
        }


class Category(object):
    def __init__(self, cat_id, expr, instances):
        self.cat_id = cat_id        # Index in _cats.
        self.expr = expr            # Expression.
        self.instances = instances  # List of str.

    def to_d(self):
        return {
            'cat_id':    self.cat_id,
            'expr':      self.expr.to_canonical_string(),
            'instances': self.instances,
        }

class TokenCategorizer(object):
    """
    Categorize tokens.  Tokens can belong to multiple categories.

    We can use precomputed lookups for closed-class categories.  Open class
    categories have to be decided dynamically.
    """

    def __init__(self, key2closed_class_evaluator, key2open_class_evaluator,
                 expressions):
        # Expression canonical string -> category ID.
        self._exprstr2catid = {}

        # List of Category.
        self._categories = []

        # String -> list of Category ID.
        self._s2catids = defaultdict(list)

        # Dynamic type -> list of Expression.
        #
        # They are grouped by type because an Expression can only be of one
        # type.
        self._key2dynamic_exprs = defaultdict(list)

        # The dynamic evaluators are required for get_category_ids_for_token().
        self._key2open_class_evaluator = key2open_class_evaluator

        for expr in expressions:
            # Contine if we have seen the Expression before.
            s = expr.to_canonical_string()
            if s in self._exprstr2catid:
                continue


            # If it was recognized a closed-class type, create a new Category. 
            #
            # (Expressions can only belong to one type (ie, Expression key)).
            evaluator = key2closed_class_evaluator.get(expr.key())
            if evaluator:
                ss = sorted(evaluator.get_token_group(expr))
                cat_id = len(self._categories)
                cat = Category(cat_id, expr, ss)
                self._categories.append(cat)
                self._exprstr2catid[expr.to_canonical_string()] = cat_id
                for s in ss:
                    self._s2catids[s].append(cat_id)
                continue

            # Else, try it as an open-class type.
            evaluator = key2open.get(expr.key())
            if evaluator:
                assert evaluator.is_valid_expression(expr)
                self._key2dynamic_exprs[expr.key()].append(expr)
                continue

            # No one could recognize the Expression.
            assert False

    def dump(self):
        import json
        print 'TokenCategorizer begin'
        print '\tCategories:'
        for i, cat in enumerate(self._categories):
            print '\t\t%d %s' % (i, json.dumps(cat.to_d(), indent=4))
        print 'TokenCategorizer end'

    def get_category_ids_for_token(self, s):
        """
        str -> list of Category ID.
        """
        # First, we check our string -> category ID mapping.
        #
        # Expressions can only belong to one type, so if anything is present,
        # that is the entire result.
        cat_ids = self._s2catids.get(s)
        if cat_ids:
            return cat_ids

        # If we didn't find anything from the precomputed table, then if it
        # matches any type at all it must be dynamic.
        for key, dynamic_exprs in self._key2dynamic_exprs.iteritems():
            cat_ids = []
            evaluator = self._key2open_class_evaluator[key]
            for expr in dynamic_expr:
                if evaluator.is_match(expr, s):
                    cat_id = self._exprstr2catid[expr.to_canonical_string()]
                    cat_ids.append(expr)
            if cat_ids:
                return cat_ids

        # Neither in precomputed nor dynamic.
        return []

    def get_category_id_of_expr(self, expr):
        """
        Expression -> Category ID.
        """
        s = expr.to_canonical_string()
        return self._exprstr2catid[s]
