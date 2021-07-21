import functools
import string
from math import floor


def _convert_number_to_letter(num):
    if num >= 26:
        return _convert_number_to_letter(floor(num / 26) - 1) + string.ascii_uppercase[num % 26]
    else:
        return string.ascii_uppercase[num]


def _column_letters():
    itr = 0
    while True:
        yield _convert_number_to_letter(itr)
        itr += 1


class _Alphabet:
    def __init__(self, starting_length=26):
        self.letters = []
        self.letter_offset = {}

        self.column_letter_factory = _column_letters()
        self._generate_more_letters(starting_length)

    @functools.lru_cache()
    def index(self, value):
        try:
            return self.letter_offset[value]
        except KeyError:
            required_letter_count = len(value) * 26
            self._generate_more_letters(required_letter_count)
            return self.letter_offset[value]

    def __getitem__(self, item):
        try:
            return self.letters[item]
        except KeyError:
            self._generate_more_letters(item)
            return self.letters[item]

    def _generate_more_letters(self, max_letter_index):
        letter_count = len(self.letters)
        for i in range(letter_count, max_letter_index + 1):
            next_letter = next(self.column_letter_factory)
            self.letter_offset[next_letter] = i
            self.letters.append(next_letter)

    def __repr__(self):
        return "Alphabet(letter_count={})".format(len(self.letter_offset))


alphabet = _Alphabet()
