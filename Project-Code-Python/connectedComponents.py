import os
import sys
import csv

import numpy as np
import image_processing

def computeComponents(imageFilename):
    if type(imageFilename) != type(np.ones((1,1))):
        grid = image_processing.load_image_from_filename(imageFilename)
    else:
        grid = imageFilename

    counter = 1
    #print(grid)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                grid[i][j] = counter
                queue = [[i,j]]
                while queue:
                    x,y = queue[-1][0],queue[-1][-1]
                    if x-1 >= 0 and grid[x-1][y] == 0:
                        grid[x-1][y] = counter
                        queue.insert(0,[x-1,y])
                    if x+1 <= len(grid)-1 and grid[x+1][y] == 0:
                        grid[x+1][y] = counter
                        queue.insert(0,[x+1,y])
                    if y-1 >= 0 and grid[x][y-1] == 0:
                        grid[x][y-1] = counter
                        queue.insert(0,[x,y-1])
                    if y+1 <= len(grid[0])-1 and grid[x][y+1] == 0:
                        grid[x][y+1] = counter
                        queue.insert(0,[x,y+1])
                    queue.pop()
                counter += 1

    counter-=1

    #print(counter)
    #print(grid)

    return counter