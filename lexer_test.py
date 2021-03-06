import unittest

from lexer import lexer


class MyTestCase(unittest.TestCase):
    def test_number(self):
        lexer.input("-0.123")
        while True:
            token = lexer.token()
            if not token:
                break
            print(token)
        self.assertEqual(True, True)

    def test_time(self):
        lexer.input("5m30s")
        while True:
            token = lexer.token()
            if not token:
                break
            print(token)

    def test_string(self):
        lexer.input(r'"ssdf   \"lkjf""sldkjfl"')
        while True:
            token = lexer.token()
            if not token:
                break
            print(token)

    def test_alri(self):
        lexer.input(r'123 + 23* 54')
        while True:
            token = lexer.token()
            if not token:
                break
            print(token)


if __name__ == '__main__':
    unittest.main()
