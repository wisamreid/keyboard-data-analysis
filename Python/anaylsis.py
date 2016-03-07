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
from lib.util import *


def buildExperiment(maxDataPaths, curryDataPaths):
    """
        Construct an analyzable experiment using max and curry generated data

        Argument(s):

                maxData: (string array) array of max generated coll file paths
                curryData: (string array) array of curry generated file paths

        Return:

                experiment: (Experiment) an experiment object ready for analysis
    """

    debug = False

    # parse data files
    raw_trial_data, blockOrdering = parseMaxData(maxDataPaths)
    raw_curry_data = parseCurryData(curryDataPaths)

    if debug:

        print "blockOrdering"
        print blockOrdering
        print "trials"
        print raw_trial_data[-1]

    raw_trial_data = removeBadTrials(raw_trial_data, raw_curry_data)

    # create notes
    # build phrases
    # build trials
    # build blocks

    # create subjects
        # assign blocks, trials, phrases

    experiment = 0

    return experiment

def parseMaxData(maxDataPaths):
    """
        Argument(s):

                maxData: (string array) array of max generated coll file paths

        Return:

                trials: (array of arrays) trials[trial number](note object array) array of trials containing note objects
                blockOrdering: (int array) Array of block ordering
    """

    numTrials = len(maxDataPaths)

    trials = []

    for trial in maxDataPaths:

        trialData = readCollFile(trial)
        trials.append(trialData)

    blockOrdering = trials.pop(0)
    # remove call file indexes
    blockOrdering = [v for i, v in enumerate(blockOrdering) if i % 2 == 1]

    return trials, blockOrdering


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

def parseCurryData(curryDataPaths):
    """
        Argument(s):

                curryData: (string array) array of curry generated file paths

        Return:

                trials: (array of arrays) trials[trial number](note object array) array of trials containing note objects
                blockOrdering: (int array) Array of block ordering
    """

    numBlocks = len(curryDataPaths)

    blocks = []

    for block in curryDataPaths:

        blockData = readCurryFile(block)
        blocks.append(blockData)

    return blocks


def readCurryFile(filename):

    return 0

def removeBadTrials(trials, curryData):
    """
        Argument(s):

            trials: (array of arrays) coll file data

        Return(s):

            decision: (array of arrays) containing only valid trial data
    """

    valid = ones(len(trials), dtype=bool)



    return 0


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
        maxDataPaths = [y for x in os.walk(maxDataLocation) for y in glob(os.path.join(x[0], '*.txt'))]

        # store the curry file locations in an array
        curryDataPaths = [y for x in os.walk(curryDataLocation) for y in glob(os.path.join(x[0], '*.ceo'))]

        try:

            ExperimentParams.subjectInitials = [str(sys.argv[1][0:2]),str(sys.argv[1][3:5])]

        except:

            print "Error: Please enter subject pair XX_YY"

    else:

        print "Error: Please enter subject pair XX_YY"
        sys.exit()

    if test_file_structure:

        print "len(maxDataPaths)"
        print len(maxDataPaths)
        print "len(curryDataPaths)"
        print len(curryDataPaths)
        print "ExperimentParams.subjectInitials"
        print ExperimentParams.subjectInitials


    experiment = buildExperiment(maxDataPaths, curryDataPaths)
