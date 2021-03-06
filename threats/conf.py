"""
Configuration for threat detection.

Threat detection looks for sequences of the form

    (subject) (auxiliary verb) (adverb) (main verb)

which are defined below.
"""

from util.misc.enum import enum


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
    return patterns, annotations


SubjectCategory = enum('SubjectCategory: I WE SOMEONE_ELSE RELIGIOUS')


SUBJECTS, SUBJECT_CATS = annotated_lines(SubjectCategory, """
    i -- i
    we -- we
    (perspro +subj +3rd +person) -- someone_else
    god -- religious
    satan -- religious
    allah -- religious
""")


AuxVerbCategory = enum(
    'AuxVerbCategory: FUTURE DESIRE CONDITIONAL HYPOTHETICAL')


AUX_VERBS, AUX_VERB_CATS = annotated_lines(AuxVerbCategory, """
    (to be +pres) going to -- future
    (to be +pres) planning to -- future
    (to plan +pres) to -- future
    (to promise +pres) (perspro +subj +1st +3rd) (to be +pres +1st +3rd) going to -- future
    (to promise +pres) (perspro +subj +1st +3rd) (to be +pres +1st +3rd) gonna -- future
    (to promise +pres) (perspro +subj +1st +3rd) (to be +pres +1st +3rd) will -- future
    (to swear +pres) (perspro +subj +1st +3rd) (to be +pres +1st +3rd) going to -- future
    (to swear +pres) (perspro +subj +1st +3rd) (to be +pres +1st +3rd) gonna -- future
    (to swear +pres) (perspro +subj +1st +3rd) (to be +pres +1st +3rd) will -- future
    (to want +pres) to -- desire
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
    kick (pospro)
    kill
    make (perspro +obj) a martyr
    make an example of (perspro +obj)
    punch
    rape
    steal
    sucker punch
    rip (pospro +obj)
    rip (posdet)
    slap
    smack
    threaten
    tie
""")
