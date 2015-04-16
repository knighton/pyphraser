"""
Configuration for threat detection.

Threat detection looks for sequences of the form

    (subject) (auxiliary verb) (adverb) (main verb)

which are defined below.
"""

from util.enum import enum


def lines(s):
    """
    Block of text -> lines with comments removed.
    """
    ss = s[1:-1].split('\n')
    for i, s in enumerate(ss):
        x = s.find('#')
        if x != -1:
            ss[i] = s[:x]
    return map(lambda s: s.strip(), ss)


def annotated_lines(enum, s):
    """
    Block of text -> lines with comments removed and annotations extracted.
    """
    patterns = []
    annotations = []
    for line in lines(s):
        pattern, annotation = line.split(' -- ')
        patterns.append(pattern)
        annotation = enum.from_s[annotation.upper()]
        annotations.append(annotation)
    return patterns, annotation


SubjectCategory = enum('SubjectCategory: I_OR_WE SOMEONE_ELSE RELIGIOUS')


SUBJECTS, SUBJECT_CATS = annotated_lines(SubjectCategory, """
    (first person subject) -- i_or_we
    (third person subject) -- someone_else
    it -- someone_else
    god -- religious
    satan -- religious
    allah -- religious
""")


AuxVerbCategory = enum(
    'AuxVerbCategory: FUTURE DESIRE CONDITIONAL HYPOTHETICAL')


AUX_VERBS, AUX_VERB_CATS = annotated_lines(AuxVerbCategory, """
    (to be) going to -- future
    (to be) planning to -- future
    (to plan) to -- future
    (to promise) (first person subject) (to be) going to -- future
    (to promise) (third person subject) (to be) going to -- future
    (to promise) it (to be) going to -- future
    (to promise) (first person subject) (to be) gonna -- future
    (to promise) (third person subject) (to be) gonna -- future
    (to promise) it (to be) gonna -- future
    (to promise) (first person subject) will -- future
    (to promise) (third person subject) will -- future
    (to promise) it will -- future
    (to swear) (first person subject) (to be) going to -- future
    (to swear) (third person subject) (to be) going to -- future
    (to swear) it (to be) going to -- future
    (to swear) (first person subject) (to be) gonna -- future
    (to swear) (third person subject) (to be) gonna -- future
    (to swear) it (to be) gonna -- future
    (to swear) (first person subject) will -- future
    (to swear) (third person subject) will -- future
    (to swear) it will -- future
    (to want) to -- desire
    wanna -- desire
    will -- future
    would -- conditional
    would like to -- hypothetical
    would love to -- hypothetical
    would so -- conditional
    would want to -- conditional
""")


ADVERBS = lines("""
    # This line is intentionally blank.
    always
""")


MAIN_VERBS = lines("""
    abduct
    choke
    kick (nonher nonfirst possessive pronoun)
    kick her
    kill
    make (nonher nonfirst person object) a martyr
    make her a martyr
    make an example of
    punch
    rape
    steal
    sucker punch
    rip (nonher nonfirst possessive pronoun)
    rip her
    slap
    smack
    threaten
    tie
""")
