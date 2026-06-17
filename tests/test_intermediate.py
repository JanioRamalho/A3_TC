import unittest

from minilang.intermediate import gerar_codigo
from minilang.lexer import lexer
from minilang.parser import parser


class IntermediateTest(unittest.TestCase):
    def test_generates_pseudo_assembly(self):
        ast = parser(lexer("x = 10\ny = (x + 5) * 2\nprint(y - x)"))

        self.assertEqual(
            gerar_codigo(ast),
            [
                "LOAD 10",
                "STORE x",
                "LOAD x",
                "PUSH",
                "LOAD 5",
                "ADD_STACK",
                "PUSH",
                "LOAD 2",
                "MUL_STACK",
                "STORE y",
                "LOAD y",
                "PUSH",
                "LOAD x",
                "SUB_STACK",
                "PRINT_ACC",
            ],
        )


if __name__ == "__main__":
    unittest.main()
