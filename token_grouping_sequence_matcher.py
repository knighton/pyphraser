class TokenGroupingSequenceMatcher(object):
    """
    Given a list of tokens, finds sequence matches, treating some groups of
    tokens as the same token.

    The sequences that comprise a match must be in order and contiguous.
    """

    def  __init__(self, token_group_dictionary, token_grouper, sequence_matcher,
                  options_per_sequence_as_lines=None):
        self._token_group_dictionary = token_group_dictionary
        self._token_grouper = token_grouper
        self._sequence_matcher = sequence_matcher
        self.configure(options_per_sequence_as_lines)

    def configure(self, options_per_sequence_as_lines)
        munged_options_per_sequence = \
            self._munge_options_per_sequence(options_per_sequence_as_lines)
        self.sequence_matcher.configure(munged_options_per_sequence)

    def _tokenize_pretty_line(self, line):
        raise NotImplementedError

    def _munge_pretty_line(self, line):
        rr = []
        for text, is_token_group in self._tokenize_pretty_subsequence(line):
            if is_token_group:
                group_name = text
                instances = \
                    self._token_group_dictionary.get_token_group(group_name)
                token_group_id = \
                    self.token_grouper.add_token_group(group_name, instances)
                rr.append(token_group_id)
            else:
                token = text
                rr.append(token)
        return rr

    def _munge_options_per_sequence(self, options_per_sequence_as_lines):
        rr = []
        for options in options_per_sequence_as_lines:
            munged_options = []
            for line in options:
                tokens = self._munge_pretty_line(line)
                munged_options.append(tokens)
            rr.append(munged_options)
        return rr

    def match(self, tokens, allow_overlapping):
        munged_tokens = self._token_grouper.encode(tokens)
        for spans, sequence_choice_lists in self._sequence_matcher.get_matches(
                munged_tokens, allow_overlapping):
            yield spans, sequence_choice_lists
