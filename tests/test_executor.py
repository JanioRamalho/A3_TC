import unittest

from minilang.compiler import compilar
from minilang.executor import executar


class ExecutorTest(unittest.TestCase):
    def test_executes_intermediate_code(self):
        result = executar(["LOAD 10", "STORE x", "LOAD x", "ADD 5", "STORE y", "PRINT y"])

        self.assertEqual(result.output, [15])
        self.assertEqual(result.memory, {"x": 10, "y": 15})

    def test_full_compiler_flow(self):
        result = compilar("x = 10\ny = x + 5\nprint(y)")

        self.assertEqual(result.resultado.output, [15])


if __name__ == "__main__":
    unittest.main()
