from matching.sequence_matcher import Match, SequenceMatcher


class ValueSequenceMatcher(SequenceMatcher):
    """
    SequenceMatcher in which 'items' are the same thing as 'values'.
    """

    def _values_from_item(self, item):
        yield item

    def _does_item_match_value(self, item_we_have, value_to_match):
        return item_we_have == value_to_match

    def _get_possible_options(self, block_index, item_we_have):
        return self._value2topionxx_per_block[block_index].get(item_we_have, [])
