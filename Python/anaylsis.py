"""
audiofile.py -- Analysis of midi keyboard data.
-----------------------------------------------------------------------
Written By: Wisam Reid
-----------------------------------------------------------------------
"""
from numpy import *
from lib.experiment import *


def readTrialData(filename):

    coll_file = open(filename, 'r')

    trial = []

    # navigate line by line
    for note in coll_file:

            note = note.strip()
            note = note.lower()
            for word in line.split():
                    dictionary[word] = dictionary.get(word, 0) + 1

    return dictionary

def readCurryData(filename):

        return "Hello Curry"


def analyzeBlock():

    return "Hi"

def analyzeSubject():

    return "Hello"

def analyzeTrial():

    return "Bye"



if __name__ == '__main__':

    import time
    import sys
    import os
    from glob import glob

    # test booleans
    test_file_structure = True

    # enter file name to run on a single set of subjects
    if len(sys.argv) > 1:

        maxDataLocation = "../Data/MaxLogs/" + sys.argv[1]
        curryDataLocation = "../Data/CurryLogs/" + sys.argv[1]

        # store the max coll file locations in an array
        trials = [y for x in os.walk(maxDataLocation) for y in glob(os.path.join(x[0], '*.txt'))]

        # store the curry file locations in an array
        curryData = [y for x in os.walk(curryDataLocation) for y in glob(os.path.join(x[0], '*.ceo'))]

    else:

        print "Error: Please enter subject pair XX_YY"
        sys.exit()

    if test_file_structure:

        print "len(trials)"
        print len(trials)
        print "len(curryData)"
        print len(curryData)

    yo = readTrialData(trials[0])
    # experiment = Experiment(trials,curryData)
    # analysis = Analysis(experiment)
    # note = analysis.readMaxData(experiment.trials)
