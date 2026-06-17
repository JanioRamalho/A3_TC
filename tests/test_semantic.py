import unittest

from minilang.errors import SemanticError
from minilang.lexer import lexer
from minilang.parser import parser
from minilang.semantic import semantico


class SemanticTest(unittest.TestCase):
    def test_defined_variables_are_accepted(self):
        ast = parser(lexer("x = 10\ny = (x + 5) * 2\nprint(y - x)"))
        defined = semantico(ast)

        self.assertEqual(defined, {"x", "y"})

    def test_undefined_variable_raises_semantic_error(self):
        ast = parser(lexer("y = x + 5"))

        with self.assertRaises(SemanticError):
            semantico(ast)

    def test_undefined_variable_inside_print_raises_semantic_error(self):
        ast = parser(lexer("x = 10\nprint(x + y)"))

        with self.assertRaises(SemanticError):
            semantico(ast)

    def test_variable_defined_only_inside_while_is_not_defined_after_loop(self):
        ast = parser(lexer("x = 0\nwhile x > 10\ny = 1\nend\nprint(y)"))

        with self.assertRaises(SemanticError):
            semantico(ast)


if __name__ == "__main__":
    unittest.main()
