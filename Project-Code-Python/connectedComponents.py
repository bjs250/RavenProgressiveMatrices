"""
This is a slightly adapted solution to the classic interview question, Number of Islands
Code adapted shamelessly from: https://leetcode.com/problems/number-of-islands/discuss/272502/Python-simple-DFS  
"""

import os
import sys
import csv

import numpy as np
import image_processing
import matplotlib.pyplot as plt

def computeComponents(imageFilename, bounding_box_flag):
    if type(imageFilename) != type(np.ones((1,1))):
        grid = image_processing.load_image_from_filename(imageFilename)
    else:
        grid = imageFilename

    # Apply a threshold to make sure that there are only black and white pixels
    grid = (grid != 0) * 255

    counter = 1
    d = {}
    d[1] = []

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                grid[i][j] = counter
                queue = [[i,j]]
                while queue:
                    x,y = queue[-1][0],queue[-1][-1]
                    if x-1 >= 0 and grid[x-1][y] == 0:
                        grid[x-1][y] = counter
                        d[counter].append((x-1,y))
                        queue.insert(0,[x-1,y])
                    if x+1 <= len(grid)-1 and grid[x+1][y] == 0:
                        grid[x+1][y] = counter
                        d[counter].append((x+1,y))
                        queue.insert(0,[x+1,y])
                    if y-1 >= 0 and grid[x][y-1] == 0:
                        grid[x][y-1] = counter
                        d[counter].append((x,y-1))
                        queue.insert(0,[x,y-1])
                    if y+1 <= len(grid[0])-1 and grid[x][y+1] == 0:
                        grid[x][y+1] = counter
                        d[counter].append((x,y+1))
                        queue.insert(0,[x,y+1])
                    queue.pop()
                counter += 1
                d[counter] = []

    del d[counter]
    counter-=1

    # Get bounding boxes of components
    bounding_boxes = {}
    for component in d.keys():
        xpos = [t[0] for t in d[component]]
        xmax = max(xpos)
        xmin = min(xpos)
        ypos = [t[1] for t in d[component]]
        ymax = max(ypos)
        ymin = min(ypos)
        print(component, xmin, ymin, xmax, ymax)
        bounding_boxes[component] = grid[xmin:xmax,ymin:ymax]
    
    #print(d)
    #print(counter)
    #plt.imshow(bounding_boxes[3])
    #plt.show()

    if bounding_box_flag == True:
        return bounding_boxes
    else:
        return counter

def compareComponents(bb1,bb2):
    pairingMatrix = np.zeros((len(bb1.keys()),len(bb2.keys())))
    for c1 in bb1.keys():
        for c2 in bb2.keys():
            row_max = max(bb1[c1].shape[0],bb2[c2].shape[0])
            col_max = max(bb1[c1].shape[1],bb2[c2].shape[1])
            #print("c1",c1,bb1[c1].shape)
            #print("c2",c2,bb2[c2].shape)
            temp1 = np.ones((row_max,col_max))*255
            temp2 = np.ones((row_max,col_max))*255
            #print("temp",temp1.shape,temp2.shape)
            temp1[0:bb1[c1].shape[0],0:bb1[c1].shape[1]] = bb1[c1]
            temp2[0:bb2[c2].shape[0],0:bb2[c2].shape[1]] = bb2[c2]
            DP,IP = image_processing.computeIdentity(temp1,temp2,"image")
            #print(DP,IP)
            if DP < 0.1 and IP > .70:
                pairingMatrix[c1-1][c2-1] = 1
            else:
                pairingMatrix[c1-1][c2-1] = 0
                
    return pairingMatrix
           