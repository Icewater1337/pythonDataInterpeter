from plots.PssPlotsCreator import PssPlotsCreator

baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"


pss_plotter = PssPlotsCreator(baseFolder)
print("Start")
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
