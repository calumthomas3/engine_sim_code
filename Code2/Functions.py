import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point


class ImportFunctions:
    # A Function which imports the gear change data from a .csv file
    @staticmethod
    def import_gear_change(filepath):
        ulines_dir = {}
        dlines_dir = {}
        xls = pd.ExcelFile(filepath)
        sheets = xls.sheet_names
        upshifts = sheets[0:int(len(sheets)/2)]
        downshifts = sheets[int(len(sheets)/2):int(len(sheets))]
        gear = 2
        for upshift in upshifts:
            ulines_dir[str(gear)] = pd.read_excel(xls, upshift)
            gear = gear + 1
        gear = 1
        for downshift in downshifts:
            dlines_dir[str(gear)] = pd.read_excel(xls, downshift)
            gear = gear + 1
        print(ulines_dir)
        print(dlines_dir)
        return ulines_dir, dlines_dir

    # A Function which imports the performance curve provided by Patrimony EV
    @staticmethod
    def import_p_curve(input_value, MASS):  # EV Performance Curve

        input_value_mph = input_value / 1.6
        # This is a curve of x-axis speed in mph and y-axis max acceleration available in Gs
        # Performance curve with reduction gear:
        points = [(0, 0.53), (32.68, 0.513), (33.27, 0.5), (41, 0.4), (52.68, 0.3), (71.71, 0.2), (101, 0.1),
                  (137, 0.0)]

        # Performance curve without reduction gear:
        # points = [(0, 0.247), (71.71, 0.2), (101, 0.1), (137, 0.0)]

        # Split the points into separate lists for x and y values
        x, y = zip(*points)

        # Fit a curve to the data
        coefficients = np.polyfit(x, y, 3)
        polynomial = np.poly1d(coefficients)

        # Check if the intercept is within the range of the x values
        if min(x) <= input_value_mph <= max(x):
            # Find the y-intercept and convert to thrust in N
            thrust = polynomial(input_value_mph) * 9.81 * MASS
            return thrust
        else:
            return None


class GearFunctions:
    # A Function to create the gear change graph
    @staticmethod
    def gear_change_graph(ulines_dir, dlines_dir):
        # Loop to fill Upshift and Downshift
        graphdata = list()
        for i in range(1, len(ulines_dir) + 1):
            for j in range(ulines_dir[str(i + 1)].shape[0] - 1):
                graphdata.append({'line': ((ulines_dir[str(i + 1)].loc[j][0], ulines_dir[str(i + 1)].loc[j][1]),
                                           (
                                           ulines_dir[str(i + 1)].loc[j + 1][0], ulines_dir[str(i + 1)].loc[j + 1][1])),
                                  'rule': i + 1,
                                  'direction': 0})

        for i in range(1, len(dlines_dir) + 1):
            for j in range(dlines_dir[str(i)].shape[0] - 1):
                graphdata.append({'line': ((dlines_dir[str(i)].loc[j][0], dlines_dir[str(i)].loc[j][1]),
                                           (dlines_dir[str(i)].loc[j + 1][0], dlines_dir[str(i)].loc[j + 1][1])),
                                  'rule': i,
                                  'direction': 1})

        # Create figure and axes
        fig, ax = plt.subplots()

        # Loop through graphData and plot the transmission lines
        for i, data in enumerate(graphdata):
            line = data['line']
            direction = data['direction']

            # Set linestyle to dotted if direction is 1, otherwise solid
            linestyle = ':' if direction == 1 else '-'
            label = f"Downshift Lines {i}" if direction == 1 else f"Upshift Lines {i}"

            # Unpack start and end points of line
            x_start, y_start = line[0]
            x_end, y_end = line[1]

            # Plot the line with appropriate linestyle
            ax.plot([x_start, x_end], [y_start, y_end], linestyle=linestyle, label=label)
            # plt.close()
        return graphdata

def live_plotter(x_data, y_data, ulines_dir, dlines_dir, line1, identifier=''):
    if line1 == []:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        gearlines = GearFunctions.gear_change_graph(ulines_dir, dlines_dir)
        line1, = ax.plot(x_data, y_data, '-o', alpha=0.8)
        # update plot label/title
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()

    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_data(x_data, y_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y_data) <= line1.axes.get_ylim()[0] or np.max(y_data) >= line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y_data) - np.std(y_data), np.max(y_data) + np.std(y_data)])
