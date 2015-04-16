from util.token_group_oracle import TokenGroupOracle
from util.token_grouper import TokenGrouper
from util.sequence_matcher import SequenceMatcher


class TokenGroupingSequenceMatcher(object):
    """
    Given a list of tokens, finds sequence matches, treating some groups of
    tokens as the same token.

    The sequences that comprise a match must be in order and contiguous.
    """

    def  __init__(self, token_group_oracle, token_grouper, sequence_matcher,
                  options_per_sequence_as_lines=None):
        self._token_group_oracle = token_group_oracle
        self._token_grouper = token_grouper
        self._sequence_matcher = sequence_matcher

        assert isinstance(self._token_group_oracle, TokenGroupOracle)
        assert isinstance(self._token_grouper, TokenGrouper)
        assert isinstance(self._sequence_matcher, SequenceMatcher)

        self.configure(options_per_sequence_as_lines)

    def configure(self, options_per_sequence_as_lines=None):
        """
        Set the phrases to match.
        """
        if options_per_sequence_as_lines is None:
            return
        munged_options_per_sequence = \
            self._munge_options_per_sequence(options_per_sequence_as_lines)
        self._sequence_matcher.configure(munged_options_per_sequence)

    def _tokenize_pretty_line(self, line):
        """
        string -> list of (text, is_expression).

        Parses human-readable config lines.

        * Expressions are delimited by ( and ).
        * ( and ) cannot occur elsewhere in the text.
        * Tokens are separated by whitespace.

        For example,

            '(to swear) (first person subject) will kill you'

        should result in:

            [
                ('to swear', True),
                ('first person subject', True),
                ('will', False),
                ('kill', False),
                ('you', False),
            ]
        """
        aa = []
        zz = []
        for i, c in enumerate(line):
            if c == '(':
                aa.append(i)
            elif c == ')':
                zz.append(i)

        assert len(aa) == len(zz)
        for a, z in zip(aa, zz):
            assert a < z

        pairs = []
        begin = 0
        for a, z in zip(aa, zz):
            end = a
            text = line[begin:end]
            for s in text.split():
                pairs.append((s, False))
            text = line[a + 1:z]
            pairs.append((text, True))
            begin = z + 1
        end = len(line)
        text = line[begin:end]
        for s in text.split():
            pairs.append((s, False))
        return pairs

    def _munge_pretty_line(self, line):
        """
        string -> munged tokens.

        For example,

            '(to swear) (first person subject) will kill you'

        could result in:

            [0, 1, 'will', 'kill', 'you']
        """
        rr = []
        for text, is_token_group in self._tokenize_pretty_line(line):
            if is_token_group:
                group_name = text
                instances = \
                    self._token_group_oracle.get_token_group(group_name)
                token_group_id = \
                    self._token_grouper.add_token_group(group_name, instances)
                rr.append(token_group_id)
            else:
                token = text
                rr.append(token)
        return rr

    def _munge_options_per_sequence(self, options_per_sequence_as_lines):
        """
        List of list of lines -> list of list of munged token lists.
        """
        rr = []
        for options in options_per_sequence_as_lines:
            munged_options = []
            for line in options:
                tokens = self._munge_pretty_line(line)
                munged_options.append(tokens)
            rr.append(munged_options)
        return rr

    def match(self, tokens, allow_overlapping):
        """
        tokens, whether overlapping -> yields (spans, sequence choice lists).

        Munge their tokens and compare them against my tokens.
        """
        munged_tokens = self._token_grouper.encode(tokens)
        for spans, sequence_choice_lists in self._sequence_matcher.get_matches(
                munged_tokens, allow_overlapping):
            yield spans, sequence_choice_lists
