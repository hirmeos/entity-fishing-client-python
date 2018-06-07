import unittest

from nerd.nerd import NerdClient


class NerdTest(unittest.TestCase):

    def setUp(self):
        self.target = NerdClient()

    def testDisambiguateText_simpleText(self):
        text = self.target.disambiguateText("This is a test which should be somehow working")
        assert text is not None or ""

    def testDisambiguateText_simpleText2(self):
        text = self.target.disambiguateText("This text is too short")
        assert text is None or ""


if __name__ == '__main__':
    unittest.main()
