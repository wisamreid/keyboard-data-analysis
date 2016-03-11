"""
analysis.py -- Analysis of midi keyboard data.
-----------------------------------------------------------------------
Written By: Wisam Reid
-----------------------------------------------------------------------

    Builds an Experiment Object made of Subject, Block, Trial, Phrase, and Note objects

    Enabling data analysis within or across any or all of these objects

    The max masp generated data will be checked against the curry generated data to
    validate and verify their concurance

"""

from numpy import *
from lib.experiment import *
from lib.util import *

def buildExperiment(maxDataPaths, curryDataPaths, scoreDataPaths):
    """

        Constructs an analyzable experiment using max, curry, and score data

        ##### NOTE: Eventualy this should be expanded:

                    1) An experiment could be built from anything imported
                    through the file system.

                    For Example:    A table containing trigger codes for a new
                                    experiment


        Argument(s):

                maxDataPaths: (string array) array of max generated coll file paths
                curryDataPaths: (string array) array of curry generated file paths
                scoreDataPaths: (string array) array of score file paths

        Return:

                experiment: (Experiment) an experiment object ready for analysis
    """

    debug = False

    # parse data files
    raw_trial_data, blockOrdering = parseMaxData(maxDataPaths)
    # parse curry files
    raw_curry_data = parseCurryData(curryDataPaths)
    # parse score files
    raw_score = parseScore(scoreDataPaths)


    #### TODO  # finish this function

    # raw curry data is currently divided into blocks
    # break it into trials, Code function below, call it here

    #### TODO  # Code function below, call it here
    # throw out bad trials

    curry_trial_data = blocksToTrials(raw_curry_data)

    if debug:

        print "---- Testing buildExperiment Function ----"
        print "---- Max Parsing ----"
        print "First Trial (Raw Data): ", raw_trial_data[0]
        print "Last Trial (Raw Data): ", raw_trial_data[-1]
        print "Block Ordering: ", blockOrdering
        print "---- Curry Parsing ----"
        print "First Block Trigger Codes: ", raw_curry_data[0]
        print "Last Block Trigger Codes: ", raw_curry_data[-1]
        # print "Number of Trigger Codes: ", numTriggerCodes
        print "\n"

    raw_trial_data = removeBadTrials(raw_trial_data, curry_trial_data)

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
    # debug boolean
    debug = False

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

    if debug:

        print "---- Testing buildExperiment Function ----"
        print "\n"

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

        print "---- Testing readCollFile Function ----"
        print "Trial Data: ", trial
        print "Note Count: ", noteCount
        print "\n"

    return trial

def parseCurryData(curryDataPaths):
    """
        Argument(s):

                curryDataPaths: (string array) array of curry generated file paths

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

    if debug:

        print "---- Testing parseCurryData Function ----"
        print "First Block: ", blocks[0]
        print "Last Block: ", blocks[-1]
        print "len(blocks): ", len(blocks)
        print "\n"

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

        print "---- Testing readCurryFile Function ----"
        print "first trigger code: ", triggerCodes[0]
        print "last trigger code: ", triggerCodes[-1]
        print "len(triggerCodes): ", len(triggerCodes)
        print "numTriggerCodes: ", numTriggerCodes
        print "\n"

    return triggerCodes, numTriggerCodes

def parseScore(scoreDataPaths):
    """
        Argument(s):

                scoreDataPaths: (string array) array of score file paths

        Return:

                scores: (array of arrays) scores[score number](note object array) array of trials containing note objects
    """

    numScores = len(scoreDataPaths)

    ##### TODO # Fill in code

    return 0

def blocksToTrials(curryData):
    """

    Function to divide curry data (in blocks) into trial data

        Argument(s):

            curryData: (array of arrays) raw curry data

        Return(s):

            curryTrials: (array of arrays) curry data divided trial arrays
    """

    ###### TODO # finish this function

    debug = False

    numBlocks = len(curryData)
    curry_data= copy(curryData)

    code = 233 # hardcoded for now
    item_index = where(curry_data[0]==code)

    # poo = split(curryData[0], 233)

    if debug:
        print "---- Testing blocksToTrials Function ----"
        print item_index
        print curryData[0],len(curryData[0])


    return 0

def removeBadTrials(trials, curryData):
    """

    Function used to filter out bad trials before constructing the experiment

        Argument(s):

            trials: (array of arrays) coll file data

        Return(s):

            decision: (array of arrays) containing only valid trial data
    """

    valid = ones(len(trials), dtype=bool)

    ###### TODO # Fill in code

    return 0

if __name__ == '__main__':

    import time
    import sys
    import os
    from glob import glob

    # test boolean(s)
    test_file_structure = False


    # enter file name to run on a single set of subjects
    if len(sys.argv) > 1:

        maxDataLocation = "../Data/MaxLogs/" + sys.argv[1]
        curryDataLocation = "../Data/CurryLogs/" + sys.argv[1]
        scoreDataLocation = "../Data/Scores/"

        # store the max coll file locations in an array
        maxDataPaths = [y for x in os.walk(maxDataLocation) for y in glob(os.path.join(x[0], '*.txt'))]

        # store the curry file locations in an array
        curryDataPaths = [y for x in os.walk(curryDataLocation) for y in glob(os.path.join(x[0], '*.ceo'))]

        # store the score file locations in an array
        scoreDataPaths = [y for x in os.walk(scoreDataLocation) for y in glob(os.path.join(x[0], '*.txt'))]

        try:

            ExperimentParams.subjectInitials = [str(sys.argv[1][0:2]),str(sys.argv[1][3:5])]

        except:

            print "Error: Please enter subject pair XX_YY"

    else:

        print "Error: Please enter subject pair XX_YY"
        sys.exit()

    if test_file_structure:

        print "---- Testing File Structure ----"
        print "len(maxDataPaths): ", len(maxDataPaths)
        print "len(curryDataPaths): ", len(curryDataPaths), " (Should be 12)"
        print "len(ScoreDataPaths): ", len(scoreDataPaths), " (Should be 4)"
        print "ExperimentParams.subjectInitials: ", ExperimentParams.subjectInitials

    # construct an experiment object, ready for analysis
    experiment = buildExperiment(maxDataPaths, curryDataPaths, scoreDataPaths)
