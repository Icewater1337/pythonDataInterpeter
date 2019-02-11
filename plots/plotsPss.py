import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

baseFolder = "C:/Users/Icewater/Google Drive/uni/Informatik/MasterThesis/data/"

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


def createEmotionsPlot():
    word_list_before = get_word_list(before_df)
    word_list_after_no_light = get_word_list(after_no_light_df)
    word_list_after_light = get_word_list(after_blue_light_df)

    all_emotions = sorted(
        ['tense', 'stressed', 'excited', 'calm', 'alert', 'depressed', 'sad', 'contented', 'serene', 'bored', 'nervous',
         'happy', 'relaxed', 'upset', 'elated'])

    count_before_labels, counter_before_values = get_full_list_of_frequencies(all_emotions, Counter(word_list_before))
    count_after_no_light_labels, count_after_no_light_values = get_full_list_of_frequencies(all_emotions, Counter(word_list_after_no_light))
    count_after_light_labels, count_after_light_values = get_full_list_of_frequencies(all_emotions, Counter(word_list_after_light))


    ind = np.arange(0, 2 * len(all_emotions), 2)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width, counter_before_values, width,
                    color='Grey', label='Before')
    rects2 = ax.bar(ind, count_after_no_light_values, width,
                    color='Red', label='After No light')
    rects3 = ax.bar(ind + width, count_after_light_values, width,
                    color='Blue', label='After blue light')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('#Of people with that score')
    ax.set_title('Stress scores comparison for the three parts')
    ax.set_xticks(ind)
    ax.set_xticklabels(all_emotions, rotation="vertical")
    ax.legend()

    plt.savefig(baseFolder + "emotions.png", bbox_inches="tight")


def createStressPlot():
    stress_before = fill_with_zero(np.bincount(np.asarray(before_df['stress']).astype(int)),10)
    stress_after_no = fill_with_zero(np.bincount(np.asarray(after_no_light_df['stress']).astype(int)),10)
    stress_after_blue = fill_with_zero(np.bincount(np.asarray(after_blue_light_df['stress']).astype(int)),10)

    y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    ind = np.arange(0, 2 * len(y), 2)  # the x locations for the groups
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width, stress_before, width,
                    color='Grey', label='Before')
    rects2 = ax.bar(ind, stress_after_no, width,
                    color='Red', label='After No light')
    rects3 = ax.bar(ind + width, stress_after_blue, width,
                    color='Blue', label='After blue light')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('#Of people with that score')
    ax.set_title('Stress scores comparison for the three parts')
    ax.set_xticks(ind)
    ax.set_xticklabels(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
    ax.legend()

    plt.savefig(baseFolder + "stress.png")


def createTensionPlot():
    y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    width = 0.35  # the width of the bars

    ind = np.arange(0, 2 * len(y), 2)
    tension_before = fill_with_zero(np.bincount(np.asarray(before_df['tension']).astype(int)),10)
    tension_after_no = fill_with_zero(np.bincount(np.asarray(after_no_light_df['tension']).astype(int)),10)
    tension_after_blue = fill_with_zero(np.bincount(np.asarray(after_blue_light_df['tension']).astype(int)),10)

    # create plot for tension


    fig1, ax1 = plt.subplots()
    tension_rects1 = ax1.bar(ind - width, tension_before, width,
                             color='Grey', label='Before')
    tension_rects2 = ax1.bar(ind, tension_after_no, width,
                             color='Red', label='After No light')
    tension_rects3 = ax1.bar(ind + width, tension_after_blue, width,
                             color='Blue', label='After blue light')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax1.set_ylabel('#Of people with that score')
    ax1.set_title('Tension scores comparison for the three parts')
    ax1.set_xticks(ind)
    ax1.set_xticklabels(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
    ax1.legend()

    plt.savefig(baseFolder + "tension.png")


def createConcentrationPlot():
    y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    ind = np.arange(0, 2 * len(y), 2)

    width = 0.35  # the width of the bars

    concentration_before = fill_with_zero(np.bincount(np.asarray(before_df['concentration']).astype(int)),10)
    concentration_after_no = fill_with_zero(np.bincount(np.asarray(after_no_light_df['concentration']).astype(int)),10)
    concentration_after_blue = fill_with_zero(np.bincount(np.asarray(after_blue_light_df['concentration']).astype(int)),10)

    # crete concentration plot
    fig2, ax2 = plt.subplots()
    concentration_rects1 = ax2.bar(ind - width, concentration_before, width,
                                   color='Grey', label='Before')
    concentration_rects2 = ax2.bar(ind, concentration_after_no, width,
                                   color='Red', label='After No light')
    concentration_rects3 = ax2.bar(ind + width, concentration_after_blue, width,
                                   color='Blue', label='After blue light')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax2.set_ylabel('#Of people with that score')
    ax2.set_title('Concentration scores comparison for the three parts')
    ax2.set_xticks(ind)
    ax2.set_xticklabels(('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
    ax2.legend()

    plt.savefig(baseFolder + "concentration.png")


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

createEmotionsPlot()

#createAveragesPlot()
#createConcentrationPlot()
#createStressPlot()
#createTensionPlot()
