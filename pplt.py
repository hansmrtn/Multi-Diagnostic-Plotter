"""Power Plotting Module

This module contains the functions used to plot input current, voltage, 
and power for a single data trial for the electric propulsion systems in the 
Advanced Propulsion Laboratory at the University of Washington.
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal, integrate
from scipy.signal import butter, lfilter
from scipy.stats import maxwell
from scipy.interpolate import CubicSpline, splev, splrep
from scipy import interpolate as inter
import re

from PyQt5.QtWidgets import QCheckBox

def get_channel_name(filename):

    # Pull out channel name identifier from filename.
    channel_name_match = re.search('CH[1-4]',filename)

    if channel_name_match == None:
        raise ValueError("Filename format is incorrect: %r" % filename)

    channel_name = channel_name_match.group()

    return channel_name



def get_data(name, energy_bool):
    data = {}
    os.chdir(name)
    dir = os.listdir()
    # index = 0
    # for folder in dir:
    #     folder_name_length = len(folder)
    #     if folder != '.gitignore':
    #         if folder[-4:folder_name_length] != '.txt':
    try:
        for file in dir:
            filename_length = len(file)
            file_extension = file[-4:filename_length]
            if (file_extension == '.csv'
                    or  file_extension == '.CSV'):

                channel_name = get_channel_name(file)
                all_data = pd.read_csv(file, header=None)

                df1 = all_data.iloc[:,3]
                df2 = all_data.iloc[:,4]

                # convert to numpy array
                if channel_name == 'CH1':
                    time_data = df1.values
                    voltage_data = df2.values
                elif channel_name == 'CH3':
                    current_data = df2.values
                else:
                    pass
                try:
                    data['time'] = time_data
                    data['voltage'] = voltage_data * 100 # V/V scaling factor
                    data['current'] = current_data * 2 # A/V scaling factor
                    data['power'] = data['voltage'] * data['current'] # W

                    if energy_bool:
                        data['energy'] = integrate.cumtrapz(data['power'], data['time'], initial=0) # J
                except:
                    pass
        # index += 1
    except:
        pass
    # except UnboundLocalError:
    #     message = ("Bias potentials text file could not be found:"
    #             + "CHECK DIRECTORY")
    #     raise FileError(message)
    return data


# def butter_filter(data, order, cutoff):

#     buttered = {}
#     sos = signal.butter(order, cutoff, btype='low', analog=False, output='sos')

#     correct = 1  # 0.004 # Is this value necessary?

#     for key in data.keys():
#         buttered.update({key: []})

#         for shot in data[key]:
#             V = np.sqrt(shot[:][:, 1]**2)
#             corrected = correct * signal.sosfiltfilt(sos, V)
#             buttered[key].append(corrected)

#     return buttered


# def butter_avg(buttered):

#     avg = {}

#     for key in buttered.keys():
#         avg.update({key: (np.sum(buttered[key], axis=0) / len(buttered[key]))})

#     return avg


if __name__ == 'main':
    print('Running pplt')
