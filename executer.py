from plots.PssPlotsCreator import PssPlotsCreator
from PhysiologicalAnalysis import PhysiologicalAnalysis
from PartsSplitter import PartsSplitter

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


#This method executes all the t-tests and prints averages.
# The
def executePhysiologicalAnalysis():
    physiological_analyzer = PhysiologicalAnalysis(baseFolder, [1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 17])
    print("Anova on HRV data")
    print (physiological_analyzer.executeAnovaOnHrv())
    print("-------------------------------\n")
    # This method executes the ttest only on the first part of the experiment (FIRST MAT)
    print("HRV for only first MAT\n")
    print(physiological_analyzer.useOnlyPartOneFromTestGetHRV())
    print("-------------------------------\n")
    # Analysis on EDA
    print("EDA Analysis\n")
    print(physiological_analyzer.getEDAAvgsAndTTest())
    print("-------------------------------\n")
    # Analysis on HRV
    print("HRV analysis on full data\n")
    print(physiological_analyzer.getHRVAvgsAndTTest())
    print("-------------------------------\n")
    # Analysis on Heart Rate
    print("HR Analysis\n")
    print(physiological_analyzer.getHRAvgAndTTest())
    print("-------------------------------\n")
    print("Done")

def splitAllFiles():
    splitter = PartsSplitter(baseFolder)
    splitter.splitALlFiles()

#splitAllFiles()
#executePssPlotter()
executePhysiologicalAnalysis()