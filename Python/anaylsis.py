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

    # gather raw trial data from each coll file
    for trial in maxDataPaths:

        # read coll file, return array of raw data
        trialData = readCollFile(trial)
        # add each trial to the trials array
        trials.append(trialData)

    # first coll file is the block ordering
    blockOrdering = trials.pop(0)
    # remove coll file indexes (leave just the block ordering)
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
    trial = coll_file.read()

    # pull out all the punctuation
    trial = str.replace(str(trial),"."," ")
    trial = str.replace(str(trial),","," ")
    trial = str.replace(str(trial),":"," ")
    trial = str.replace(str(trial),";"," ")

    # create an int array for trial data
    list =  str.split(trial)
    trial = asarray(list)
    trial = trial.astype(int)

    count = len(trial)

    # coll file validatation
    # (This is not robust, just a dumb sanity check for now)
    if not count%numNoteParams:
        noteCount = count/numNoteParams

    else: # check that each not has numNoteParams associated with it
        noteCount = "coll file is improperly formatted"
        print noteCount

    if debug:

        print "Trial Data: ", trial
        print "Note Count: ", noteCount

    return trial



def parseCurryData(curryDataPaths):
    """
        Argument(s):

                curryData: (string array) array of curry generated file paths

        Return:

                trials: (array of arrays) trials[trial number](note object array) array of trials containing note objects
                blockOrdering: (int array) Array of block ordering
    """
    # debug boolean
    debug = False

    numBlocks = len(curryDataPaths)
    blocks = []

    for block in curryDataPaths:

        blockData, numTriggerCodes = readCurryFile(block)
        blocks.append(blockData)

    return blocks



def readCurryFile(filename):
    """
        Argument(s):

            filename: (string) path to curry generated file containing
                        trigger codes for a block

        Return(s):

            triggerCodes: (integer array) all trigger codes for a block
            numTriggerCodes: (int) number of trigger codes
    """

    # debug boolean
    debug = False
    numTriggerCodes = 0

    # open curry file
    curry_file = open(filename, 'rb')
    line = curry_file.readline()

    # counter looking for lines including 'NUMBER_LIST'
    symbolCount = 0

    # skip all lines until fourth 'NUMBER_LIST' line
    # (the beginning of the trigger code data)
    while line != '' and symbolCount < 4:
        line = next(curry_file)

        # get number of trigger codes
        if 'ListNrRows' in line:
            list =  str.split(line)
            temp = asarray(list)
            numTriggerCodes = int(temp[2])
            triggerCodes = zeros(numTriggerCodes-1,dtype=int)

        # count 'NUMBER_LIST' instances
        if 'NUMBER_LIST' in line:
            symbolCount += 1
        if symbolCount == 4:
            # skip 'NUMBER_LIST' line and the header code in .ceo file
            line = next(curry_file)
            line = next(curry_file)

    code = 0
    # Collect the trigger codes untill the next 'NUMBER_LIST'
    # (the end of the trigger code data)
    while code < numTriggerCodes:

        list = str.split(line)
        curry_line = asarray(list)
        # only grab the trigger code and add it to the list
        triggerCodes[code] = curry_line[2]

        # go to next line
        line = next(curry_file)
        code += 1
        # break if we hit the end of the triger data
        if 'NUMBER_LIST' in line:
            break

    numTriggerCodes -= 1 # we skipped the first line of the curry data

    if debug:

        print "first trigger code: ", triggerCodes[0]
        print "last trigger code: ", triggerCodes[-1]
        print "len(triggerCodes): ", len(triggerCodes)
        print "numTriggerCodes: ", numTriggerCodes
        print "\n"

    return triggerCodes, numTriggerCodes



def removeBadTrials(trials, curryData):
    """
        Argument(s):

            trials: (array of arrays) coll file data

        Return(s):

            decision: (array of arrays) containing only valid trial data
    """

    valid = ones(len(trials), dtype=bool)



    return 0



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

        print "len(maxDataPaths): ", len(maxDataPaths)
        print "len(curryDataPaths): ", len(curryDataPaths), " (Should be 12)"
        print "ExperimentParams.subjectInitials: ", ExperimentParams.subjectInitials


    experiment = buildExperiment(maxDataPaths, curryDataPaths)
