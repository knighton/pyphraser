from sequence_matcher import SequenceMatcher
import threat_config as cfg
from threat_tokenizer import ThreatTokenizer
from token_group_oracle import TokenGroupDictionary
from token_grouper import TokenGrouper


class ThreatMatch(object):
    def __init__(self, span, subject_cat, aux_verb_cat):
        self.span = span
        self.subject_cat = subject_cat
        self.aux_verb_cat = aux_verb_cat


class ThreatMatcher(object):
    def __init__(self, subjects, subject_categories, aux_verbs,
                 aux_verb_categories, adverbs, main_verbs):
        self._tokenizer = ThreatTokenizer()

        token_group_oracle = TokenGroupDictionary()
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
        self.matcher.configure(options_per_sequence)

        self._subject_categories = subject_categories
        self._aux_verb_categories = aux_verb_categories

    @staticmethod
    def init_default():
        return ThreatMatcher(
            cfg.SUBJECTS, cfg.SUBJECT_TYPES, cfg.AUX_VERBS, cfg.AUX_VERB_TYPES,
            cfg.ADVERBS, cfg.MAIN_VERBS)

    def match(self, text, allow_overlapping):
        """
        Text, whether overlapping -> yields list of ThreatMatch.
        """
        ss = self._tokenizer.tokenize(text)
        for spans, sequence_choice_lists in \
                self._matcher.match(aa, allow_overlapping):
            matches = []
            for span, choices in zip(spans, sequence_choice_lists):
                subject_x, aux_verb_x = choices[:2]
                subject_cat = self._subject_categories[subject_x]
                aux_verb_cat = self._aux_verb_categories[aux_verb_x]
                m = ThreatMatch(span, subject_cat, aux_verb_cat)
                matches.append(m)
            yield matches
