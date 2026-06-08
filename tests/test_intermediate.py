import unittest

from minilang.intermediate import gerar_codigo
from minilang.lexer import lexer
from minilang.parser import parser


class IntermediateTest(unittest.TestCase):
    def test_generates_pseudo_assembly(self):
        ast = parser(lexer("x = 10\ny = x + 5\nprint(y)"))

        self.assertEqual(
            gerar_codigo(ast),
            [
                "LOAD 10",
                "STORE x",
                "LOAD x",
                "ADD 5",
                "STORE y",
                "PRINT y",
            ],
        )


if __name__ == "__main__":
    unittest.main()
