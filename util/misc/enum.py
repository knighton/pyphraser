"""
Enum creator.

Usage:

    from enum import enum

    Color = enum('Color: RED GREEN BLUE')
"""

import re


class EnumManager(object):
    """
    Enum creator.
    """

    def __init__(self):
        self._next_id = 1337000
        self._reserved = set("""
            first
            last
            is_valid
            values
            to_s
            from_s
        """.split())
        self._key_re = re.compile('^[A-Z_][A-Z0-9_]*$')

    def create(self, class_name, keys):
        """
        (class name, keys) -> new class 'class_name' with fields 'keys'.
        """

        # Check args.
        assert class_name[0].isupper()
        assert class_name.isalnum()
        for key in keys:
            assert self._key_re.match(key)
            assert key not in self._reserved
        assert len(keys) == len(set(keys))

        values = range(self._next_id, self._next_id + len(keys))
        key2value = dict(zip(keys, values))

        d = dict(key2value)

        first = self._next_id
        last = self._next_id + len(keys) - 1
        d['first'] = first
        d['last'] = last
        d['is_valid'] = lambda self, k: \
            isinstance(k, int) and first <= k <= last

        d['values'] = set(values)

        d['to_s'] = dict(zip(values, keys))
        d['from_s'] = dict(key2value)

        base_classes = ()
        klass = type(class_name, base_classes, d)
        
        self._next_id += len(keys)

        return klass()


_ENUM_MGR = EnumManager()


def enum(text):
    """
    '(enum name): (list of space-separated enum values)' -> creates a new class.
    """
    class_name, rest = text.split(':')
    keys = rest.split()
    return _ENUM_MGR.create(class_name, keys)


def main():
    Color = enum('Color: RED GREEN BLUE')
    print Color.GREEN
    print Color.to_s[Color.GREEN]
    print Color.from_s[Color.to_s[Color.GREEN]]
    print Color.is_valid(Color.GREEN)
    print Color.is_valid('GREEN')
    print Color.is_valid('MAUVE')

    print Color.values

    print Color.to_s
    print Color.from_s


if __name__ == '__main__':
    main()
