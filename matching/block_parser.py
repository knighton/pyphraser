class BlockParser(object):
    """
    Parses human-readable SequenceMatcher config lines.

    For example, a line like:

        '(perspro +1st +subj) (to swear +pres) (perspro +1st +subj) will kill you'

    will result in:
    
        [Expression, Expression, Expression, will, kill, you]
    """

    def _tokenize_pretty_line_normal_piece(self, line):
        return line.split()

    def _parse_pretty_line(self, line):
        """
        str -> list of token or Expression

        * Expressions are delimited by ( and ).
        * ( and ) cannot occur elsewhere in the text.
        * Tokens are separated by whitespace.
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

        rr = []
        begin = 0
        for a, z in zip(aa, zz):
            end = a
            text = line[begin:end]
            for s in self._tokenize_pretty_line_normal_piece(text):
                rr.append(s)
            text = line[a + 1:z]
            rr.append(Expression.init_from_str(text))
            begin = z + 1
        end = len(line)
        text = line[begin:end]
        for s in self._tokenize_pretty_line_normal_piece(text):
            rr.append(s)
        return rr

    def parse_blocks(self, blocks_as_lines):
        """
        blocks (as lines) -> blocks (as token lists)

        See SequenceMatcher.__init__ for what blocks are.
        """
        blocks_as_tokens = []
        for block in blocks_as_lines:
            new_block = []
            for line in block:
                tokens = self._parse_pretty_line(line)
                new_block.append(tokens)
            blocks_as_tokens.append(new_block)
        return blocks_as_tokens
