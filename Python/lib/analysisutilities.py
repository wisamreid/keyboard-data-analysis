"""
analysisutilities.py -- support utilities for the analysis of midi keyboard data.
-----------------------------------------------------------------------
Written By: Wisam Reid
-----------------------------------------------------------------------
"""
import sys

def validateData(maxData,curryData):
    pass

def listOfListLengths(listoflists):
    """ Return the lengths of a list of lists """
    return [len(x) for x in listoflists]

def printHelpMenu():
    print "----------------------------------------------------------------------------------"
    print "---------------------------------- Help Menu -------------------------------------"
    print "----------------------------------------------------------------------------------"
    print "\n"
    print "This is some helpful info"
    print "\n"
    print "\n"
    sys.exit()
"-------------------------------------------------------------------------------"
"----------------------- Main: Errors and Debug Options ------------------------"
"-------------------------------------------------------------------------------"

def commandlineErrorMain(args, errorType):
    """ This is the message for commandline argument errors
        in the blockToTrials function """
    print "-----------------------------------------------------------------------------------------"
    print "------------------------------------- Input Error ---------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "----------------------------------  Type -h for help  -----------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "\n"
    if errorType == "argumentInvalid":
        print args, "is not a valid input"
        print "\n"
        print "\n"
    elif errorType == 'tooManyArguments':
        print "Too many input arguments"
        print "\n"
        print "\n"
    sys.exit()

def printOptionsMain(args,numTrialsInBlock):
    pass

"-----------------------------------------------------------------------------------------"
"----------------------- BlocksToTrials: Errors and Debug Options ------------------------"
"-----------------------------------------------------------------------------------------"

def commandlineErrorBlockToTrials(args, errorType):
    """ This is the message for commandline argument errors
        in the blockToTrials function """
    print "-----------------------------------------------------------------------------------------"
    print "------------------------------------- Input Error ---------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "----------------------------------  Type -h for help  -----------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "\n"
    if errorType == "ArgumentInvalid":
        print args, "is not a valid input"
        print "\n"
        print "\n"
    elif errorType == "tooManyArguments":
        print "Too many input arguments"
        print "\n"
        print "\n"
    sys.exit()

def printOptionsBlockToTrials(args,numTrialsInBlock):
    # if the user didn't specify, just print the first and last trial
    if len(args) == 3:
        numbertrials_Print_trigger_codes = 0
        return numbertrials_Print_trigger_codes # return zero trials
    # 4 inputs
    elif len(args) == 4:
        if args[3] == '-v':
            numbertrials_Print_trigger_codes = 0
        # if user inputs '.' we will print all the trials in
        elif args[3] == '.':
            numbertrials_Print_trigger_codes = numTrialsInBlock - 2;
        # set the number of prints to user input if input is valid
        else:
            try:
                if isinstance(int(args[3]),int):
                    numbertrials_Print_trigger_codes = int(args[3])
            except:
                commandlineErrorBlockToTrials(args[3],"argumentInvalid")
        return numbertrials_Print_trigger_codes
    # 5 inputs
    elif len(args) == 5:
        if args[3] == '-v':
            numbertrials_Print_trigger_codes = 0
        # if user inputs '.' we will print all the trials in
        elif args[3] == '.':
            numbertrials_Print_trigger_codes = numTrialsInBlock - 2;
        # set the number of prints to user input if input is valid
        else:
            try:
                if isinstance(int(args[3]),int):
                    numbertrials_Print_trigger_codes = int(args[3])
            except:
                commandlineErrorBlockToTrials(args[3],"argumentInvalid")
        return numbertrials_Print_trigger_codes
    else:
        commandlineErrorBlockToTrials(args[3], "tooManyArguments")


if __name__ == '__main__':

    pass
