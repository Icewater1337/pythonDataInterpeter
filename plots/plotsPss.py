import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


# USAGE: Set the base folder to the folder that contains the PSS data.
# The folder needs to contain The following files:
# 1. PSS_BEFORE.csv for the before experiment pss data
# 2. PSS_AFTER_NO_LIGHT.csv for the experiment data after the no light experiment
# 3. PSS_AFTER_LIGHT.csv for the experiment data after the light experiment
#############
# After this you can chose what plots to create in the main method.
baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"

#### DO NOT CHANGE THE FOLLOWING ############
colnames = ['time', 'participant', 'stress', 'tension', 'concentration', 'emotions']
colnames_blue = ['time', 'participant', 'stress', 'tension', 'concentration', 'calming', 'helpful', 'fav_color',
                 'fav_music', 'emotions', ]

before_df = pd.read_csv(baseFolder + "PSS_BEFORE.csv", delimiter=';', header=0, names=colnames)
before_df = before_df.dropna(0, how='all')

after_no_light_df = pd.read_csv(baseFolder + "PSS_AFTER_NO_LIGHT.csv", delimiter=';', header=0, names=colnames)
after_no_light_df = after_no_light_df.dropna(0, how='all')

after_blue_light_df = pd.read_csv(baseFolder + "PSS_AFTER_LIGHT.csv", delimiter=';', header=0, names=colnames_blue)
after_blue_light_df = after_blue_light_df.dropna(0, how='all')


# Create count tables

def fill_with_zero(array, maxNbr):
    last_index = len(array) - 1

    if last_index <= maxNbr:
        array = np.append(array, np.zeros(maxNbr - last_index))

    return np.delete(array, (0), axis=0)


def get_word_list(df):
    ret_list = []
    [ret_list.extend(i.split(",")) for i in df['emotions']]
    return [x.strip() for x in ret_list]


def get_full_list_of_frequencies(all_emotions, counter):
    ret_dict = {}
    for key in all_emotions:
        ret_dict[key] = counter[key]

    return ret_dict.keys(), ret_dict.values()

# Creates the plot of the emotions. Takes one argument
# 1. Subset: is either first, second or all. First only takes the first MAT task and second only from the second. All takes all.
def createEmotionsPlot(subset):
    adjusted_after_blue_light_df, adjusted_after_no_light_df = getSubsetOfDf(subset)

    word_list_before = get_word_list(before_df)
    word_list_after_no_light = get_word_list(adjusted_after_no_light_df)
    word_list_after_light = get_word_list(adjusted_after_blue_light_df)

    all_emotions = sorted(
        ['tense', 'stressed', 'excited', 'calm', 'alert', 'depressed', 'sad', 'contented', 'serene', 'bored', 'nervous',
         'happy', 'relaxed', 'upset', 'elated'])

    count_before_labels, counter_before_values = get_full_list_of_frequencies(all_emotions, Counter(word_list_before))
    count_after_no_light_labels, count_after_no_light_values = get_full_list_of_frequencies(all_emotions, Counter(
        word_list_after_no_light))
    count_after_light_labels, count_after_light_values = get_full_list_of_frequencies(all_emotions,
                                                                                      Counter(word_list_after_light))

    ind = np.arange(0, 2 * len(all_emotions), 2)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    if subset == "all":
        rects1 = ax.bar(ind - width, counter_before_values, width,
                        color='Grey', label='Before')
        rects2 = ax.bar(ind, count_after_no_light_values, width,
                        color='Red', label='After No light')
        rects3 = ax.bar(ind + width, count_after_light_values, width,
                        color='Blue', label='After blue light')
    if subset == "first" or subset == "second":
        rects2 = ax.bar(ind - width / 2, count_after_no_light_values, width,
                        color='Red', label='After no light')
        rects3 = ax.bar(ind + width / 2, count_after_light_values, width,
                        color='Blue', label='After blue light')



    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('#Of people with that score')
    if subset == "all":
        ax.set_title('Emotions scores comparison for the three parts')
    elif subset =="first":
        ax.set_title('Emotions scores comparison for only the first MAT')
    elif subset == "second":
        ax.set_title('Emotions scores comparison for only the second MAT')
    ax.set_xticks(ind)
    ax.set_xticklabels(all_emotions, rotation="vertical")
    ax.legend()

    plt.savefig(baseFolder + subset + "emotions.png", bbox_inches="tight")


#Creates the different plots. To create a stress, tension or concentration plot supply the two arguments
# 1. sequence: Can either be first, second or all. first if only the first MAT part is wanted etc.
# 2. Type: The type can be stress, concentration or tension. Creates an according plot
#
def createPlot(subset, type):
    if type != "stress" and type != "tension" and type != "concentration":
        raise ValueError('Variable type has to be stress, tension or concentration. Yours was: ' + type)
    if subset != "first" and subset != "second" and subset != "all":
        raise ValueError('Variable subset has to be first, second or all. Yours was: ' + subset)
    adjusted_after_light_df, adjusted_after_no_light_df = getSubsetOfDf(subset)

    before = fill_with_zero(np.bincount(np.asarray(before_df[type]).astype(int)), 10)
    after_no = fill_with_zero(np.bincount(np.asarray(adjusted_after_no_light_df[type]).astype(int)), 10)
    after_blue = fill_with_zero(np.bincount(np.asarray(adjusted_after_light_df[type]).astype(int)), 10)

    y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    ind = np.arange(0, 2 * len(y), 2)  # the x locations for the groups
    width = 0.5  # the width of the bars

    fig, ax = plt.subplots()
    if subset == "all":
        rects1 = ax.bar(ind - width, before, width,
                        color='Grey', label='Before')
        rects2 = ax.bar(ind, after_no, width,
                        color='Red', label='After no light')
        rects3 = ax.bar(ind + width, after_blue, width,
                        color='Blue', label='After blue light')
    if subset == "first" or subset == "second":
        rects2 = ax.bar(ind - width / 2, after_no, width,
                        color='Red', label='After no light')
        rects3 = ax.bar(ind + width / 2, after_blue, width,
                        color='Blue', label='After blue light')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('#Of people with that score')
    if subset == "all":
        ax.set_title(type + ' scores comparison of all experiment data')
    elif subset == "first":
        ax.set_title(type + ' scores comparison of only the first MAT')
    elif subset == "second":
        ax.set_title(type + ' scores comparison of only the second MAT')

    ax.set_xticks(ind)
    ax.set_xticklabels(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
    ax.legend()

    plt.savefig(baseFolder + subset + type + ".png")


def getSubsetOfDf(subset):
    if subset == "first":
        adjusted_after_no_light_df = after_no_light_df.loc[after_no_light_df['participant'].astype(int) % 2 == 1]
        adjusted_after_light_df = after_blue_light_df.loc[after_blue_light_df['participant'].astype(int) % 2 == 0]
    elif subset == "second":
        adjusted_after_no_light_df = after_no_light_df.loc[after_no_light_df['participant'].astype(int) % 2 == 0]
        adjusted_after_light_df = after_blue_light_df.loc[after_blue_light_df['participant'].astype(int) % 2 == 1]
    else:
        adjusted_after_no_light_df = after_no_light_df
        adjusted_after_light_df = after_blue_light_df
    return adjusted_after_light_df, adjusted_after_no_light_df


#Creates a plot of all experiment data and plots the three averages
def createAveragesPlot():
    # Create averages plot
    zz = [1, 2, 3]

    ind = np.arange(0, 2 * len(zz), 2)  # the x locations for the groups
    width = 0.5  # the width of the bars

    avgs_before = [np.average(before_df['stress']), np.average(before_df['tension']),
                   np.average(before_df['concentration'])]
    avgs_after_no = [np.average(after_no_light_df['stress']), np.average(after_no_light_df['tension']),
                     np.average(after_no_light_df['concentration'])]
    avgs_after_blue = [np.average(after_blue_light_df['stress']), np.average(after_blue_light_df['tension']),
                       np.average(after_blue_light_df['concentration'])]

    fig_avg, ax_avg = plt.subplots()
    avg_rects1 = ax_avg.bar(ind - width, avgs_before, width,
                            color='Grey', label='Before')
    avg_rects2 = ax_avg.bar(ind, avgs_after_no, width,
                            color='Red', label='After No light')
    avg_rects3 = ax_avg.bar(ind + width, avgs_after_blue, width,
                            color='Blue', label='After blue light')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax_avg.set_ylabel('Average score over all participants')
    ax_avg.set_title('Average scores for stress, tension and concentration')
    ax_avg.set_xticks(ind)
    ax_avg.set_xticklabels(('Stress', 'Tension', 'Concentration'))
    ax_avg.legend()

    plt.savefig(baseFolder + "averagePlot.png")  # Preload things



def main():
    print("Start")
    createPlot("first", "stress")
    createPlot("second", "stress")
    createPlot("all", "stress")
    createPlot("first", "concentration")
    createPlot("second", "concentration")
    createPlot("all", "concentration")
    createPlot("first", "tension")
    createPlot("second", "tension")
    createPlot("all", "tension")
    createAveragesPlot()
    createEmotionsPlot("all")
    createEmotionsPlot("first")
    createEmotionsPlot("second")


if __name__ == '__main__':
    main()


