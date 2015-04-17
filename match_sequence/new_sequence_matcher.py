



class Match(object):
    def __init__(self, span, option_choices):
        self.span = span
        self.option_choices = option_choices


class SequenceMatcher(object):
    def __init__(self, blocks):
        """
        blocks -> None

        Our goal is to match one option from each block, in order, contiguously.
        Each block is a list of options.  Each option is a list of values.
        
        The caller provides a list of items to match.  According to my
        subclass, items may be
        * TokenSequenceMatcher: values to compare directly
        * ListMembershipSequenceMatcher: lists of values to check for membership
        """
        self._blocks = blocks

        # Verify no duplicate options.
        for block in self._blocks:
            seen = set()
            for option in block:
                key = tuple(option)
                assert key not in seen
                seen.add(key)

        # Index the first item of each option per formance.
        self._value2optionxx_per_block = []
        self._canbeempty_per_block = []
        for i, block in enumerate(self._blocks):
            can_be_empty = False
            value2optionxx = {}
            for j, option in enumerate(block):
                if option:
                    value2optionxx[value].append(j)
                else:
                    can_be_empty = True
            self._canbeempty_per_block.append(can_be_empty)
            self._value2optionxx_per_block.append(value2optionxx)

    def _each_match_that_starts_at_inner(
            self, items, begin_item_index, option_choices):
        """
        (item list, index into item list, option choices) -> yields Match
        """
        # Bail if we're out of items.
        if begin_item_index == len(items):
            return

        # Get the sequence option we are supposed to match.
        cur_block_index = len(option_choices) - 1
        option_index = option_choices[cur_block_index]
        values_to_match = self._blocks[cur_block_index][option_index]

        # Check each item in the sequence.
        for i, value_to_match in enumerate(values_to_match):
            item_index = begin_item_index + i
            if item_index == len(items):
                return

            item = items[item_index]
            if not self._does_item_match(item, value_to_match):
                return

        # Ran out of sequences options to match means the match was a success.
        next_block_index = cur_block_index + 1
        if next_block_index == len(self._value2optionxx_per_block):
            a = begin_item_index
            z_excl = a
            for i, option_index in enumerate(option_choices):
                option = self._blocks[i][option_index]
                z_excl += len(option)
            yield Match(span, option_choices)

        # Else, if we're out of tokens, the match was a failure.
        begin_item_index += len(values_to_match)
        if begin_item_index == len(items):
            return

        # We have tokens and sequences to match left, so try to match the
        # beginning of the next sequence.
        item = items[begin_item_index]
        for choice in self._get_possible_options(next_block_index, item):
            new_option_choices = option_choices + [choice]
            for match in self._each_match_that_starts_at_inner(
                    items, begin_token_index, new_option_choices):
                yield match

    def _each_match_at_or_after(self, items, item_index):
        while item_index < len(items):
            item = items[item_index]
            XXX
        XXX


class TokenSequenceMatcher(SequenceMatcher):
    def _values_from_item(self, item):
        yield item

    def _does_item_match(self, item_we_have, value_to_match):
        return item_we_have == value_to_match

    def _get_possible_options(self, block_index, item_we_have):
        return self._value2topionxx_per_block[block_index].get(item_we_have, [])


class ListMembershipSequenceMatcher(SequenceMatcher):
    def _values_from_item(self, item):
        for value in item:
            yield value

    def _does_item_match(self, item_we_have, value_to_match):
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
