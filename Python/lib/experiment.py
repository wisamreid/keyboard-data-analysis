"""
experiment.py -- Analysis of midi keyboard data.
# ---------------------------------------------------------------------
Written By: Wisam Reid
-----------------------------------------------------------------------

Defines an Experiment Object made of Subject, TriggerCode, Block, Trial, Phrase, and Note objects

"""

class ExperimentParams:
    """ A class to hold coding parameters to share across subjects, trials and blocks """
    pass # add attributes at runtime as needed


class Experiment:
    """
    An abstract class defining the experiment
    """

    def __init__(self, subjects, blocks, score, triggerCodes):
        """Object is initialized with its subjectInitials"""
        # self.subjectInitials = subjectInitials
        self.subjects = subjects
        self.blocks = blocks
        self.score = score
        self.triggerCodes = triggerCodes

    def AnalyzeSomeExperimentData(self, data):
        """ Empty structure for within experiment data analysis """
        pass


    def readTriggerCodes(self, codes):
        """
        We will hardcode this for now, but this should take a text file in as input
        """
        pass


class Subject:
    """
    An abstract class defining handlers expected for a data file containing audio data
    """

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

    def __init__(self, trials, isSkyNet = False):
        """
        initialized with the frequency and SPL of a masker and whether or not
        it is Tonal
        """
        self.numTrials = len(trials)
        self.trials = trials
        self.isSkyNet = isSkyNet

    def AnalyzeSomeBlockData(self, data):
        """ Empty structure for within Block data analysis """
        pass


class Trial:
    """
    Defines a trial
    """

    def __init__(self, phrases):
        """
        Trial takes in an array of constituent phrases

        Argument(s):

                an array of phrases
        """

        self.phrases = phrases



class Phrase:
    """
    Defines a Phrase
    """

    def __init__(self, notes, isPreBoundary = False, isDeviant = False):
        """
        Phrase takes in an array of constituent notes
        """

        self.notes = notes
        self.isPreBoundary = isPreBoundary
        self.isDeviant = isDeviant

class Note:
    """
    Defines a note
    """

    def __init__(self, noteParams, isDeviant = False):
        """
        Assigns MDCT lines to scale factor bands based on a vector of the number
        of lines in each band
        """

        self.noteIndex = noteParams[0]
        self.IOI = noteParams[1]
        self.player = noteParams[2]
        self.midivalue = noteParams[3]
        self.velociy = noteParams[4]
        self.duration = noteParams[5]
        self.isDeviant = isDeviant

if __name__ == '__main__':

    pass
