from collections import defaultdict

from english.base import LingGender, LingNumber, LingPerson
from util.enum import enum
from util.table import Table


# A column of the personal pronouns and determiners table.
#
# All but POS_DET are the pronouns.
#
# Meanings:
# * SUBJ subject
# * OBJ  object
# * REFL reflexive
# * POS  possessive
# * DET  determiner
PersonalsColumn = enum(
    'PersonalsColumn: NP_SUBJ NP_OBJ NP_REFL POS_SUBJ POS_OBJ POS_REFL POS_DET')


# Personal pronoun case.
PersProCase = enum('PersProCase: SUBJ OBJ REFL')


# Possessivity.
Poss = enum('Poss: NO YES')


# For personal pronouns:
#
# personals table column -> (case, is possessive).
PRONOUN_PERCOL2INFO = {
    PersonalsColumn.NP_SUBJ:  (PersProCase.SUBJ, Poss.NO),
    PersonalsColumn.NP_OBJ:   (PersProCase.OBJ,  Poss.NO),
    PersonalsColumn.NP_REFL:  (PersProCase.REFL, Poss.NO),
    PersonalsColumn.POS_SUBJ: (PersProCase.OBJ,  Poss.YES),
    PersonalsColumn.POS_OBJ:  (PersProCase.OBJ,  Poss.YES),
    PersonalsColumn.POS_REFL: (PersProCase.OBJ,  Poss.YES),
}


# A row of the personal pronouns and determiners table.
PersonalsRow = enum(
    'PersonalsRow: I YOU1 THOU HE SHE IT THEY1 ONE WHO1 WHOEVER1 WE YOU2 YALL '
    'THEY2 WHO2 WHOEVER2')


# For both personal pronouns and personal determiners:
#
# personals table row -> (number, person, maybe gender).
N = LingNumber
P = LingPerson
PH = LingPersonhood
G = LingGender
PERROW2INFO = {
    PersonalsRow.I:        (N.SING, P.FIRST,     None,   None),
    PersonalsRow.YOU1:     (N.SING, P.SECOND,    None,   None),
    PersonalsRow.THOU:     (N.SING, P.SECOND,    None,   None),
    PersonalsRow.HE:       (N.SING, P.THIRD,     PH.YES, G.MALE),
    PersonalsRow.SHE:      (N.SING, P.THIRD,     PH.YES, G.FEMALE),
    PersonalsRow.IT:       (N.SING, P.THIRD,     PH.NO,  G.NEUTER),
    PersonalsRow.THEY1:    (N.SING, P.THIRD,     PH.YES, None),
    PersonalsRow.ONE:      (N.SING, P.THIRD,     None,   None),
    PersonalsRow.WHO1:     (N.SING, P.INTR,      PH.YES, None),
    PersonalsRow.WHOEVER1: (N.SING, P.INTR_EMPH, PH.YES, None),
    PersonalsRow.WE:       (N.PLUR, P.FIRST,     None,   None),
    PersonalsRow.YOU2:     (N.PLUR, P.SECOND,    None,   None),
    PersonalsRow.YALL:     (N.PLUR, P.SECOND,    None,   None),
    PersonalsRow.THEY2:    (N.PLUR, P.THIRD,     None,   None),
    PersonalsRow.WHO2:     (N.PLUR, P.INTR,      PH.YES, None),
    PersonalsRow.WHOEVER2: (N.PLUR, P.INTR_EMPH, PH.YES, None),
}


class Idiolect(object):
    """
    How to choose when the choice is arbitrary.
    """

    def __init__(self, you_or_thou, you_or_yall):
        self.you_or_thou = you_or_thou
        self.you_or_yall = you_or_yall

        assert self.you_or_thou in (PersonalsRow.YOU1, PersonalsRow.THOU)
        assert self.you_or_yall in (PersonalsRow.YOU2, PersonalsRow.YALL)

    @staticmethod
    def init_default():
        return Idiolect(PersonalsRow.YOU1, PersonalsRow.YOU2)


def make_pronouns_table(text):
    def on_row_key(s):
        return PersonalsRow.from_s[s]

    def on_column_key(s):
        return PersonalsColumn.from_s[s]

    def on_value(s):
        if s == '-':
            return None
        return s

    return Table.init_from_text(text, on_row_key, on_column_key, on_value)


# Personal pronouns and determiners table.
#
# This is used to provide information about words.  Also note aliases below.
personals_table = make_pronouns_table("""
             NP_SUBJ  NP_OBJ   NP_REFL      POS_SUBJ  POS_OBJ    POS_REFL     POS_DET
    I        I        me       myself       mine      mine       myself's     my
    YOU1     you      you      yourself     yours     yours      yourself's   your
    THOU     thou     thee     thyself      thine     thine      thyself's    thy
    HE       he       him      himself      his       his        himself's    his
    SHE      she      her      herself      hers      hers       herself's    her
    IT       it       it       itself       its       its        itself's     its
    THEY1    they     them     themself     theirs    theirs     themself's   their
    ONE      one      one      oneself      one's     one's      oneself's    one's
    WHO1     who      whom     -            whose     whose      -            whose
    WHOEVER1 whoever  whomever -            whoever's whomever's -            whoever's
    WE       we       us       ourselves    ours      ours       ourselves'   our
    YOU2     you      you      yourselves   yours     yours      yourselves'  your
    YALL     y'all    y'all    y'allsselves yall's    y'all's    y'allsselves yall's
    THEY2    they     them     themselves   theirs    theirs     themselves'  their
    WHO2     who      whom     -            whose     whose      -            whose
    WHOEVER2 whoever  whomever -            whoever's whomever's -            whoever's
""")


def make_pronoun_aliases(text):
    d = {}
    for line in text.strip().split('\n'):
        canonical, other = line.split()
        d[other] = canonical
    return d


# Text: list of (canonical form, form to also recognize as that).
#
# Mapping: other form -> canonical form.
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


def flip_dict(k2v):
    d = defaultdict(list)
    for k, v in k2v.iteritems():
        d[v].append(k)
    return d


class PersonalsManager(object):
    def __init__(self, personals_table, other2canonical, idiolect):
        self._personals_table = personals_table
        self._other2canonical = other2canonical
        self._idiolect = idiolect

        self._canonical2other = flip_dict(self._other2canonical)

        assert set(self._personals_table.rows()) == PersonalsRow.values
        assert set(self._personals_table.columns()) == PersonalsColumn.values

    def get_personal_pronoun(self, number, person, personhood, gender):
        """
        (number, person, personhood, gender) -> word or None.

        Notes:
        * It will assert if you use 'personhood = no' for an interrogative form.
          Use 'what' instead, not 'who'.
        * Otherwise, personhood usually doesn't matter.
        * Gender only changes the output if third person singular.
        """
        pass

    def each(self):
        pass
