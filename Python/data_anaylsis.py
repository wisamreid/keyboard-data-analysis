"""
audiofile.py -- Analysis of midi keyboard data.
-----------------------------------------------------------------------
Written By: Wisam Reid
-----------------------------------------------------------------------
"""


class ExperimentParams:
    """ A class to hold coding parameters to share across subjects, trials and blocks """
    pass # will just add attributes at runtime as needed

class Subject:
    """An abstract class defining handlers expected for a data file containing audio data"""

    def __init__(self, subjectInitials):
        """Object is initialized with its subjectInitials"""
        self.subjectInitials = subjectInitials


    def AnalyzeSomeSubjectData(self, data):
        """ Empty structure for within subject data analysis """
        pass

class Block:
    """
    A class to hold parameters to share across subjects and trials
    """

    def __init__(self, score, trials, isSkyNet = False):
        """
        initialized with the frequency and SPL of a masker and whether or not
        it is Tonal
        """
        self.score = score
        self.numTrials = len(trials)
        self.trials = trials
        self.isSkyNet = isSkyNet

    def AnalyzeSomeBlockData(self, data):
        """ Empty structure for within Block data analysis """
        pass

class Trial:
    """
    Defines a current trial
    """

    def __init__(self, subjectInitials, trialNumber):
        """
        Assigns MDCT lines to scale factor bands based on a vector of the number
        of lines in each band
        """

        self.nSubjects = len(subjectInitials)
        self.trialNumber = trialNumber


if __name__ == '__main__':

    print "I am running"

    pass
