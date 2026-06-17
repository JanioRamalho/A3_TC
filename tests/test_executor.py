import unittest

from minilang.compiler import compilar
from minilang.executor import executar


class ExecutorTest(unittest.TestCase):
    def test_executes_intermediate_code(self):
        result = executar(
            [
                "LOAD 10",
                "STORE x",
                "LOAD x",
                "PUSH",
                "LOAD 5",
                "ADD_STACK",
                "STORE y",
                "PRINT y",
            ]
        )

        self.assertEqual(result.output, [15])
        self.assertEqual(result.memory, {"x": 10, "y": 15})

    def test_full_compiler_flow(self):
        result = compilar("x = 0\ny = (10 + 5) * 2\nwhile x < 3\nx = x + 1\nend\nprint(y - x)")

        self.assertEqual(result.resultado.output, [27])
        self.assertEqual(result.resultado.memory, {"x": 3, "y": 30})


if __name__ == "__main__":
    unittest.main()
