from threats.conf import AuxVerbCategory, SubjectCategory


class ThreatMatch(object):
    def __init__(self, span, subject_cat, aux_verb_cat):
        self.span = span
        self.subject_cat = subject_cat
        self.aux_verb_cat = aux_verb_cat

    def to_d(self):
        return {
            'span': self.span,
            'subject_cat': SubjectCategory.to_s[self.subject_cat],
            'aux_verb_cat': AuxVerbCategory.to_s[self.aux_verb_cat],
        }
