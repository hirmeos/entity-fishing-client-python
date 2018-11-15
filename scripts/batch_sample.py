import sys
import time

from nerd.nerd_client_batch import NerdBatch

if len(sys.argv) != 4:
    sys.exit("Missing parameter. Usage: python nerd_batch.py /input/directory /output/directory nbThreads")

inputPath = sys.argv[1]
outputPath = sys.argv[2]
nbThreads = sys.argv[3]

#
# def saveFile(filename, result):
#     output = join(outputPath, os.path.basename(filename)) + ".json"
#     with open(output, 'w') as outfile:
#         json.dump(result, outfile)
#
#     print("Writing output to " + output)
#     return


start = time.time()
NerdBatch('http://localhost:8090/service/').process(inputPath, outputPath, int(nbThreads))

print("Batch processed in " + str(time.time() - start))
