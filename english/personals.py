from collections import defaultdict

from english.base import LingGender, LingNumber, LingPerson
from util.collections import v2kk_from_k2v
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


PRONOUN_INFO2PERCOL = v2k_from_k2v(PRONOUN_PERCOL2INFO)


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


INFO2PERROW = v2k_from_k2v(PERRROW2INFO)


def personals_table_row_tuples_to_try(self, number, person, personhood, gender):
    """
    The correct way to search the INFO2PERROW dict.

    Note: none of the 'who' forms have a 'personhood = no' option.  Use 'what'
    instead.
    """
    yield (number, person, personhood, gender)
    yield (number, person, personhood, None)
    yield (number, person, None, None)


class Idiolect(object):
    """
    How to choose when the choice is arbitrary.
    """

    YOU1_OPTIONS = tuple(sorted([PersonalsRow.YOU1, PersonalsRow.THOU]))
    YOU2_OPTIONS = tuple(sorted([PersonalsRow.YOU2, PersonalsRow.YALL]))

    def __init__(self, you_or_thou, you_or_yall):
        assert you_or_thou in YOU1_OPTIONS
        assert you_or_yall in YOU2_OPTIONS

        self._options2choice = {
            YOU1_OPTIONS: you_or_thou,
            YOU2_OPTIONS: you_or_yall,
        }

    @staticmethod
    def init_default():
        return Idiolect(PersonalsRow.YOU1, PersonalsRow.YOU2)

    def choose(self, options_tuple):
        return self._options2choice[options_tuple]


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
    for line in text.strip().split('\n')[2:]:
        canonical, other = line.split()
        d[other] = canonical
    return d


# Text: list of (canonical form, form to also recognize as that).
#
# Mapping: other form -> canonical form.
other2canonical = make_pronoun_aliases("""
    canonical    other
    ---------    -----

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


class PersonalPronounInfo(object):
    def __init__(self, case, poss, number, person, personhood, gender):
        self.case = case
        self.poss = poss
        self.number = number
        self.person = person
        self.personhood = personhood
        self.gender = gender


class PersonalDeterminerInfo(object):
    def __init__(self, number, person, personhood, gender):
        self.number = number
        self.person = person
        self.personhood = personhood
        self.gender = gender


class PersonalsManager(object):
    def __init__(self, personals_table, other2canonical, idiolect):
        self._personals_table = personals_table
        self._other2canonical = other2canonical
        self._idiolect = idiolect

        self._canonical2other = k2v_to_v2kk(self._other2canonical)

        assert set(self._personals_table.rows()) == PersonalsRow.values
        assert set(self._personals_table.columns()) == PersonalsColumn.values

        self._pronoun_s2infos = defaultdict(list)
        self._determiner_s2infos = defaultdict(list)
        for row, column, s_or_none in self._personals_table.each():
            if s_or_none is None:
                continue
            s = s_or_none
            if column == PersonalsColumn.POS_DET:
                number, person, personhood, gender = PERROW2INFO[row]
                info = PersonalDeterminerInfo(
                    number, person, personhood, gender)
                d = self._determiner_s2infos
            else:
                case, poss = PRONOUN_PERCOL2INFO[column]
                number, person, personhood, gender = PERROW2INFO[row]
                info = PersonalPronounInfo(
                    case, poss, number, person, personhood, gender)
                d = self._pronoun_s2infos
            d[s].append(info)

    def _decide_row_name(self, number, person, personhood, gender):
        """
        (number, person, personhood, gender) -> row name

        Decide which row in the table to use for this combination.

        Notes:
        * It will assert if you use 'personhood = no' for an interrogative form.
          Use 'what' instead, not 'who'.
        * Otherwise, personhood usually doesn't matter.
        * Gender only changes the output if third person singular.
        """
        for key in personals_table_row_tuples_to_try(
                number, person, personhood, gender):
            row_names = INFO2PERROW.get(key)
            if row_names:
                if len(options) == 1:
                    return row_names[0]

                return self._idiolect.choose(tuple(sorted(row_names)))

        assert False

    def _decide_column_name(self, case, poss):
        """
        (case, poss) -> column name
        """
        return PRONOUN_INFO2PERCOL[(case, poss)]

    def encode_pronoun(self, ppi):
        """
        (case, poss, number, person, personhood, gender) -> word or None
        """
        row = self._decide_row_name(
            ppi.number, ppi.person, ppi.personhood, ppi.gender)
        column = self._decide_column_name(case, poss)
        return self._personals_table.get(row, column)

    def encode_determiner(self, pdi):
        """
        (number, person, personhood, gender) -> word or None
        """
        row = self._decide_row_name(
            pdi.number, pdi.person, pdi.personhood, pdi.gender)
        column = PersonalsColumn.POS_DET
        return self._personals_table.get(row, column)

    def decode_pronoun(self, s):
        """
        word -> list of PersonalPronounInfo
        """
        return self._pronoun_s2infos.get(s, [])

    def decode_determiner(self, s):
        """
        word -> list of PersonalDeterminerInfo
        """
        return self._determiner_s2infos.get(s, [])

    def decode(self, s):
        """
        word list of (PersonalPronounInfo or PersonalDeterminerInfo)
        """
        return self.decode_pronoun() + self.decode_determiner()

