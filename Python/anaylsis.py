"""
analysis.py -- Analysis of midi keyboard data.
-----------------------------------------------------------------------
Written By: Wisam Reid
-----------------------------------------------------------------------

Builds an Experiment Object made of Subject, Block, Trial, Phrase, and Note objects

Enabling data analysis within or accross any or all of these objects

The max masp generated data will be checked against the curry generated data to
validate and verify their concurance

"""
from numpy import *
from lib.experiment import *


def buildExperiment(maxData, curryData):
    """
        Argument(s):

                maxData: (string array) array of max generated coll file paths
                curryData: (string array) array of curry generated file paths

        Return:

                experiment: (Experiment) an experiment object ready for analysis
    """

    # parse data files
    trials, blockOrdering = parseMaxData(maxData)

    # get block ordering

    # create notes
    # build phrases
    # build trials
    # build blocks

    # create subjects
        # assign blocks, trials, phrases

    experiment = 0

    return experiment

def parseMaxData(maxData):
    """
        Argument(s):

                maxData: (string array) array of max generated coll file paths

        Return:

                trials: (array[trial number](note object array)) array of trials containing note objects
    """

    blockOrdering = 0

    numTrials = len(maxData)

    for trial in maxData:
        trial = readCollFile(trial)
        print trial


    return 0, blockOrdering


def isGoodTrial():
    """
        Argument(s):

            not sure: (type) stuff

        Return(s):

            decision: (int) 0 or 1
    """

    return 0


def readCollFile(filename):
    """
        Argument(s):

            filename: (string) path to max msp generated coll file

        Return(s):

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
    test_file_structure = True

    # enter file name to run on a single set of subjects
    if len(sys.argv) > 1:

        maxDataLocation = "../Data/MaxLogs/" + sys.argv[1]
        curryDataLocation = "../Data/CurryLogs/" + sys.argv[1]

        # store the max coll file locations in an array
        maxData = [y for x in os.walk(maxDataLocation) for y in glob(os.path.join(x[0], '*.txt'))]

        # store the curry file locations in an array
        curryData = [y for x in os.walk(curryDataLocation) for y in glob(os.path.join(x[0], '*.ceo'))]

        try:

            ExperimentParams.subjectInitials = [str(sys.argv[1][0:2]),str(sys.argv[1][3:5])]

        except:

            print "Error: Please enter subject pair XX_YY"

    else:

        print "Error: Please enter subject pair XX_YY"
        sys.exit()

    if test_file_structure:

        print "len(trialData)"
        print len(maxData)
        print "len(curryData)"
        print len(curryData)
        print "ExperimentParams.subjectInitials"
        print ExperimentParams.subjectInitials


    experiment = buildExperiment(maxData, curryData)
