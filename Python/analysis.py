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

def buildExperiment(subjectDataPaths, maxDataPaths, curryDataPaths, scoreDataPaths, ExperimentParams, DebugPrintParams):
    """

        Constructs an analyzable experiment using max, curry, and score data

        ##### NOTE: Eventualy this should be expanded:

                # 1) An experiment could be built from anything imported
                through the file system.

                For Example:    A table containing trigger codes for a new
                                experiment


        Argument(s):

                subjectDataPaths: (string array) array of subject (Pairs) data folder names
                maxDataPaths: (string array of arrays) arrays of max generated coll file paths
                curryDataPaths: (string array of arrays) arrays of curry generated file paths
                scoreDataPaths: (string array) array of score file paths
                ExperimentParams: class for dynamically generated variables

        Return:

                experiment: (Experiment) an experiment object ready for analysis
    """

    local_debug = False

    numSubjects = len(subjectDataPaths)
    raw_curry_data = []
    curry_trial_data = []
    raw_max_data = []
    blockOrdering = []

    #### PARSE SCORE ####
    raw_score = parseScore(scoreDataPaths)

    #### PARSE MAX ####
    # loop over subjects
    for subjectPair in range(len(subjectDataPaths)):
        # parse max data files
        raw_max_data_one_subject_pair, blockOrdering_one_subject_pair = parseMaxData(maxDataPaths[subjectPair])

        raw_max_data.append(raw_max_data_one_subject_pair)
        blockOrdering.append(blockOrdering_one_subject_pair)

        raw_curry_data.append(parseCurryData(curryDataPaths[subjectPair]))


    #### PARSE CURRY ####
    # loop over subjects
    for subjectPair in range(len(subjectDataPaths)):
        # raw curry data is currently divided into blocks break it into trials
        # loop over the blocks for each subject pair
        DebugPrintParams.current_subject_pair = subjectPair # set print options then pass to helper functions
        for block in range(len(raw_curry_data[subjectPair])):
            # chop curry block data into trials
            DebugPrintParams.current_block = block
            curry_trial_data.append(blockToTrials(raw_curry_data[subjectPair][block], ExperimentParams, DebugPrintParams))

    # if local_debug:
    if debug_buildExperiment:
        for subjectPair in range(len(subjectDataPaths)):
            print "Block Ordering for Subject Pairing", subjectDataPaths[subjectPair], ": ", blockOrdering[subjectPair]
            print "\n"
        print "Number of Subjects: ", numSubjects
        print "\n"
        print "\n"
        print "--------------------------------------------------------"
        print "Still need to throw out practice trials and bad trials!:"
        print "--------------------------------------------------------"
        print "\n"
        print "---------------------------------------------"
        print "---------------- Max Parsing ----------------"
        print "---------------------------------------------"
        print "\n"
        print "Number of Trials per Subject Pairing: "
        print listOfListLengths(raw_max_data)
        print "\n"
        print "Total Number of Trials: ", sum(listOfListLengths(raw_max_data))
        print "\n"
        print "First Trial for Subject Pairing", subjectDataPaths[0], ": "
        print raw_max_data[0][0]
        print "\n"
        print "-----------------------------------------------"
        print "---------------- Curry Parsing ----------------"
        print "-----------------------------------------------"
        print "\n"
        print "Total Number of Trials: ", sum(listOfListLengths(curry_trial_data))
        print "\n"
        print "Number of Curry Blocks: ", len(listOfListLengths(curry_trial_data)), " ( Should be ", 60, ")"
        print "\n"
        print "Number of Trials in Block: "
        print listOfListLengths(curry_trial_data)
        print "\n"
        print "Number of Trials per Subject Pairing: "
        print [sum(listOfListLengths(curry_trial_data)[:12]),sum(listOfListLengths(curry_trial_data)[12:24]), sum(listOfListLengths(curry_trial_data)[24:36]), sum(listOfListLengths(curry_trial_data)[36:48]),sum(listOfListLengths(curry_trial_data)[48:])]
        print "\n"
        print "Number of Blocks per Subject Pairing: "
        print [len(listOfListLengths(curry_trial_data)[:12]),len(listOfListLengths(curry_trial_data)[12:24]), len(listOfListLengths(curry_trial_data)[24:36]), len(listOfListLengths(curry_trial_data)[36:48]),len(listOfListLengths(curry_trial_data)[48:])]
        print "\n"
        print "[Fist Block : First Trial] Trigger Codes: "
        print curry_trial_data[0][0]
        print "\n"

        if verbose:
            print "-----------------------------------------"
            print "---------------- Verbose ----------------"
            print "-----------------------------------------"
            print "\n"
            print "First Subject : First Trial (Max Raw Data): "
            print raw_max_data[0][0]
            print "\n"
            print "Last Subject : Last Trial (Max Raw Data): "
            print raw_max_data[-1][-1]
            print "\n"
            print "\n"
            print "----------------------------------------------"
            print "---------------- Debug Prints ----------------"
            print "----------------------------------------------"
            print "\n"
            print "---- Current Block ----"
            print DebugPrintParams.current_block + 1
            print "Value: ", DebugPrintParams.current_block
            print "\n"
            print "---- Current Subject Pair ----"
            print subjectDataPaths[DebugPrintParams.current_subject_pair]
            print "Value: ", DebugPrintParams.current_subject_pair
            print "\n"

    #### MERGE AND CONCUR DATA ####
    #### TODO  # Code function below, call it here
    # throw out bad trials
    raw_max_data = removeBadTrials(raw_max_data, curry_trial_data,ExperimentParams)

    #### BUILD EXPERIMENT OBJECT ####
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

    if debug_parseMaxData:
        print "-------- Number of Trials in the Block --------"
        print "\n"
        print numTrials
        print "\n"
        if verbose:
            print "-------- Number of Trials in the Block --------"
            print "\n"
            print trials
            print "\n"
    return trials, blockOrdering

def readCollFile(filename):
    """
        Argument(s):

            filename: (string) path to max msp generated coll file

        Return(s):

            trial: (integer array) data in the coll files
    """

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
    if debug_readCollFile:
        print trial
    trial = trial.astype(int)

    count = len(trial)

    # coll file validatation
    # (This is not robust, just a dumb sanity check for now)
    if not count%numNoteParams:
        noteCount = count/numNoteParams

    else: # check that each not has numNoteParams associated with it
        noteCount = "coll file is improperly formatted"
        print noteCount

    if debug_readCollFile:

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

def blockToTrials(curryData, ExperimentParams, DebugPrintParams):
    """

    Function to divide a block of curry data into arrays of trial data

        Argument(s):

            curryData: (int array) raw curry data (One Block)

        Return(s):

            curryTrials: (array of arrays) curry data divided by trial (One Block)
                        this will return good and bad trials to be validated later
    """

    # Print Variables
    global debug_blockToTrials # Allows for dynamic debug print options
    subjectsToPrint = DebugPrintParams.subjects_to_print

    # helper function for block parsing
    find = lambda searchList, elem: [[i for i, x in enumerate(searchList) if x == e] for e in elem]

    curry_data = copy(curryData)

    # this is trigger code # 233 : metro tick
    metro_tick_trigger_code = ExperimentParams.metronome_codes[-1]
    # these are the indices for all metro trigger codes (201 - 233)
    metro_ticks = find(curry_data, ExperimentParams.metronome_codes)

    metro_tick_trigger_code_indices = []
    # we now need to grab only the last metro ticks so we can use them to
    # break the block into trials (this is only for TC# 233 since they are repeated)
    valid = ediff1d(metro_ticks[-1]) - 1 # creates a mask (in order to eliminate repeats keeping the last tick)
    for tick in range(len(valid)):
        if valid[tick]:
            metro_tick_trigger_code_indices.append(metro_ticks[-1][tick])

    # combine into one list and then sort
    # after we make the last decision to keep or throw out # 233 ticks
    # these are the indices we will cut our block with
    final_indices = []

    for code in range(len(metro_ticks)-1):
        if metro_ticks[code]:
            final_indices.append(metro_ticks[code])

    # append indices for TC# 233
    final_indices.append(metro_tick_trigger_code_indices)
    final_indices = reduce(lambda x,y: x+y,final_indices)
    # sort the full list of indices
    final_indices = sorted(final_indices)

    # Decide which Trigger code: #233's to keep
    # we will thow out the values that only jump by 2
    # we want to replace the second value with the first value
    final_valid = ediff1d(final_indices)
    minDiff = min(final_valid)
    final_valid -= minDiff # set low values to zero

    # decide which TC 233's to keep
    for index in range(len(final_valid)):

        if not final_valid[index] and index + 1 <= len(final_indices):
            # replace indexes to be removed with zeros
            final_indices[index+1] = 0
    final_indices = filter(lambda a: a != 0, final_indices) # remove zeros

    # cut our list of trigger codes recieved by curry into individual trials
    # we cut the at the indices we just gathered
    curryTrials = partitionList(curry_data,final_indices)

    #### final clean up ####

    for index, trial in enumerate(curryTrials):
        # after cutting, delete all instances of 233 TCs for trials
        # that dont begin with 233
        if trial[0] != metro_tick_trigger_code:
            curryTrials[index] = filter(lambda a: a != metro_tick_trigger_code, trial) # remove zeros

    if DebugPrintParams.subjects_to_print == ".":
        subjectsToPrint = DebugPrintParams.current_subject_pair

    if DebugPrintParams.current_subject_pair == subjectsToPrint:
        if DebugPrintParams.blocks_to_print != '.':
            # print  DebugPrintParams.blocks_to_print,  type(DebugPrintParams.blocks_to_print)
            # print  DebugPrintParams.current_block, type(DebugPrintParams.current_block)
            if DebugPrintParams.blocks_to_print == DebugPrintParams.current_block:
                print "---------------------------------------------------------------------"
                print "---- Printing Subject Pair:", subjectPathsMax[DebugPrintParams.current_subject_pair], " Printing Block:", DebugPrintParams.current_block, "----------------"
                print "---------------------------------------------------------------------"
                print "\n"
                print "current_block: ", DebugPrintParams.current_block
                debug_blockToTrials = True
            else:
                debug_blockToTrials = False

        if debug_blockToTrials:
            print "---- Number of Trials in the Block ----"
            print "\n"
            print len(curryTrials)
            print "\n"
            print "---- First Curry Trial ----"
            print curryTrials[1]
            print "Number of Codes in Trial: ", len(curryTrials[1])
            print "\n"
            # decide how many trials to print
            number_of_trials_Print_trigger_codes, block_number_Print_trigger_codes = printOptionsBlockToTrials(sys.argv,len(curryTrials))

            if number_of_trials_Print_trigger_codes <= len(curryTrials) + 2: # first and last
                for i in range(number_of_trials_Print_trigger_codes):
                    print "---- Curry Trial Number:", str(i+2)," ----"
                    print curryTrials[i+1]
                    print "Number of Codes in Trial: ", len(curryTrials[i+1])
                    print "\n"
            else:
                print "WARNING: number out of bounds, Did not print extra trials"
                print "\n"
            print "---- Last Curry Trial ----"
            print curryTrials[-1]
            print "Number of Codes in Trial: ", len(curryTrials[-1])
            print "\n"


            if verbose:
                print "-----------------------------------------"
                print "---------------- Verbose ----------------"
                print "-----------------------------------------"
                print "\n"
                print "---- Trigger Codes Associated with Metronome Ticks ----"
                print ExperimentParams.metronome_codes
                print "\n"
                print "---- final_indices ----"
                # we should have twelve instances of 4 different trigger codes
                # Since each trigger code is a permutaion of 2 variables that determine
                # the order of deviant phrases
                print "---- Trigger Codes Associated with Metronome Ticks  : [Index of] ----"
                print metro_ticks
                print "\n"
                print final_indices
                print "\n"

    return curryTrials

def removeBadTrials(trials, curryData, ExperimentParams):
    """

    Function used to filter out bad trials before constructing the experiment

        Argument(s):

            trials: (array of arrays) coll file data

        Return(s):

            decision: (array of arrays) containing only valid trial data
    """

    valid = ones(len(trials), dtype=bool)

    ###### TODO # Fill in code

    # look for prcatice trials
    # look for error codes
    # look for out of place shit (May need to look at block ordering)

    if debug_removeBadTrials:
        pass

    return 0

if __name__ == '__main__':

    from lib.analysis_utilities import *
    from lib.experiment import *

    #### TODO # add flag documentation to the readme

    #### test print booleans ####
    verbose = False

    # debug flags [for each function]
    debug_main = False
    debug_buildExperiment = False
    debug_blockToTrials = False
    debug_removeBadTrials = False
    debug_readCollFile = False
    debug_parseMaxData = False

    # testing variables
    number_of_trials_Print_trigger_codes = 0
    block_number_Print_trigger_codes = '.'
    subjectsToPrint = '.'

    #### COMMANDLINE PARSING ####
    # enter file name to run on a single set of subjects
    # '.' runs all subjects
    if len(sys.argv) > 1:
        subjects = sys.argv[1]
        # check for help menu
        if len(sys.argv) == 2:
            if sys.argv[1] == '-h':
                printHelpMenu()
        if len(sys.argv) >= 3: # TODO # Check this
            if sys.argv[2] == 'main':
                debug_main = True
            if sys.argv[-1] == '-v':
                verbose = True

        maxDataLocation = "../Data/MaxLogs/"
        curryDataLocation = "../Data/CurryLogs/"
        scoreDataLocation = "../Data/Scores/"

        # path to all subjects' max data
        subjectPathsMax = []
        for (dirpath, dirnames, filenames) in walk(maxDataLocation):
            subjectPathsMax.extend(dirnames)
            break

        # path to all subjects' curry data
        subjectPathsCurry = []
        for (dirpath, dirnames, filenames) in walk(curryDataLocation):
            subjectPathsCurry.extend(dirnames)
            break

        if subjectPathsCurry != subjectPathsMax:
            commandlineErrorMain(sys.argv,'fileStructure')

        maxDataPaths= []
        curryDataPaths = []
        for index, subjectPair in enumerate(subjectPathsMax):
            # for
            maxDataLocation = "../Data/MaxLogs/" + subjectPair
            curryDataLocation = "../Data/CurryLogs/" + subjectPair

            # store the max coll file locations in an array
            maxDataPaths.append([y for x in os.walk(maxDataLocation) for y in glob(os.path.join(x[0], '*.txt'))])

            # store the curry file locations in an array
            curryDataPaths.append([y for x in os.walk(curryDataLocation) for y in glob(os.path.join(x[0], '*.ceo'))])

        # store the score file locations in an array
        scoreDataPaths = [y for x in os.walk(scoreDataLocation) for y in glob(os.path.join(x[0], '*.txt'))]

        if sys.argv[1] != '.':
            try:
                subjectsToPrint = int(subjectPathsCurry.index(sys.argv[1]))
            except:
                commandlineErrorMain(sys.argv[1],'subjectsInvalid')

        if debug_main:
            print "--------------------------------------------------------"
            print "-------- Testing Main Function (File Structure) --------"
            print "--------------------------------------------------------"
            print "\n"
            if verbose:
                print "---------- Subject File Paths ----------"
                print "\n"
                print subjectPathsMax
                print "\n"

        try:
            if len(subjectPathsMax) > 1:
                # store all the subject pairs in an array
                ExperimentParams.subjectInitials = []
                for subjectPath in subjectPathsMax:
                    ExperimentParams.subjectInitials.append([str(subjectPath[0:2]),str(subjectPath[3:5])])
            else:
                ExperimentParams.subjectInitials = [str(subjects[0:2]),str(subjects[3:5])]

        except:
            commandlineErrorMain(sys.argv,'subjestsInvalid')

    else:
        commandlineErrorMain(sys.argv,'subjectsInvalid')

    if len(sys.argv) == 2:
        pass

    elif len(sys.argv) == 3:
        # already checked for main debugging and
        # printed debugging header
        if sys.argv[2] == 'main':
            pass
        # check for debugging
        elif sys.argv[2] == 'buildExperiment':
            print "----------------------------------------------------------"
            print "----------- Testing buildExperiment Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_buildExperiment = True
        elif sys.argv[2] == 'readCollFile':
            print "----------------------------------------------------------"
            print "------------- Testing readCollFile Function --------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_readCollFile = True
        elif sys.argv[2] == 'parseMaxData':
            print "----------------------------------------------------------"
            print "------------- Testing parseMaxData Function --------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_parseMaxData = True
        elif sys.argv[2] == 'removeBadTrials':
            print "----------------------------------------------------------"
            print "----------- Testing removeBadTrials Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_removeBadTrials = True
        elif sys.argv[2] == "blockToTrials":
            debug_blockToTrials = True
            print "-------------------------------------------------"
            print "--------- Testing blockToTrials Function --------"
            print "-------------------------------------------------"
            print "\n"
        elif sys.argv[-1] == '-v':
            pass
        else:
            commandlineErrorMain(sys.argv, 'functionNameInvalid')

    elif len(sys.argv) == 4:
        if sys.argv[2] == 'main':
            debug_main = True
        elif sys.argv[2] == 'buildExperiment':
            print "----------------------------------------------------------"
            print "----------- Testing buildExperiment Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_buildExperiment = True

        elif sys.argv[2] == 'readCollFile':
            print "----------------------------------------------------------"
            print "----------- Testing readCollFile Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_readCollFile = True
        elif sys.argv[2] == 'parseMaxData':
            print "----------------------------------------------------------"
            print "------------- Testing parseMaxData Function --------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_parseMaxData = True
        elif sys.argv[2] == 'removeBadTrials':
            print "----------------------------------------------------------"
            print "----------- Testing removeBadTrials Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_removeBadTrials = True
        elif sys.argv[2] == "blockToTrials":
            debug_blockToTrials = True
            print "-------------------------------------------------"
            print "--------- Testing blockToTrials Function --------"
            print "-------------------------------------------------"
            print "\n"
        else:
            commandlineErrorMain(sys.argv, 'functionNameInvalid')
        if sys.argv[-1] == "-v":
            verbose = True
        elif sys.argv[-1] == '.':
            pass
        else:
            try:
                if isinstance(int(sys.argv[3]),int):
                    pass
            except:
                commandlineErrorMain(sys.argv[3],'flagInvalid')

    elif len(sys.argv) == 5:

        if sys.argv[2] == 'main':
            debug_main = True
        elif sys.argv[2] == 'buildExperiment':
            print "----------------------------------------------------------"
            print "----------- Testing buildExperiment Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_buildExperiment = True
        elif sys.argv[2] == 'readCollFile':
            print "----------------------------------------------------------"
            print "----------- Testing readCollFile Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_readCollFile = True
        elif sys.argv[2] == 'parseMaxData':
            print "----------------------------------------------------------"
            print "------------- Testing parseMaxData Function --------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_parseMaxData = True
        elif sys.argv[2] == 'removeBadTrials':
            print "----------------------------------------------------------"
            print "----------- Testing removeBadTrials Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_removeBadTrials = True
        elif sys.argv[2] == "blockToTrials":
            debug_blockToTrials = True
            print "-------------------------------------------------"
            print "--------- Testing blockToTrials Function --------"
            print "-------------------------------------------------"
            print "\n"
        else:
            commandlineErrorMain(sys.argv, 'functionNameInvalid')
        if sys.argv[-1] == "-v":
            verbose = True
        else:
            if sys.argv[3] != '.':
                try:
                    if isinstance(int(sys.argv[3]),int):
                        pass
                except:
                    commandlineErrorMain(sys.argv[3],'flagInvalid')
            if sys.argv[4] != '.':
                try:
                    if isinstance(int(sys.argv[4]),int):
                        block_number_Print_trigger_codes = int(sys.argv[4])
                except:
                    commandlineErrorMain(sys.argv[4],'flagInvalid')

    elif len(sys.argv) == 6:

        if sys.argv[2] == 'main':
            debug_main = True
        elif sys.argv[2] == 'buildExperiment':
            print "----------------------------------------------------------"
            print "----------- Testing buildExperiment Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_buildExperiment = True
        elif sys.argv[2] == 'readCollFile':
            print "----------------------------------------------------------"
            print "----------- Testing readCollFile Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_readCollFile = True
        elif sys.argv[2] == 'parseMaxData':
            print "----------------------------------------------------------"
            print "------------- Testing parseMaxData Function --------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_parseMaxData = True
        elif sys.argv[2] == 'removeBadTrials':
            print "----------------------------------------------------------"
            print "----------- Testing removeBadTrials Function -------------"
            print "----------------------------------------------------------"
            print "\n"
            debug_removeBadTrials = True
        elif sys.argv[2] == "blockToTrials":
            debug_blockToTrials = True
            print "-------------------------------------------------"
            print "--------- Testing blockToTrials Function --------"
            print "-------------------------------------------------"
            print "\n"
        else:
            commandlineErrorMain(sys.argv, 'functionNameInvalid')
        if sys.argv[-1] == "-v":
            verbose = True
        else:
                commandlineErrorMain(sys.argv[4],'flagInvalid')
        if sys.argv[3] != '.':
            try:
                if isinstance(int(sys.argv[3]),int):
                    pass
            except:
                commandlineErrorMain(sys.argv[3],'flagInvalid')
        if sys.argv[4] != '.':
            try:
                if isinstance(int(sys.argv[4]),int):
                    block_number_Print_trigger_codes = int(sys.argv[4])
            except:
                commandlineErrorMain(sys.argv[4],'flagInvalid')
    else:
        commandlineErrorMain(sys.argv,'tooManyArguments')

    #### EXPERIMENT PARAMETERS ####
    # metronome trigger codes (TCs: 201 - 233)
    ExperimentParams.metronome_codes = arange(33) + 201
    # error trigger codes (TCs: 240 - 246)
    ExperimentParams.error_codes = arange(7) + 240
    # number of subjects in our experiment
    ExperimentParams.number_of_subjectPairs = len(subjectPathsMax)
    # blocks per subject pair
    ExperimentParams.number_of_blocks_per_subjectPair = []
    for pair in range(ExperimentParams.number_of_subjectPairs):
        ExperimentParams.number_of_blocks_per_subjectPair.append(len(curryDataPaths[pair]))

    #### DEBUG PRINT PARAMETERS ####
    # blocks for printing
    DebugPrintParams.blocks_to_print = block_number_Print_trigger_codes
    # subjects for printing
    DebugPrintParams.subjects_to_print = subjectsToPrint

    if debug_main:
        print "---------- Number of Subject Pairs in the File System ----------"
        print "\n"
        print len(subjectPathsMax)
        print "\n"
        print "---------- Number of Max Files (Single Trials) For Subject Pair: ", ExperimentParams.subjectInitials[0],"----------"
        print "\n"
        print len(maxDataPaths[0])
        print "\n"
        print "---------- Number of Curry Files (Blocks of Trials) For Subject Pair: ", ExperimentParams.subjectInitials[0],"----------"
        print "\n"
        print len(curryDataPaths[0]), " (Should be 12)"
        print "\n"
        print "---------- Number of Score Files ----------"
        print "\n"
        print len(scoreDataPaths), " (Should be 4)"
        print "\n"
        print "---------- Subject Pairs ----------"
        print "\n"
        print ExperimentParams.subjectInitials
        print "\n"
        if verbose:
            print "--------------------------------------------------------"
            print "--------- Verbose (Debug Print Options) ----------------"
            print "--------------------------------------------------------"
            print "\n"
            print "---------- Index of Subjects For Printing ----------"
            print "\n"
            print DebugPrintParams.subjects_to_print, "  print all subjects if value is '.'"
            print "\n"
            print "---------- Index of Block For Printing ----------"
            print "\n"
            print DebugPrintParams.blocks_to_print, "  print all blocks if value is '.'"
            print "\n"

    #### LETS BUILD AN EXPERIMENT ####
    # construct an experiment object, ready for analysis
    experiment = buildExperiment(subjectPathsMax,maxDataPaths, curryDataPaths, scoreDataPaths, ExperimentParams, DebugPrintParams)
