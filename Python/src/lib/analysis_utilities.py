"""
analysisutilities.py -- support utilities for the analysis of midi keyboard data.
-----------------------------------------------------------------------
Written By: Wisam Reid
-----------------------------------------------------------------------
"""
from numpy import *
from time import *
from ast import *
import sys
import os
from glob import glob
import itertools
from itertools import groupby
# from itertools import izip, chain
from inspect import currentframe, getframeinfo # We will use this to print line numbers
from os import walk
set_printoptions(threshold=inf) # don't truncate prints

class DebugPrintParams:
    """ A class to hold coding parameters to share across subjects, trials and blocks """
    pass # add attributes at runtime as needed

def validateData(maxData,curryData):
    pass

def findIndices(searchList,elem, removeEmptyList=True):
    """ Return array of indices for a list of values"""
    indices = [[i for i, x in enumerate(searchList) if x == e] for e in elem]
    if removeEmptyList:
        indices = filter(None,indices) # remove empty lists
    # indices = reduce(add, map(lambda x: list(x), [i for i in indices]))
    # indices = itertools.chain(indices)
    return indices

def listOfListLengths(listoflists):
    """ Return the lengths of a list of lists """
    return [len(x) for x in listoflists]

def partitionList(alist, indices):
    """
    Takes a list and partitions it based on a list of indexes

        Argument(s):

                alist: list to partition
                indices: indices to partition by

        Return:

                listOfLists: (array of arrays) list partitians
    """
    debug = False

    listOfLists = []
    for i in range(len(indices)):

        if i+1 < len(indices):
            # cut ranges
            listOfLists.append(alist[indices[i]:indices[i+1]])
            if debug:
                print listOfLists[i]
        else:
            # grab the rest of the list
            listOfLists.append(alist[indices[i]:])

    if debug:
        print "---- Testing partitionList ----"
        print "len(listOfLists) ",len(listOfLists)
        print "First Trial: ", listOfLists[0]
        print "Last Trial: ", listOfLists[-1]
        print "\n"

    return listOfLists

def printHelpMenu():
    print "----------------------------------------------------------------------------------"
    print "---------------------------------- Help Menu -------------------------------------"
    print "----------------------------------------------------------------------------------"
    print "\n"
    print "------------------------------------------------------------------"
    print "-------------------- If Testing a Function: ----------------------"
    print "------------------------------------------------------------------"
    print "\n"
    print "@ Commandline type:"
    print ">> python analysis.py Subjects nameOfFunctionToDebug"
    print "\n"
    print "Subjects: A subject pair by intials"
    print "\n"
    print "          (formatted as: 'XX_YY'): print subject pair, omit others"
    print "          ('.'): print all subjects"
    print "\n"
    print "-------------------------------------------------------"
    print "---------- blockToTrials Printing Options: ------------"
    print "-------------------------------------------------------"
    print "\n"
    print "@ Commandline type:"
    print ">> python analysis.py Subjects blockToTrials Block(s) Trial(s)"
    print "\n"
    print "Subjects: A subject pair by intials"
    print "\n"
    print "          (formatted as: 'XX_YY'): print subject pair, omit others"
    print "          ('.'): print all subjects"
    print "\n"
    print "Block(s): The first and last blocks in a block are printed by default"
    print "\n"
    print "          (Int): number of block to print"
    print "          ('.'): print all blocks for a subject"
    print "\n"
    print "Trial(s): All trials are printed by default"
    print "\n"
    print "          (Int): number of trial to print (all others will be omitted)"
    print "          ('.'): print all trials in a block"
    print "\n"
    print "\n"
    print "------------------------------"
    print "---------- Flags: ------------"
    print "------------------------------"
    print "\n"
    print "@ Commandline type:"
    print "-v: at the end of any print configuration for verbose printing"
    print "\n"
    print "Example: "
    print ">> python analysis.py nameOfFunctionToDebug -v"
    print "\n"
    print "@ Commandline type:"
    print "-h: print help menu"
    print "\n"
    print "Example: "
    print ">> python analysis.py -h"
    print "\n"
    sys.exit()

"---------------------------------------------------------"
"------- buildExperiment: Errors and Debug Options -------"
"---------------------------------------------------------"

def commandlineErrorBuildExperiment(args, errorType='default'):
    """ This is the message for commandline argument errors
        in the buildExperiment function """
    print "-----------------------------------------------------------------------------------------"
    print "------------------------------------- Input Error ---------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "----------------------------------  Type -h for help  -----------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "\n"
    print "Commandline Error Thrown by: buildExperiment function: "
    print "\n"
    if errorType == 'default':
        pass
    if errorType == 'fileStructure':
        print "File structure is not valid"
        print "\n"
        print "\n"
    if errorType == 'argumentInvalid':
        print args, "is not a valid input"
        print "\n"
        print "\n"
    elif errorType == 'tooManyArguments':
        print "Too many input arguments"
        print "\n"
        print "\n"
    elif errorType == 'functionNameInvalid':
        print "Invalid Function Name: ", args[2]
        print "\n"
        print "\n"
    elif errorType == 'flagInvalid':
        print "Error: Unknown Flag"
        print "\n"
        print "\n"
    elif errorType == 'subjestsInvalid':
        print "Error: Please enter a subject pair by intials [formatted as: 'XX_YY']"
        print "       or enter '.' to build with all subjects'"
        print "\n"
        print "\n"
    sys.exit()

def printOptionsBuildExperiment(args,numTrialsInBlock):
    pass

"---------------------------------------------------------"
"------------- Main: Errors and Debug Options ------------"
"---------------------------------------------------------"

def commandlineErrorMain(args, errorType='default'):
    """ This is the message for commandline argument errors
        in the blockToTrials function """
    print "-----------------------------------------------------------------------------------------"
    print "------------------------------------- Input Error ---------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "----------------------------------  Type -h for help  -----------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "\n"
    print "Commandline Error Thrown by: main function: "
    print "\n"
    if errorType == 'default':
        pass
    elif errorType == 'fileStructure':
        print "File structure is not valid"
        print "\n"
        print "\n"
    elif errorType == 'argumentInvalid':
        print args, "is not a valid input"
        print "\n"
        print "\n"
    elif errorType == 'tooManyArguments':
        print "Too many input arguments"
        print "\n"
        print "\n"
    elif errorType == 'functionNameInvalid':
        print "Invalid Function Name: ", args[2]
        print "\n"
        print "\n"
    elif errorType == 'flagInvalid':
        print "Error: Unknown Flag ", args
        print "\n"
        print "\n"
    elif errorType == 'subjectsInvalid':
        print "Error: Please enter a subject pair by intials [formatted as: 'XX_YY']"
        print "       or enter '.' to build with all subjects'"
        print "\n"
        print "\n"
    sys.exit()

def printOptionsMain(args,numTrialsInBlock):
    pass

"---------------------------------------------------------"
"-------- BlocksToTrials: Errors and Debug Options -------"
"---------------------------------------------------------"


def commandlineErrorCurryBlockToTrials(args, errorType="default"):
    """ This is the message for commandline argument errors
        in the blockToTrials function """
    print "-----------------------------------------------------------------------------------------"
    print "------------------------------------- Input Error ---------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "----------------------------------  Type -h for help  -----------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "\n"
    print "Commandline Error Thrown by: blockToTrials function: "
    print "\n"
    if errorType == "default":
        pass
    if errorType == "argumentInvalid":
        print args, "is not a valid input"
        print "\n"
        print "\n"
    if errorType == "tooManyArguments":
        print "Too many input arguments"
        print "\n"
        print "\n"
    sys.exit()

def printOptionsCurryBlockToTrials(args, numTrialsInBlock, DebugPrintParams):
    #### TODO # get rid of block_number_Print_trigger_codes
    # if the user didn't specify, just print the first and last trial
    if len(args) == 3:
        trialsToPrint = 0
        blocksToPrint = '.'
        # return zero trials, print all blocks
        return blocksToPrint, trialsToPrint
    # 4 inputs
    elif len(args) == 4:
        if args[-1] == '-v':
            trialsToPrint = 0
        # if user inputs '.' we will print all the trials in
        elif args[-1] == '.':
            trialsToPrint = numTrialsInBlock - 2;
        # set the number of prints to user input if input is valid
        else:
            try:
                if isinstance(int(args[3]),int):
                    trialsToPrint = int(args[3])
            except:
                commandlineErrorCurryBlockToTrials(args[3],"argumentInvalid")
        blocksToPrint = DebugPrintParams.blocks_to_print
        return blocksToPrint, trialsToPrint
    # 5 inputs
    elif len(args) == 5:
        if args[-1] == '-v':
            blocksToPrint = '.'
        # if user inputs '.' we will print all the trials in
        if args[3] == '.':
            trialsToPrint = numTrialsInBlock - 2
        # set the number of prints to user input if input is valid
        else:
            try:
                if isinstance(int(args[3]),int):
                    trialsToPrint = int(args[3])
            except:
                commandlineErrorCurryBlockToTrials(args[3],"argumentInvalid")
        if args[4] == '.':
            blocksToPrint = '.'
        # set the number of prints to user input if input is valid
        else:
            if args[4] != '-v':
                try:
                    if isinstance(int(args[4]),int):
                        blocksToPrint = int(args[4])
                except:
                    commandlineErrorCurryBlockToTrials(args[4],"argumentInvalid")

        return blocksToPrint, trialsToPrint
    # 6 inputs
    elif len(args) == 6:
        if args[3] == '-v':
            pass
        # if user inputs '.' we will print all trials
        if args[3] == '.':
            numbertrials_Print_trigger_codes = numTrialsInBlock - 2
        # set the number of prints to user input if input is valid
        else:
            try:
                if isinstance(int(args[3]),int):
                    trialsToPrint = int(args[3])
            except:
                commandlineErrorCurryBlockToTrials(args[3],"argumentInvalid")
        # if user inputs '.' we will print all blocks
        if args[4] == '.':
            blocksToPrint = '.'
        # set the number of prints to user input if input is valid
        else:
            try:
                if isinstance(int(args[4]),int):
                    blocksToPrint = int(args[4])
            except:
                commandlineErrorCurryBlockToTrials(args[4],"argumentInvalid")

        return blocksToPrint, trialsToPrint

    else:
        commandlineErrorCurryBlockToTrials(args[3], "tooManyArguments")


if __name__ == '__main__':

    pass
