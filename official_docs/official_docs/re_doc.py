import re
import random
from typing import NamedTuple


def displaymatch(match):
    if match is None:
        return print('None')
    print('<Match: %r, groups=%r>' % (match.group(), match.groups()))
    if match.groups():
        print('group(1)=%r' % match.group(1))


# Regular Expression Examples
# 1 Checking for a Pair
valid = re.compile(r"^[a2-9tjqk]{5}$", re.DEBUG)
displaymatch(valid.match("akt5q"))
displaymatch(valid.match("akt5e"))  # Invalid.
displaymatch(valid.match("akt"))    # Invalid.
displaymatch(valid.match("727ak"))
print('------------------------------------------------')
pair = re.compile(r".*(.).*\1")
displaymatch(pair.match("717ak"))     # Pair of 7s.
displaymatch(pair.match("718ak"))     # No pairs.
displaymatch(pair.match("354aa"))     # Pair of aces.
print('------------------------------------------------')

# 2 Simulating scanf()
# /usr/sbin/sendmail - 0 errors, 4 warnings
# %s - %d errors, %d warnings
# (\S+) - (\d+) errors, (\d+) warning

# 3 search() vs. match()
print(re.match("c", "abcdef"))    # No match
print(re.search("c", "abcdef"))   # Match

print(re.match("c", "abcdef"))    # No match
print(re.search("^c", "abcdef"))  # No match
print(re.search("^a", "abcdef"))  # Match

print(re.match('X', 'A\nB\nX', re.MULTILINE))  # No match
print(re.search('^X', 'A\nB\nX', re.MULTILINE))  # Match
print('------------------------------------------------')

# 4 Making a Phonebook
text = """Ross McFluff: 834.345.1254 155 Elm Street

Ronald Heathmore: 892.345.3428 436 Finley Avenue
Frank Burger: 925.541.7625 662 South Dogwood Way


Heather Albrecht: 548.326.4584 919 Park Place"""
entries = re.split("\n+", text)
print(entries)
print([re.split(":? ", entry, 3) for entry in entries])
print([re.split(":? ", entry, 4) for entry in entries])
print('------------------------------------------------')


# 5 Text Munging
def repl(m):
    inner_word = list(m.group(2))
    random.shuffle(inner_word)
    return m.group(1) + "".join(inner_word) + m.group(3)


text = "Professor Abdolmalek, please report your absences promptly."
print(re.sub(r"(\w)(\w+)(\w)", repl, text))
print(re.sub(r"(\w)(\w+)(\w)", repl, text))
print('------------------------------------------------')

# 6 Finding all Adverbs
text = "He was carefully disguised but captured quickly by police."
print(re.findall(r"\w+ly", text))
print('------------------------------------------------')

# 7 Finding all Adverbs and their Positions
for m in re.finditer(r"\w+ly", text):
    print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))
print('------------------------------------------------')

# 8 Raw String Notation
print(re.match(r"\W(.)\1\W", " ff "))
# 等同于以上代码
print(re.match("\\W(.)\\1\\W", " ff "))
print(re.match(r"\\", r"\\"))
# 等同于以上代码
print(re.match("\\\\", r"\\"))


# 9 Writing a Tokenizer
class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


def tokenize(code):
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',   r':='),           # Assignment operator
        ('END',      r';'),            # Statement terminator
        ('ID',       r'[A-Za-z]+'),    # Identifiers
        ('OP',       r'[+\-*/]'),      # Arithmetic operators
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column)


statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
    ENDIF;
'''

for token in tokenize(statements):
    print(token)
