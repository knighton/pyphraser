from util.enum import enum
from util.table import Table


# A column of the personals table.
#
# Meanings:
# * SUBJ subject
# * OBJ  object
# * REFL reflexive
# * POS  possessive
# * DET  determiner
#
# The possesive pronouns (which are everything but the POS_DET column) map to
# (linguistic case, is possessive).
PersonalCase = enum('PersonalCase: SUBJ OBJ REFL POS_SUBJ POS_OBJ POS_REFL POS_DET')


# Corresponds to a row in the personals table.
#
# They map to (person, number, maybe a gender).
PerNumGen = enum(
    'PerNumGen: I YOU1 THOU HE SHE IT THEY1 ONE WE YOU2 YALL THEY2 WHO1 WHO2 '
    'WHOEVER1 WHOEVER2')


def make_pronouns_table(text):
    def on_row_key(s):
        return PerNumGen.from_s[s]

    def on_column_key(s):
        return PersonalCase.from_s[s]

    def on_value(s):
        return s

    return Table.init_from_text(text, on_row_key, on_column_key, on_value)


# Personal pronouns and determiners table.
#
# This is used to provide information about words.  Also note aliases below.
personals_table = make_pronouns_table("""
             SUBJ     OBJ      REFL         POS_SUBJ  POS_OBJ    POS_REFL     POS_DET
    I        I        me       myself       mine      mine       myself's     my
    YOU1     you      you      yourself     yours     yours      yourself's   your
    THOU     thou     thee     thyself      thine     thine      thyself's    thy
    HE       he       him      himself      his       his        himself's    his
    SHE      she      her      herself      hers      hers       herself's    her
    IT       it       it       itself       its       its        itself's     its
    THEY1    they     them     themself     theirs    theirs     themself's   their
    ONE      one      one      oneself      one's     one's      oneself's    one's
    WE       we       us       ourselves    ours      ours       ourselves'   our
    YOU2     you      you      yourselves   yours     yours      yourselves'  your
    YALL     y'all    y'all    y'allsselves yall's    y'all's    y'allsselves yall's
    THEY2    they     them     themselves   theirs    theirs     themselves'  their
    WHO1     who      whom     -            whose     whose      -            whose
    WHO2     who      whom     -            whose     whose      -            whose
    WHOEVER1 whoever  whomever -            whoever's whomever's -            whoever's
    WHOEVER2 whoever  whomever -            whoever's whomever's -            whoever's
""")


def make_pronoun_aliases(text):
    d = {}
    for line in text.strip().split('\n'):
        canonical, other = line.split()
        d[other] = canonical
    return d


# Canonical form -> form to also recognize as that.
other2canonical = make_pronoun_aliases("""
    himself      hisself

    y'all        yall
    y'all        y'all's
    y'allsselves yallsselves
    y'allsselves yallselves

    you          u

    whom         who
    whomever     whoever
    whomever's   whoever's
""")
