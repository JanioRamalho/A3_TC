import unittest

from minilang.errors import LexicalError
from minilang.lexer import lexer
from minilang.tokens import TokenType


class LexerTest(unittest.TestCase):
    def test_valid_code_generates_tokens(self):
        tokens = lexer("x = 10\ny = (x + 5) * 2\nwhile y > 20\nprint(y - 1)\nend")
        types = [token.type for token in tokens if token.type is not TokenType.NEWLINE]

        self.assertEqual(
            types,
            [
                TokenType.ID,
                TokenType.ASSIGN,
                TokenType.NUM,
                TokenType.ID,
                TokenType.ASSIGN,
                TokenType.LPAREN,
                TokenType.ID,
                TokenType.PLUS,
                TokenType.NUM,
                TokenType.RPAREN,
                TokenType.STAR,
                TokenType.NUM,
                TokenType.WHILE,
                TokenType.ID,
                TokenType.GT,
                TokenType.NUM,
                TokenType.PRINT,
                TokenType.LPAREN,
                TokenType.ID,
                TokenType.MINUS,
                TokenType.NUM,
                TokenType.RPAREN,
                TokenType.END,
                TokenType.EOF,
            ],
        )

    def test_invalid_character_raises_lexical_error(self):
        with self.assertRaises(LexicalError):
            lexer("x = 10 @ 5")


if __name__ == "__main__":
    unittest.main()
