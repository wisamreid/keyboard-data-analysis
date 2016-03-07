"""
audiofile.py -- Analysis of midi keyboard data.
-----------------------------------------------------------------------
Written By: Wisam Reid
-----------------------------------------------------------------------
"""
from numpy import *
from lib.experiment import *


def buildExperiment(trialData, curryData):
    """
        Argument(s):

        Return:

                experiment: (Experiment) an experiment object

    """

    # create notes
    # build phrases
    # build trials
    # build blocks

    # create subjects
        # assign blocks, trials, phrases

    experiment = 0

    return experiment


def readCollFile(filename):
    """
        Argument(s):

            filename: (string) path to max msp generated coll file

        Return:

            trial: (integer array) data in the coll files

    """
    # debug boolean
    debug = False

    numNoteParams = 6

    coll_file = open(filename, 'rb')
    newstring = coll_file.read()

    # pull out all the punctuation
    newstring = str.replace(str(newstring),"."," ")
    newstring = str.replace(str(newstring),","," ")
    newstring = str.replace(str(newstring),":"," ")
    newstring = str.replace(str(newstring),";"," ")
    newstring = str.lower(newstring)

    list =  str.split(newstring)
    coll_line = asarray(list)

    trial = coll_line.astype(int)

    count = len(trial)

    if not count%numNoteParams:
        noteCount = count/numNoteParams
    else:
        noteCount = "coll file is improperly formatted"
        print noteCount

    if debug:
        print "Trial Data"
        print trial
        print "Count"
        print noteCount

    return trial


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
    test_file_structure = False

    # enter file name to run on a single set of subjects
    if len(sys.argv) > 1:

        maxDataLocation = "../Data/MaxLogs/" + sys.argv[1]
        curryDataLocation = "../Data/CurryLogs/" + sys.argv[1]

        # store the max coll file locations in an array
        trialData = [y for x in os.walk(maxDataLocation) for y in glob(os.path.join(x[0], '*.txt'))]

        # store the curry file locations in an array
        curryData = [y for x in os.walk(curryDataLocation) for y in glob(os.path.join(x[0], '*.ceo'))]

        try:

            subjectInitials = [str(sys.argv[1][0:2]),str(sys.argv[1][3:5])]

        except:

            print "Error: Please enter subject pair XX_YY"

    else:

        print "Error: Please enter subject pair XX_YY"
        sys.exit()

    if test_file_structure:

        print "len(trialData)"
        print len(trialData)
        print "len(curryData)"
        print len(curryData)
        print "subjectInitials"
        print subjectInitials


    experiment = buildExperiment(trialData, curryData)

    trial = readCollFile(trialData[1])
