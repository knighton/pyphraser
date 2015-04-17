from matching.sequence_matcher import SequenceMatcher


class ListSequenceMatcher(SequenceMatcher):
    """
    SequenceMatcher in which 'items' are not 'values' but instead are lists of
    values, of which one must match.
    """

    def _values_from_item(self, item):
        for value in item:
            yield value

    def _does_item_match_value(self, item_we_have, value_to_match):
        for value in item_we_have:
            if value == value_to_match:
                return True
        return False

    def _get_possible_options(self, block_index, item_we_have):
        value2optionxx = self._value2optionxx_per_block[block_index]
        rr = []
        for value in item_we_have:
            rr += value2optionxx.get(value, [])
        return rr
