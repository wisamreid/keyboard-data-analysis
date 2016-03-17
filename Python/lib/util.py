"""
util.py -- support utilities for the analysis of midi keyboard data.
-----------------------------------------------------------------------
Written By: Wisam Reid
-----------------------------------------------------------------------
"""
import sys

def validateData(maxData,curryData):


    return 0


"-----------------------------------------------------------------------------------------"
"----------------------- BlocksToTrials: Errors and Debug Options ------------------------"
"-----------------------------------------------------------------------------------------"

def commandlineErrorBlockToTrials(args):

    print "-----------------------------------------------------------------------------------------"
    print "------------------------------------- Input Error ---------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "----------------------------------  Type -h for help  -----------------------------------"
    print "-----------------------------------------------------------------------------------------"
    print "\n"
    print args, "is not a valid input"
    sys.exit()

def printOptionsBlockToTrials(args,numTrialsInBlock):
    # if the user didn't specify, just print the first and last trial
    if len(args) == 4:
        numbertrials_Print_trigger_codes = 0
    # if user inputs '.' we will print all the trials in
    elif args[4] == '.':
        numbertrials_Print_trigger_codes = numTrialsInBlock - 2;
    # set the number of prints to user input if input is valid
    else:
        try:
            if isinstance(int(args[4]),int):
                numbertrials_Print_trigger_codes = int(args[4])
        except:
            commandlineErrorBlockToTrials(args[4])

    return numbertrials_Print_trigger_codes

if __name__ == '__main__':

    pass
