class TokenEncoder(object):
    """
    Convert a token to a list of integers for consumption by a
    ListSequenceMatcher.
    
    These capture both (a) its category IDs if any, and (b) a unique token ID.
    """

    def __init__(self, token_categorizer):
        self._token_categorizer = token_categorizer
        self._ss = []
        self._s2index = {}

    def token_id_from_index(self, index):
        """
        index -> token ID

        Returns the number as negative to avoid conflict with category IDs.
        """
        return -index - 1

    def _get_or_create_token_id(self, s):
        """
        s -> int
        """
        index = self._s2index.get(s)
        if index is not None:
            return self._token_id_from_index(index)

        index = len(self._ss)
        self._ss.append(s)
        self._s2index[s] = index
        return self._token_id_from_index(index)

    def to_ints(self, s):
        """
        Token string -> list of int

        For example,

            '7' -> [
                (the token ID for '7'),
                (category ID for expression 'number'),
                (category ID for second matching expression),
                ...
            ]
        """
        rr = []
        rr.append(self._get_or_create_token_id(s))
        for cat_id in self._token_categorizer.get_category_ids(s):
            rr.append(cat_id)
        return rr

    def from_token_id(self, token_id):
        index = self.index_from_token_id(token_id)
        return self._ss[index]
