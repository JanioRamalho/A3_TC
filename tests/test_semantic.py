import unittest

from minilang.errors import SemanticError
from minilang.lexer import lexer
from minilang.parser import parser
from minilang.semantic import semantico


class SemanticTest(unittest.TestCase):
    def test_defined_variables_are_accepted(self):
        ast = parser(lexer("x = 10\ny = x + 5\nprint(y)"))
        defined = semantico(ast)

        self.assertEqual(defined, {"x", "y"})

    def test_undefined_variable_raises_semantic_error(self):
        ast = parser(lexer("y = x + 5"))

        with self.assertRaises(SemanticError):
            semantico(ast)


if __name__ == "__main__":
    unittest.main()
