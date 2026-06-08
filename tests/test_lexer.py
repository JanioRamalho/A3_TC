import unittest

from minilang.errors import LexicalError
from minilang.lexer import lexer
from minilang.tokens import TokenType


class LexerTest(unittest.TestCase):
    def test_valid_code_generates_tokens(self):
        tokens = lexer("x = 10\ny = x + 5\nprint(y)")
        types = [token.type for token in tokens if token.type is not TokenType.NEWLINE]

        self.assertEqual(
            types,
            [
                TokenType.ID,
                TokenType.ASSIGN,
                TokenType.NUM,
                TokenType.ID,
                TokenType.ASSIGN,
                TokenType.ID,
                TokenType.PLUS,
                TokenType.NUM,
                TokenType.PRINT,
                TokenType.LPAREN,
                TokenType.ID,
                TokenType.RPAREN,
                TokenType.EOF,
            ],
        )

    def test_invalid_character_raises_lexical_error(self):
        with self.assertRaises(LexicalError):
            lexer("x = 10 @ 5")


if __name__ == "__main__":
    unittest.main()
