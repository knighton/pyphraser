from threats import conf
from threats.threat_tokenizer import ThreatTokenizer
from util.sequence_matching.phrase_matcher import PhraseMatcher


class ThreatMatch(object):
    def __init__(self, span, subject_cat, aux_verb_cat):
        self.span = span
        self.subject_cat = subject_cat
        self.aux_verb_cat = aux_verb_cat


class ThreatMatcher(object):
    def __init__(self, subjects, subject_categories, aux_verbs,
                 aux_verb_categories, adverbs, main_verbs):
        self._tokenizer = ThreatTokenizer()

        blocks = [
            subjects,
            aux_verbs,
            adverbs,
            main_verbs,
        ]

        self._subject_categories = subject_categories
        self._aux_verb_categories = aux_verb_categories

        self._phrase_matcher = PhraseMatcher(blocks)

    @staticmethod
    def init_default():
        return ThreatMatcher(
            conf.SUBJECTS, conf.SUBJECT_CATS, conf.AUX_VERBS,
            conf.AUX_VERB_CATS, conf.ADVERBS, conf.MAIN_VERBS)

    def each_match_list(self, text):
        """
        Text, whether overlapping -> yields list of ThreatMatch.
        """
        ss = self._tokenizer.tokenize(text)
        for match_list in self._phrase_matcher.each_match_list(ss):
            rr = []
            for match in match_list:
                subject_x, aux_verb_x = match.option_choices[:2]
                subject_cat = self._subject_categories[subject_x]
                aux_verb_cat = self._aux_verb_categories[aux_verb_x]
                m = ThreatMatch(match.span, subject_cat, aux_verb_cat)
                rr.append(m)
            yield rr
