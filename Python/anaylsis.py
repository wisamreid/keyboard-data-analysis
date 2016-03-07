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
    An abstract class defining handlers expected for a data file containing audio data
    """

    def setup(self):

        # load up a ExperimentParams object
        myParams=ExperimentParams()
        myParams.triggerCodes = triggerCodes


    def analyzeBlock(self):

        return "Hi"

    def analyzeSubject(self):

        return "Hello"

    def analyzeTrial(self):

        return "Bye"


if __name__ == '__main__':

    import time
    import sys


    if len(sys.argv) > 1:
        maxData = "../Experiments/MaxLogs/" + sys.argv[1]
        curryData = "../Experiments/CurryLogs/" + sys.argv[1][:-4] + ".wak"


    print "I am running"

    pass
