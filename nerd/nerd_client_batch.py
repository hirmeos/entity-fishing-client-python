import itertools
import sys
from concurrent.futures.process import ProcessPoolExecutor
from os import listdir
from os.path import isfile, join

from nerd.nerd_client import NerdClient
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
        # response, errorCode = ({'runtime': 12345, 'bao': 'miao'}, 200)
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
                    pages = len(result['pages'])
                    runtime = result['runtime'] / 1000
                    pages_seconds = pages / runtime

                    logger.info("Processed {} ({} pages) with runtime {} s. {} pages/second."
                                .format(filename,
                                        pages,
                                        runtime,
                                        pages_seconds))

                    callback(filename, result)
                else:
                    logger.debug("Result is null. ")
