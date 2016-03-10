# keyboard-data-analysis

Author: Wisam Reid

An attempt at a modular, flexible, and scalable environment for keyboard data analysis

##### This is a work in progress

-----

# Running the code
## Command line
run with 'python analysis.py << Subject's Initials >>'

# Code Structure

The **__main__** function at the bottom of analysis.py fetches data from the file system
by subject (Chosen at the command line)

It then calls the **buildExperiment** function passing in string arrays containing file paths to the data needed to run the experiment.  

The **buildExperiment** function constructs an experiment object that is informed of
the relevant data and is ready for analysis

-----

# Development

Search **TODO** in the source code files


| TODO: | Code Location              | Called                     | Task                                                             |
| ----- |:--------------------------:|:--------------------------:| ----------------------------------------------------------------:|
| 1.    | [analysis.parseScore]      | [analysis.buildExperiment] | fill in the scoreParse function                                  |
| 2.    | [analysis.blocksToTrials]  | [analysis.buildExperiment] | break raw curry data into trials (currently divided into blocks) |                                                         | 3.    | [analysis.removeBadTrials] | [analysis.buildExperiment] | throw out bad trials                                             |
| 4.    | [experiment.py]            | [analysis.main]            | call the experiment constructor to begin the building process    |


## Miscellaneous Notes

While some error checking is done at the command line, but this could use improvement if we want to add features


The experiement constructor will:

1. build block objects
2. build trial objects
3. build phrase objects
4. create note objects
5. create subject objects
⋅⋅ 1. assign block, trial, phrase objects

# Dependencies
