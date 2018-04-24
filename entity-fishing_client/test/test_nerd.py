import unittest

class NerdTest(unittest.TestCase):

    def setUp(self):
        self.target = NerdClient()

    def testDisambiguateText_simpleText(self):
        self.target.disambiguateText("This is a test which should be somehow working")


def main():
    unittest.main()


if __name__ == '__main__':
    main()
