from threats import conf
from threats.threat_tokenizer import ThreatTokenizer
from util.sequence_matcher import SequenceMatcher
from util.token_group_oracle import TokenGroupOracle
from util.token_grouper import TokenGrouper
from util.token_grouping_sequence_matcher import TokenGroupingSequenceMatcher


class ThreatMatch(object):
    def __init__(self, span, subject_cat, aux_verb_cat):
        self.span = span
        self.subject_cat = subject_cat
        self.aux_verb_cat = aux_verb_cat


class ThreatMatcher(object):
    def __init__(self, subjects, subject_categories, aux_verbs,
                 aux_verb_categories, adverbs, main_verbs):
        self._tokenizer = ThreatTokenizer()

        token_group_oracle = TokenGroupOracle()
        token_grouper = TokenGrouper()
        sequence_matcher = SequenceMatcher()
        self._matcher = TokenGroupingSequenceMatcher(
            token_group_oracle, token_grouper, sequence_matcher)

        options_per_sequence = [
            subjects,
            aux_verbs,
            adverbs,
            main_verbs,
        ]
        self._matcher.configure(options_per_sequence)

        from util.io import print_func
        map(print_func, self._matcher.dump())

        self._subject_categories = subject_categories
        self._aux_verb_categories = aux_verb_categories

    @staticmethod
    def init_default():
        return ThreatMatcher(
            conf.SUBJECTS, conf.SUBJECT_CATS, conf.AUX_VERBS,
            conf.AUX_VERB_CATS, conf.ADVERBS, conf.MAIN_VERBS)

    def match(self, text, allow_overlapping):
        """
        Text, whether overlapping -> yields list of ThreatMatch.
        """
        ss = self._tokenizer.tokenize(text)
        for spans, sequence_choice_lists in \
                self._matcher.match(ss, allow_overlapping):
            matches = []
            for span, choices in zip(spans, sequence_choice_lists):
                subject_x, aux_verb_x = choices[:2]
                subject_cat = self._subject_categories[subject_x]
                aux_verb_cat = self._aux_verb_categories[aux_verb_x]
                m = ThreatMatch(span, subject_cat, aux_verb_cat)
                matches.append(m)
            yield matches
