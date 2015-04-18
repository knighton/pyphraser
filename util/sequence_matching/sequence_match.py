class SequenceMatch(object):
    def __init__(self, span, option_choices):
        # A pair: begin index, end index exclusive.
        self.span = span

        # An option index per block.
        self.option_choices = option_choices

    def to_d(self):
        return {
            'span': self.span,
            'option_choices': self.option_choices,
        }
