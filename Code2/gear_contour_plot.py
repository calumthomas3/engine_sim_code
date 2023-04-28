# Create the 3D plot for reference by the input throttle voltage and speed voltage
import numpy as np
import matplotlib.pyplot as plt


def find_rpm(min_rpm, max_rpm, maxspeed, downshift_dir, upshift_dir):
    # create x-y points to be used in heatmap
    # Create example dataset
    # kmph

    # Need to import upshift_dir
    # Need to import downshift_dir

    # Set up gear dicitonary
    gears = {}

    # Find number of gears
    no_of_gears = len(upshift_dir) + 1
    print(str(no_of_gears) + " gears found")

    # For importing the gear lines from the excel input
    for i in range(1, no_of_gears + 1):
        if i == 1:
            gears[str(i) + " up"] = np.array(upshift_dir[str(i+1)])
            gears[str(i) + " down"] = [[0, 0], [0, 100]]
        elif i == no_of_gears:
            gears[str(i) + " up"] = [[maxspeed, 0], [maxspeed, 100]]
            gears[str(i) + " down"] = np.array(downshift_dir[str(i-1)])
        else:
            gears[str(i) + " up"] = np.array(upshift_dir[str(i+1)])
            gears[str(i) + " down"] = np.array(downshift_dir[str(i-1)])
        print(i)
        print("Gear " + str(i) + " created")

    print(gears)
    # # For testing
    # gears["1 down"] = np.array([[0, 0], [0, 100]])
    # gears["1 up"] = np.array([[17, 0], [17, 15], [60, 60], [60, 100]])
    # gears["2 down"] = np.array([[7, 0], [7, 70], [45, 70], [45, 100]])
    # gears["2 up"] = np.array([[30, 0], [37, 15], [110, 60], [110, 100]])
    # gears["3 down"] = np.array([[21, 0], [25, 15], [45, 40], [105, 70], [105, 100]])
    # gears["3 up"] = np.array([[45, 0], [50, 12], [160, 60], [160, 100]])
    # gears["4 down"] = np.array([[35, 0], [50, 20], [150, 70], [150, 100]])
    # gears["4 up"] = np.array([[maxspeed, 0], [maxspeed, 100]])

    xrange = np.arange(0, maxspeed + 1, 1)
    yrange = np.arange(0, 101, 1)

    # Store coordinates within Lines Directory
    planes = {}

    # Set Up discrete coordinates for the lines
    for i in range(1, no_of_gears + 1):
        z = np.ones((maxspeed + 1, 101))
        z = z * min_rpm
        down = gears[str(i) + ' down']
        up = gears[str(i) + ' up']
        print(down)
        print(up)
        downarray = np.zeros((1, 2))
        uparray = np.zeros((1, 2))
        print(downarray)
        count = 0
        for j in range(len(down) - 1):
            start = down[j]
            end = down[j + 1]
            if (end[0] - start[0]) == 0:
                for k in range(start[1], end[1]):
                    downarray = np.append(downarray, [[start[0], k]], axis=0)
            else:
                m = (end[1] - start[1]) / (end[0] - start[0])
                if m == 0:
                    for k in range(start[0], end[0]):
                        y = int(np.round(m * (k - start[0]) + start[1]))
                        downarray = np.append(downarray, [[k, y]], axis=0)
                else:
                    for k in range(start[1], end[1]):
                        x = int(np.round((1 / m) * (k - start[1]) + start[0]))
                        downarray = np.append(downarray, [[x, k]], axis=0)
        downarray = np.append(downarray, [end], axis=0)
        downarray = np.delete(downarray, 0, axis=0)
        print(np.shape(downarray))

        for j in range(len(up) - 1):
            start = up[j]
            end = up[j + 1]
            print(start)
            print(end)
            count = 0
            if (end[0] - start[0]) == 0:
                for k in range(start[1], end[1]):
                    uparray = np.append(uparray, [[start[0], k]], axis=0)
            else:
                m = (end[1] - start[1]) / (end[0] - start[0])
                if m == 0:
                    for k in range(start[0], end[0]):
                        y = int(np.round(m * (k - start[0]) + start[1]))
                        uparray = np.append(uparray, [[k, y]], axis=0)
                else:
                    for k in range(start[1], end[1]):
                        x = int(np.round((1 / m) * (k - start[1]) + start[0]))
                        uparray = np.append(uparray, [[x, k]], axis=0)
        uparray = np.append(uparray, [end], axis=0)
        uparray = np.delete(uparray, 0, axis=0)

        # Create and plot lookup tables for rpm.
        for j in range(downarray.shape[1]):
            z[int(downarray[j, 0]), int(downarray[j, 1])] = min_rpm
        for j in range(uparray.shape[1]):
            z[int(uparray[j, 0]), int(uparray[j, 1])] = max_rpm
        for j in range(np.size(yrange) - 1):
            diff = int(uparray[j, 0]) - int(downarray[j, 0])
            gap = (max_rpm - min_rpm) / diff
            for k in range(int(downarray[j, 0]) + 1, int(uparray[j, 0]) - 1):
                z[k, j] = z[k - 1, j] + gap

        # Save z as an output plane
        z = np.swapaxes(z, 0, 1)
        planes[str(i) + " gear"] = z
        print(np.shape(z))

    # Plot as test.

    X, Y = np.meshgrid(xrange, yrange)

    print(np.shape(X))
    print(np.shape(Y))

    m = np.zeros([101, maxspeed + 1])
    print(np.shape(m))
    # All planes together
    for plane in planes:
        m += planes[plane]


    plt.contourf(X, Y, m, 10)

    plt.colorbar()
    plt.xlabel("Speed")
    plt.ylabel("Throttle")
    plt.title("Gear Contour Graph")
    plt.show()

    # for plane in planes:
    #     plt.contourf(X, Y, planes[plane], 10)
    #     plt.colorbar()
    #     plt.xlabel("Speed")
    #     plt.ylabel("Throttle")
    #     plt.title(plane)
    #     plt.show()
    #     plt.close()


    return planes
