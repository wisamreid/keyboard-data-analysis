"""
audiofile.py -- Analysis of midi keyboard data.
-----------------------------------------------------------------------
Written By: Wisam Reid
-----------------------------------------------------------------------
"""
from numpy import *
from lib.experiment import *

class Analysis(Experiment):
    """
    An abstract class defining handlers expected for a experiment data
    """

    def setup(self):

        # load up a ExperimentParams object
        myParams=ExperimentParams()
        myParams.triggerCodes = triggerCodes


    def readMaxData(self, filename):

        coll_file = open(fileName, 'r')

        dictionary = dict()

        # navigate line by line
        for line in coll_file:

                line = line.strip()
                line = line.lower()
                for word in line.split():
                        dictionary[word] = dictionary.get(word, 0) + 1

        return dictionary

    def readCurryData(self, filename):

            return "Hello Curry"


    def analyzeBlock(self):

        return "Hi"

    def analyzeSubject(self):

        return "Hello"

    def analyzeTrial(self):

        return "Bye"


if __name__ == '__main__':

    import time
    import sys
    import os

    curryData = []
    trials = []

    # enter file name to run on a single set of subjects
    if len(sys.argv) > 1:
        maxDataLocation = "../Data/MaxLogs/" + sys.argv[1]
        curryDataLocation = "../Data/CurryLogs/" + sys.argv[1]

        # store the coll max file locations in an array
        for (path, dirnames, filenames) in os.walk(maxDataLocation):
            # subjectPairs.extend(os.path.join(path, name) for name in dirnames)
            trials.extend(os.path.join(path, name) for name in filenames)

        # store the coll max file locations in an array
        for (path, dirnames, filenames) in os.walk(curryDataLocation):
            # subjectPairs.extend(os.path.join(path, name) for name in dirnames)
            curryData.extend(os.path.join(path, name) for name in filenames)

    else:

        print "Error: Please enter subject pair XX_YY"
        sys.exit()


    print len(trials)
    print len(curryData)

    # for i in range(len(subjectPairs)):
    #     print subjectPairs[i]
    #
    for i in range(len(trials)):
        print trials[i]



    print "I am running"

    pass
