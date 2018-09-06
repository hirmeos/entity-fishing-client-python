import itertools
import json
import os
import sys
from concurrent.futures.process import ProcessPoolExecutor

from nerd import NerdClient
from os import listdir
from os.path import isfile, join

from zenlog import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '\n\n %(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
stream.setFormatter(formatter)
logger.addHandler(stream)


class NerdBatch:
    client = NerdClient()

    def _process(self, pdfPath):
        logger.info("Processing " + pdfPath)
        # ({'runtime': 12345, 'bao': 'miao'}, 200)#
        response, errorCode = self.client.disambiguate_pdf(pdfPath)

        if errorCode != 200:
            return None
        else:
            return response

    def processBatch(self, inputPath, callback, num_processes):
        logger.info("Processing data from {} using {} threads".format(inputPath, num_processes))

        onlyfiles = [join(inputPath, f) for f in listdir(inputPath) if
                     f.lower().endswith("pdf") and isfile(join(inputPath, f))]

        iterable = itertools.cycle(onlyfiles)
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            for filename, result in zip(iterable, executor.map(self._process, onlyfiles)):
                if result is not None:
                    logger.info("Processed {} with runtime {}".format(filename, result['runtime']))
                    callback(filename, result)
                else:
                    logger.debug("Result is null. fuck it.")


if __name__ == '__main__':
    def callback2(filename, result):
        output = join("/Users/lfoppiano/development/github/nerd-samples/out", os.path.basename(filename)) + ".json"
        with open(output, 'w') as outfile:
            json.dump(result, outfile)

        logger.info("Writing output to " + output)
        return


    NerdBatch().processBatch("/Users/lfoppiano/development/github/nerd-samples/in", callback2, 2)