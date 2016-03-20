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
from itertools import izip, chain
from inspect import currentframe, getframeinfo # We will use this to print line numbers
from os import walk
set_printoptions(threshold=inf) # don't truncate prints

class DebugPrintParams:
    """ A class to hold coding parameters to share across subjects, trials and blocks """
    pass # add attributes at runtime as needed

def validateData(maxData,curryData):
    pass

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
    print "This is some helpful info"
    print "\n"
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


def commandlineErrorBlockToTrials(args, errorType="default"):
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

def printOptionsBlockToTrials(args,numTrialsInBlock):
    #### TODO # get rid of block_number_Print_trigger_codes
    # if the user didn't specify, just print the first and last trial
    if len(args) == 3:
        numbertrials_Print_trigger_codes = 0
        block_number_Print_trigger_codes = '.'
        # return zero trials, print all blocks
        return numbertrials_Print_trigger_codes, block_number_Print_trigger_codes
    # 4 inputs
    elif len(args) == 4:
        if args[-1] == '-v':
            numbertrials_Print_trigger_codes = 0
        # if user inputs '.' we will print all the trials in
        elif args[-1] == '.':
            numbertrials_Print_trigger_codes = numTrialsInBlock - 2;
        # set the number of prints to user input if input is valid
        else:
            try:
                if isinstance(int(args[3]),int):
                    numbertrials_Print_trigger_codes = int(args[3])
            except:
                commandlineErrorBlockToTrials(args[3],"argumentInvalid")
        block_number_Print_trigger_codes = '.'
        return numbertrials_Print_trigger_codes, block_number_Print_trigger_codes
    # 5 inputs
    elif len(args) == 5:
        if args[-1] == '-v':
            block_number_Print_trigger_codes = '.'
        # if user inputs '.' we will print all the trials in
        if args[3] == '.':
            numbertrials_Print_trigger_codes = numTrialsInBlock - 2
        # set the number of prints to user input if input is valid
        else:
            try:
                if isinstance(int(args[3]),int):
                    numbertrials_Print_trigger_codes = int(args[3])
            except:
                commandlineErrorBlockToTrials(args[3],"argumentInvalid")
        if args[4] == '.':
            block_number_Print_trigger_codes = '.'
        # set the number of prints to user input if input is valid
        else:
            if args[4] != '-v':
                try:
                    if isinstance(int(args[4]),int):
                        block_number_Print_trigger_codes = int(args[4])
                except:
                    commandlineErrorBlockToTrials(args[4],"argumentInvalid")

        return numbertrials_Print_trigger_codes, block_number_Print_trigger_codes
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
                    numbertrials_Print_trigger_codes = int(args[3])
            except:
                commandlineErrorBlockToTrials(args[3],"argumentInvalid")
        # if user inputs '.' we will print all blocks
        if args[4] == '.':
            block_number_Print_trigger_codes = '.'
        # set the number of prints to user input if input is valid
        else:
            try:
                if isinstance(int(args[4]),int):
                    block_number_Print_trigger_codes = int(args[4])
            except:
                commandlineErrorBlockToTrials(args[4],"argumentInvalid")

        return numbertrials_Print_trigger_codes, block_number_Print_trigger_codes

    else:
        commandlineErrorBlockToTrials(args[3], "tooManyArguments")


if __name__ == '__main__':

    pass
