from plots.PssPlotsCreator import PssPlotsCreator
from PhysiologicalAnalysis import PhysiologicalAnalysis
from PartsSplitter import PartsSplitter
import itertools

# Adjust the baseFolder according to your folder, where your empatica episodes are
# Remember that this baseFolder has to contain empatica folders in the form of "empatica_ep_01" etc. and those folders
# contain the downloaded empatica data for a specific episode
baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"


# This method creates all plots for all the PSS data.
# the "first" parameter always signalizes to take only the first MAT.
# The "second" parameter always signalizes to take only the second MAT
# and "all" states to take all the pss data. Which is before the MAT, after first MAt and after second MAT
# Just comment out the line, if you do not want a certain plot to be created.
# IMPORTANT: The baseFolder has to contain :
# 1. PSS_BEFORE.csv for the before experiment pss data
# 2. PSS_AFTER_NO_LIGHT.csv for the experiment data after the no light experiment
# 3. PSS_AFTER_LIGHT.csv for the experiment data after the light experiment
def executePssPlotter():
    pss_plotter = PssPlotsCreator(baseFolder)
    print("Start")
    pss_plotter.createBlueLightPieChart()
    pss_plotter.createPlot("first", "stress")
    pss_plotter.createPlot("second", "stress")
    pss_plotter.createPlot("all", "stress")
    pss_plotter.createPlot("first", "concentration")
    pss_plotter.createPlot("second", "concentration")
    pss_plotter.createPlot("all", "concentration")
    pss_plotter.createPlot("first", "tension")
    pss_plotter.createPlot("second", "tension")
    pss_plotter.createPlot("all", "tension")
    pss_plotter.createAveragesPlot()
    pss_plotter.createEmotionsPlot("all")
    pss_plotter.createEmotionsPlot("first")
    pss_plotter.createEmotionsPlot("second")


# This method executes all the t-tests and prints averages.
# The
def executePhysiologicalAnalysis():
    # Bad EDA: 6,7,10, 12,13,18
    # Bad HR  -
    #epNbrs = [1, 2, 3, 4, 5, 6, 8, 9, 11, 14, 15, 16, 17]
    epNbrs = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17, 18]

    physiological_analyzer =  PhysiologicalAnalysis(baseFolder, epNbrs)
    print("HRV (RMSSD) analysis on full data\n")
    print(physiological_analyzer.getHrvRMSSD())
    print("-------------------------------\n")
    print("HRV (SDRR) analysis on full data\n")
    print(physiological_analyzer.getHRVSDRR())
    print("-------------------------------\n")
    # Analysis on Heart Rate
    print("HR Analysis\n")
    print(physiological_analyzer.getHr())
    print("-------------------------------\n")
    print("Base HR avg and Base HRV agb")
    physiological_analyzer.getHRandHRVBaseAvg()
    print("-------------------------------\n")
    print("Done")

    #unevenNbrs = [k for k in epNbrs if k % 2]
    #permutationLength = 1
    #tuplesToRemove = list(itertools.permutations(unevenNbrs, permutationLength))
    #for tuple in tuplesToRemove:
    #    if permutationLength > 1 and ((tuple[1], tuple[0]) in tuplesToRemove):
    #        tuplesToRemove.remove((tuple[1], tuple[0]))##

    #for tuple in tuplesToRemove:
    #    epNbrsTmp = epNbrs.copy()
    #    for nbr in tuple:
    #        epNbrsTmp.remove(nbr)
    #    physiological_analyzer = PhysiologicalAnalysis(baseFolder, epNbrsTmp)
    #    print(epNbrsTmp)
    #    # Analysis on EDA
    #    print("EDA Analysis\n")
    #    print(physiological_analyzer.getEDAAvgsAndTTest())
    #    print("-------------------------------\n")
    #    # Analysis on HRV
    #    print("HRV (RMSSD) analysis on full data\n")
    #    print(physiological_analyzer.getHRVRMSSDAvgsAndTTest())
    #    print("-------------------------------\n")
    #    # Analysis on Heart Rate
    #    print("HR Analysis\n")
    #    print(physiological_analyzer.getHRAvgAndTTest())
    #    print("-------------------------------\n")
        #print("-------------------------------\n")
        #print("Base HR avg and Base HRV agb")
        #physiological_analyzer.getHRandHRVBaseAvg()
        #print("-------------------------------\n")
        #print("Done")


def splitAllFiles():
    splitter = PartsSplitter(baseFolder)
    splitter.splitALlFiles()


# splitAllFiles()
#executePssPlotter()
executePhysiologicalAnalysis()
