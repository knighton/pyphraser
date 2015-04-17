from collections import defaultdict


class SequenceMatcher(object):
    """
    Given a list of tokens, finds sequence matches.
    
    This means one list from each list of options must match, verbatim, in
    order, contiguously.

    For example,

    [a]      []      [cat]     [lounged around]
    [the]    [fat]   [dog]     [dozed]
    [some] x       x [horse] x [dozed off]
    [my]                       [ate]
    [your]                     [slept]

    "I told you my lazy fat cat slept all day"
        -> []

    "I told you my fat cat slept all day and your dog ate my homework"
        -> [
               ((2, 7),   [3, 1, 0, 4]),
               ((10, 13), [4, 0, 1, 3]),
           ]
    """

    def __init__(self, options_per_sequence=None):
        self._options_per_sequence = None
        self._seqx2token2optionxx = []
        self._seqx2canbeempty = []
        self.configure(options_per_sequence)

    def configure(self, options_per_sequence=None):
        self._options_per_sequence = options_per_sequence
        self._check_and_preprocess()

    def _check_and_preprocess(self):
        if self._options_per_sequence is None:
            return

        # Duplicates are not allowed.
        for token_lists in self._options_per_sequence:
            seen_ss = set()
            for token_list in token_lists:
                ss = tuple(token_list)
                assert ss not in seen_ss
                seen_ss.add(ss)
            
        # Build an index of the first token of each sequence for performance.
        self._seqx2token2optionxx = []
        self._seqx2canbeempty = []
        for i, token_lists in enumerate(self._options_per_sequence):
            can_be_empty = False
            token2optionxx = defaultdict(list)
            for j, token_list in enumerate(token_lists):
                if token_list:
                    first_token = token_list[0]
                    token2optionxx[first_token].append(j)
                else:
                    # There can only be one empty list, since we checkd for
                    # duplicate lists above.
                    assert not can_be_empty
                    can_be_empty
            self._seqx2token2optionxx.append(token2optionxx)
            self._seqx2canbeempty.append(can_be_empty)

    def _get_sequences_that_match_from(
            self, tokens, begin_token_index, sequence_choices):
        # Bail if we're out of tokens.
        if begin_token_index == len(tokens):
            return

        # Get the expected sequence.
        cur_sequence_index = len(sequence_choices) - 1
        choice = sequence_choices[-1]
        expected_sequence = \
            self._options_per_sequence[cur_sequence_index][choice]

        # Check each token in the sequence.
        for i in xrange(len(expected_sequence)):
            token_index = begin_token_index + i
            if token_index == len(tokens):
                return

            token = tokens[token_index]
            expected_token = expected_sequence[i]
            if token != expected_token:
                return

        # Ran out of sequences to match means the match was a success.
        next_sequence_index = cur_sequence_index + 1
        if next_sequence_index == len(self._seqx2token2optionxx):
            yield sequence_choices

        # Else, if we're out of tokens, match was a failure.
        begin_token_index += len(expected_sequence)
        if begin_token_index == len(tokens):
            return

        # Try to match the beginning of the next sequence.
        token = tokens[begin_token_index]
        for choice_index in \
                self._seqx2token2optionxx[next_sequence_index].get(token, []):
            new_sequence_choices = sequence_choices + [choice_index]
            for r in self._get_sequences_that_match_from(
                    tokens, begin_token_index, new_sequence_choices):
                yield r

    def _find_next_match(self, tokens, token_index):
        option_xx = []
        while token_index < len(tokens):
            token = tokens[token_index]
            option_xx = self._seqx2token2optionxx[0].get(token, [])
            if option_xx:
                break
            token_index += 1

        for option_index in option_xx:
            sequence_choices = [option_index]
            for sequence_choices in self._get_sequences_that_match_from(
                    tokens, token_index, sequence_choices):
                a = token_index
                sequence_len = 0
                for i, choice in enumerate(sequence_choices):
                    sequence_len += len(self._options_per_sequence[i][choice])
                z_excl = token_index + sequence_len
                yield (a, z_excl), sequence_choices

    def _find_all_matches_from(
            self, tokens, token_index, allow_overlapping, spans,
            sequence_choice_lists):
        if token_index == len(tokens):
            return

        for span, sequence_choices in \
                self._find_next_match(tokens, token_index):
            if allow_overlapping:
                resume_index = token_index + 1
            else:
                last_span = spans[-1]
                resume_index = last_span[-1]
            for span, sequence_choices in self._find_all_matches_from(
                    tokens, resume_index, allow_overlapping, spans + [span],
                    sequence_choice_lists + [sequence_choices]):
                yield span, sequence_choices

    def match(self, tokens, allow_overlapping):
        token_index = 0
        spans = []
        sequence_choice_lists = []
        for span, sequence_choices in self._find_all_matches_from(
                tokens, token_index, allow_overlapping, spans,
                sequence_choice_lists):
            yield span, sequence_choices
