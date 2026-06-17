import unittest

from minilang.errors import SyntaxErrorMiniLang
from minilang.lexer import lexer
from minilang.parser import Assignment, Print, While, parser


class ParserTest(unittest.TestCase):
    def test_valid_code_generates_program_ast(self):
        ast = parser(lexer("x = 10\ny = (x + 5) * 2\nprint(y - 1)"))

        self.assertEqual(len(ast.statements), 3)
        self.assertIsInstance(ast.statements[0], Assignment)
        self.assertIsInstance(ast.statements[2], Print)

    def test_valid_while_generates_while_ast(self):
        ast = parser(lexer("x = 0\nwhile x < 3\nx = x + 1\nend\nprint(x)"))

        self.assertEqual(len(ast.statements), 3)
        self.assertIsInstance(ast.statements[1], While)
        self.assertEqual(len(ast.statements[1].body), 1)

    def test_invalid_order_raises_syntax_error(self):
        with self.assertRaises(SyntaxErrorMiniLang):
            parser(lexer("x 10 = + 5"))


if __name__ == "__main__":
    unittest.main()
