import re
from dataclasses import dataclass
from typing import Any

@dataclass
class Location:
    filename: str = ""
    line: int = 0
    column: int = 0

    def __eq__(self, other: Any) -> bool:
        # If the other is the special 'L' object, return True.
        if other is L:
            return True
        if not isinstance(other, Location):
            return NotImplemented
        return (self.filename, self.line, self.column) == (other.filename, other.line, other.column)
    
@dataclass
class Token:
    loc: Location
    type: str
    text: str

    def __eq__(self, other: Any) -> bool:
        # If either self.loc or other.loc is L, return True if the rest matches
        if self.loc is L or other.loc is L:
            return self.type == other.type and self.text == other.text
        if not isinstance(other, Token):
            return NotImplemented
        return (self.loc, self.type, self.text) == (other.loc, other.type, other.text)

L = Location("", -1, -1)

def get_token_type(text: str) -> str:
    if text in ['+', '-', '*', '**', '/', "=", '==', "!=", "<", "<=", ">", ">="]:
        return "operator"
    if text in ['(', ')', '{', '}', ';', ',']:
        return "punctuation"
    if text.isidentifier():
        return "identifier"
    if text.isdigit():
        return "int_literal"
    return "unknown"

def tokenize(source_code: str, filename: str = "") -> list[Token]:
    token_pattern = r'''
        (?P<WHITESPACE>\s+)|                             # Whitespace
    (?P<COMMENT>//[^\n]*|\#[^\n]*)|                      # One-line comments (// or #)
    (?P<TOKEN>
        \*\*|<<|>>|<=|>=|==|!=|                          # Multi-character operators
        \+|\-|\*|\/|\=|\<|\>|\(|\)|\{|\}|\,|\;|          # Single-character operators and punctuation
        [a-zA-Z_][a-zA-Z0-9_]*|                          # Identifiers
        \d+                                              # Integer literals
    )
    '''

    line_num = 1
    col_num = 1
    tokens = []

    for match in re.finditer(token_pattern, source_code, re.VERBOSE):
        kind = match.lastgroup
        value = match.group()
        start, end = match.span()

        col_num = start - source_code.rfind('\n', 0, start)

        if kind == 'TOKEN':
            token_type = get_token_type(value)
            token_location = Location(filename, line_num, col_num)
            tokens.append(Token(loc=token_location, type=token_type, text=value))
        elif kind == 'WHITESPACE':
            newline_count = value.count('\n')
            if newline_count > 0:
                line_num += newline_count
                col_num = 1
            else:
                col_num += len(value)
        # Skip over comments
        elif kind == 'COMMENT':
            newline_count = value.count('\n')
            if newline_count > 0:
                line_num += newline_count
                col_num = 1
            else:
                col_num += len(value)

    return tokens


if __name__ == "__main__":
    print("hi")
    # print(tokenize("aaa 123 bbb 2 == 3,#4 "))
    # print(tokenize("if 3\nwhile -2"))
    # assert tokenize("if 3\nwhile") == ["if", "3", "while"]