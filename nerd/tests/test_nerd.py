import unittest

from nerd.nerd import NerdClient


class NerdTest(unittest.TestCase):

    def setUp(self):
        self.target = NerdClient()

    def testDisambiguateText_simpleText(self):
        result = self.target.disambiguateText("This is a test which should be somehow working")
        assert result is not None or ""
        assert result[1] is 200


    def testDisambiguateText_simpleText2(self):
        result = self.target.disambiguateText("This text is ")
        assert result is not None
        assert result[1] is 200


if __name__ == '__main__':
    unittest.main()
