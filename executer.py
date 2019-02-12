from plots.PssPlotsCreator import PssPlotsCreator
from PhysiologicalAnalysis import PhysiologicalAnalysis
from PartsSplitter import PartsSplitter

baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"

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

def executePhysiologicalAnalysis():
    physiological_analyzer = PhysiologicalAnalysis(baseFolder, [1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 17])
    #print(physiological_analyzer.useOnlyPartOneFromTestGetHRV())
    #print(physiological_analyzer.getEDAAvgsAndTTest())
    print(physiological_analyzer.getHRVAvgsAndTTest())
    #print(physiological_analyzer.getHRAvgAndTTest())
    print("Done")

def splitAllFiles():
    splitter = PartsSplitter(baseFolder)
    splitter.splitALlFiles()

#splitAllFiles()
executePhysiologicalAnalysis()