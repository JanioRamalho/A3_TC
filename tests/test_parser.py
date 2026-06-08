import unittest

from minilang.errors import SyntaxErrorMiniLang
from minilang.lexer import lexer
from minilang.parser import Assignment, Print, parser


class ParserTest(unittest.TestCase):
    def test_valid_code_generates_program_ast(self):
        ast = parser(lexer("x = 10\ny = x + 5\nprint(y)"))

        self.assertEqual(len(ast.statements), 3)
        self.assertIsInstance(ast.statements[0], Assignment)
        self.assertIsInstance(ast.statements[2], Print)

    def test_invalid_order_raises_syntax_error(self):
        with self.assertRaises(SyntaxErrorMiniLang):
            parser(lexer("x 10 = + 5"))


if __name__ == "__main__":
    unittest.main()
