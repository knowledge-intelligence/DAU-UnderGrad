# =============================================================================
# %matplotlib qt
# when you want graphs in a separate window and
# 
# %matplotlib inline
# when you want an inline plot
# =============================================================================
# =============================================================================
# Go to Tools >> Preferences >> IPython console >> Graphics >> Backend:Inline, 
# change "Inline" to "Automatic", click "OK"
# =============================================================================

# %% Load Data
from SubClass.ProcSoftSensorData import *
import pandas as pd
from StaticMotionMapInfo_200901_bySST_Final import MotionNames, StaticMotionMap, CheckDataIntegrity_StaticMotionMap

data, SubjNames, _ = LoadSoftSensorData(0)
SubjName = SubjNames[0]
df_Subj = data[SubjName]
MotRepNames = [*df_Subj.keys()]  # 컨테이너 타입의 데이터를 Unpacking 할 때 (*)

# Static Motion Map - Integrity Check
CheckDataIntegrity_StaticMotionMap(StaticMotionMap)

# %% Plot Data
import sys
import numpy as np
import matplotlib.pyplot as plt


def DrawPlot(MotName):
    df_Mot = df_Subj[MotName]
    Sig_Col_Names = df_Mot.columns[1:11]  # A0 - A9
    Sig_Col_Ind = list(range(1, 11))
    N = len(df_Mot.index)
    x = np.arange(0, N, 100)

    ### Plot
    # linestyle > https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html    
    # fig = plt.figure()
    fig = plt.gcf()
    fig.clf()

    # Static Motion Map
    try:
        SampleIndex = StaticMotionMap[SubjName][MotName]
    except:
        SampleIndex = []

        # SW Position
    ret = np.where(np.diff(df_Mot['SW'] >= 1) == 1)

    # #Clear Global Variables
    # for name in dir():
    #     if not name.startswith('_'):
    #         del globals()[name]

    #del globals()[('ax0_line_l','ax0_line_r')]
    #del globals()['ax0_line_r']
    global SW_pos, SW_n, SW_index, ax0, ax1, ax2, ax0_line

    SW_pos = ret[0]
    SW_n = len(SW_pos)
    SW_index = 0

    # Plot Signals
    # Max Value form A0-A9 Except SW & Time
    # Limit SW Value (1.0) to The Max Value
    max_value = df_Mot.max()[Sig_Col_Ind].max()
    SW_Sig = df_Mot['SW'] * max_value

    """ # %% Plot1
    ax0 = plt.subplot(311)
    ax0.set_title(SubjName + '-' + MotName + '-All')
    for y in Sig_Col_Names:
        plt.plot(x, df_Mot[y][x], picker=5)
    plt.plot(x, SW_Sig[x], linestyle='dotted')

    # Draw StaticMotionSample
    for tup_mot in SampleIndex:
        plt.plot((tup_mot[1], tup_mot[1]), (0, max_value), color='b', linewidth=2, linestyle='--')
        plt.plot((tup_mot[2], tup_mot[2]), (0, max_value), color='g', linewidth=2, linestyle='--')
        plt.plot((tup_mot[3], tup_mot[3]), (0, max_value), color='r', linewidth=2, linestyle='--')
        plt.plot((tup_mot[4], tup_mot[4]), (0, max_value), color='c', linewidth=2, linestyle='--')

    ax0_line = (plt.plot((x[0], x[0]), (0, max_value), color='red', linewidth=3), \
        plt.plot((x[-1], x[-1]), (0, max_value), color='red', linewidth=3))
    plt.grid(True) """

    # %% Plot2
    #ax1 = plt.subplot(312)
    ax1 = plt.subplot(111)
    ax1.set_title(SubjName + '-' + MotName)

    for y in Sig_Col_Names:
        plt.plot(x, df_Mot[y][x], picker=5)
    #plt.plot(x, SW_Sig[x], linestyle='dotted')

    # Draw StaticMotionSample
    """ for tup_mot in SampleIndex:
        plt.plot((tup_mot[1], tup_mot[1]), (0, max_value), color='b', linewidth=2, linestyle='--')
        plt.plot((tup_mot[2], tup_mot[2]), (0, max_value), color='g', linewidth=2, linestyle='--')
        plt.plot((tup_mot[3], tup_mot[3]), (0, max_value), color='r', linewidth=2, linestyle='--')
        plt.plot((tup_mot[4], tup_mot[4]), (0, max_value), color='c', linewidth=2, linestyle='--') """
    #plt.grid(True)
    plt.grid(False)

    """ # %% Plot3
    # Plot Diff
    # Cal Diff
    # diff_val = np.diff(df_Mot[Sig_Col_Names], axis=0)
    diff_val = df_Mot[Sig_Col_Names].diff()

    # Max Value form A0-A9 Except SW & Time
    # Limit SW Value (1.0) to The Max Value
    max_value = diff_val.max().max()
    SW_Diff = df_Mot['SW'] * max_value

    ax2 = plt.subplot(313, sharex=ax1)
    ax2.set_title(SubjName + '-' + MotName + '-Diff')
    for y in Sig_Col_Names:
        plt.plot(x, diff_val[y][x].abs(), picker=5)
    plt.plot(x, SW_Diff[x], linestyle='dotted')
    plt.grid(True)  # ax.grid(color='white', linestyle='solid') """
    
    plt.tight_layout()

    fig.canvas.mpl_connect('pick_event', onpick)
    fig.canvas.mpl_connect('key_press_event', press)
    plt.show()


def SetXLim(left, right):
    #ax0_line[0][0].set_xdata((left, left))
    #ax0_line[1][0].set_xdata((right, right))
    ax1.set_xlim(left, right)
    ax1.autoscale(True, 'y')
    #ax2.set_xlim(left, right)
    #ax2.autoscale(True, 'y')
    plt.draw()


def press(event):
    global SW_index
    # print('press', event.key)
    sys.stdout.flush()
    if event.key == 'n':
        SW_index += 1
        if SW_index > SW_n: SW_index = SW_n
    elif event.key == 'p':
        SW_index -= 1
        if SW_index < 0: SW_index = 0
    elif event.key == '`':
        DrawPlot(MotRepNames[6])  # 6: 'Static 1'
    elif event.key == '1':
        DrawPlot(MotRepNames[7])  # 7: 'Static 2'
    elif event.key == '2':
        DrawPlot(MotRepNames[8])  # 8: 'Static 3'
    elif event.key == '3':
        DrawPlot(MotRepNames[9])  # 9: 'Static 4'
    elif event.key == '4':
        DrawPlot(MotRepNames[10])  # 10: 'Static 5'
    elif event.key == '5':
        DrawPlot(MotRepNames[11])  # 11: 'Static 6'
    elif event.key == '6':
        DrawPlot(MotRepNames[0])  # 0: 'Dynamic 1'
    elif event.key == '7':
        DrawPlot(MotRepNames[1])  # 1: 'Dynamic 2'
    elif event.key == '8':
        DrawPlot(MotRepNames[2])  # 2: 'Dynamic 3'
    elif event.key == '9':
        DrawPlot(MotRepNames[3])  # 3: 'Dynamic 4'
    elif event.key == '0':
        DrawPlot(MotRepNames[4])  # 4: 'Dynamic 5'
    elif event.key == '-':
        DrawPlot(MotRepNames[5])  # 5: 'Dynamic 6'

    SetXLim(SW_pos[SW_index] - 2000, SW_pos[SW_index] + 10000)


def onpick(event):
    if type(event.artist) != plt.Line2D: return True

    N = len(event.ind)
    if not N: return True

    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind[0]
    # points = tuple(zip(xdata[ind], ydata[ind]))
    points = (xdata[ind], ydata[ind])
    print('onpick points:', points)


# %% Run PlotData
MotRepName = MotRepNames[6]  # 0: 'Dynamic 1', 6: 'Static 1'
DrawPlot(MotRepName)
