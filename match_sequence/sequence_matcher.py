# TODO: match empty options.


class Match(object):
    def __init__(self, span, option_choices):
        # A pair: begin index, end index exclusive.
        self.span = span

        # An option index per block.
        self.option_choices = option_choices


class SequenceMatcher(object):
    """
    Given a list of items, finds sequence matches.

    This means one list from each list of options must match, in order,
    contiguously.

    For example,

        TokenSequenceMatcher subclass:

        [a]      []      [cat]     [lounged around]
        [the]    [fat]   [dog]     [dozed]
        [some] x       x [horse] x [dozed off]
        [my]                       [ate]
        [your]                     [slept]

        "I told you my lazy fat cat slept all day"
            -> []

        "I told you my fat cat slept all day and your dog ate my homework"
            -> [
                   Match((2, 7),   [3, 1, 0, 4]),
                   Match((10, 13), [4, 0, 1, 3]),
               ]
    """

    def __init__(self, blocks_to_match_against):
        """
        blocks -> None

        Our goal is to match one option from each block, in order, contiguously.
        Each block is a list of options.  Each option is a list of values.
        """
        self._blocks = blocks_to_match_against

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
            if not self._does_item_match_value(item, value_to_match):
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

    def _each_match_that_starts_at(self, items, item_index):
        """
        (items, item index) -> yields Match
        """
        first_block = 0
        item = items[item_index]
        for option_index in self._get_possible_options(self, first_block, item):
            option_choices = [option_index]
            for match in self._each_match_that_starts_at_inner(
                    items, item_index, option_choices):
                yield match

    def _each_match_list_that_starts_at(self, items, item_index):
        """
        (items, item index) -> yields list of Match
        """
        while item_index < len(items):
            for match in self._each_match_that_starts_at(items, item_index):
                resume_item_index = match.span[-1]
                for matches in self._each_match_list_that_starts_at(
                        items, resume_item_index):
                    yield [match] + matches
            item_index += 1

    def each_match_list(self, items):
        """
        items -> yields list of Match
        """
        item_index = 0
        for match_list in self._each_match_list_that_starts_at(
                items, item_index):
            yield match_list
