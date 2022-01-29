import subprocess
import unittest


class TestAirML(unittest.TestCase):
    def test_airml_input_args_with_valid_kn(self):
        process = subprocess.Popen(
            ['python3', 'interpreter.py', "--airml", "http://nspm.org/art", "--output", "test", "--inputstr",
             '"yuncken freeman has architected in how many cities?"'], stdout=subprocess.PIPE)
        output, err = process.communicate()
        output = output.decode("utf-8")
        self.assertTrue("http://nspm.org/art KB installed." in output)
        self.assertTrue("Predicted translation:" in output)

    def test_airml_input_args_with_invalid_kn(self):
        process = subprocess.Popen(
            ['python3', 'interpreter.py', "--airml", "http://nspm.org/arts", "--output", "test", "--inputstr",
             '"yuncken freeman has architected in how many cities?"'], stdout=subprocess.PIPE)
        output, err = process.communicate()
        output = output.decode("utf-8")
        self.assertTrue("Predicted translation:" not in output)

    def test_airml_without_input_arg(self):
        process = subprocess.Popen(
            ['python3', 'interpreter.py', "--output", "test", "--inputstr",
             '"yuncken freeman has architected in how many cities?"'], stdout=subprocess.PIPE)
        output, err = process.communicate()
        output = output.decode("utf-8")
        self.assertTrue("--input or --airml argument should be provided to load the model." in output)
        self.assertTrue("Predicted translation:" not in output)


if __name__ == '__main__':
    unittest.main()
