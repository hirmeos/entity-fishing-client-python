import unittest

from nerd_batch import NerdBatch


class NerdTest(unittest.TestCase):

    def setUp(self):
        self.target = NerdBatch()

    def testDisambiguateText_longText(self):
        self.target.processBatch("/Users/lfoppiano/development/github/nerd-samples/in", 2)


if __name__ == '__main__':
    unittest.main()
