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

def computeCorners(imageFilename):
    if type(imageFilename) != type(np.ones((1,1))):
        grid = image_processing.load_image_from_filename(imageFilename)
    else:
        grid = imageFilename

    # Apply a threshold to make sure that there are only black and white pixels
    grid = (grid != 0) * 255

    corners = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}        
    for i in range(1,len(grid)-1):
        for j in range(1,len(grid[i]-1)):
            if grid[i][j] == 0:
                bcount = 0
                #cardinal
                if grid[i-1][j] == 0:
                    bcount += 1
                if grid[i+1][j] == 0:
                    bcount += 1
                if grid[i][j-1] == 0:
                    bcount += 1
                if grid[i][j+1] == 0:
                    bcount += 1
                #diag
                if grid[i-1][j-1] == 0:
                    bcount += 1
                if grid[i+1][j+1] == 0:
                    bcount += 1
                if grid[i-1][j+1] == 0:
                    bcount += 1
                if grid[i+1][j-1] == 0:
                    bcount += 1

                corners[bcount] +=1
    plt.imshow(grid)
    plt.show()
    
    return corners

def computeDifference(c1,c2):
    score = 0
    for key in c1.keys():
        score += np.abs(c1[key] - c2[key])
    return score

def computeCornersBB(bb):

    bb_corners = {}
    for key in bb.keys():
        grid = bb[key]
        
        # Apply a threshold to make sure that there are only black and white pixels
        grid = (grid != 0) * 255

        bb_corners[key] = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0}  
        for i in range(1,len(grid)-1 ):
            for j in range(1,len(grid[i])-1 ):
                if grid[i][j] == 0:
                    bcount = 0
                    #cardinal
                    if grid[i-1][j] == 0:
                        bcount += 1
                    if grid[i+1][j] == 0:
                        bcount += 1
                    if grid[i][j-1] == 0:
                        bcount += 1
                    if grid[i][j+1] == 0:
                        bcount += 1
                    #diag
                    if grid[i-1][j-1] == 0:
                        bcount += 1
                    if grid[i+1][j+1] == 0:
                        bcount += 1
                    if grid[i-1][j+1] == 0:
                        bcount += 1
                    if grid[i+1][j-1] == 0:
                        bcount += 1

                    bb_corners[key][bcount] +=1
        total = 0
        for p in bb_corners[key].keys():
            total += bb_corners[key][p]
        for p in bb_corners[key].keys():
            bb_corners[key][p] = int(bb_corners[key][p]/total*100)
        
        plt.imshow(grid)
        plt.show()
    
    return bb_corners

def computeComponents(imageFilename, bounding_box_flag):
    if type(imageFilename) != type(np.ones((1,1))):
        grid = image_processing.load_image_from_filename(imageFilename)
    else:
        grid = imageFilename

    # Apply a threshold to make sure that there are only black and white pixels
    grid = (grid != 0) * 255

    counter = 1
    d = {} # for holding connected components and associated pixels
    d[1] = []
    background = {} # for holding the "mask" of the image with only the white pixels
    background[1] = np.ones(grid.shape) * 255

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
                        background[counter][x-1][y] = 0
                        queue.insert(0,[x-1,y])
                    if x+1 <= len(grid)-1 and grid[x+1][y] == 0:
                        grid[x+1][y] = counter
                        d[counter].append((x+1,y))
                        background[counter][x+1][y] = 0
                        queue.insert(0,[x+1,y])
                    if y-1 >= 0 and grid[x][y-1] == 0:
                        grid[x][y-1] = counter
                        d[counter].append((x,y-1))
                        background[counter][x][y-1] = 0
                        queue.insert(0,[x,y-1])
                    if y+1 <= len(grid[0])-1 and grid[x][y+1] == 0:
                        grid[x][y+1] = counter
                        d[counter].append((x,y+1))
                        background[counter][x][y+1] = 0
                        queue.insert(0,[x,y+1])
                    queue.pop()
                if len(d[counter]) == 0:
                    counter -= 1
                counter += 1
                d[counter] = []
                background[counter] = np.ones(grid.shape) * 255

    del d[counter]
    del background[counter]
    counter-=1

    #plt.imshow(grid)
    #plt.show()
    #print("test",[(key,len(d[key])) for key in d.keys()])

    if bounding_box_flag == True:
        # Get bounding boxes of components
        bounding_boxes = {}
        for component in d.keys():
            xpos = [t[0] for t in d[component]]
            xmax = max(xpos)
            xmin = min(xpos)
            ypos = [t[1] for t in d[component]]
            ymax = max(ypos)
            ymin = min(ypos)
            #print(component, xmin, ymin, xmax, ymax)
            bounding_boxes[component] = background[component][xmin:xmax,ymin:ymax]
        return bounding_boxes
    else:
        return counter

def computeComponents_white(imageFilename, bounding_box_flag):
    if type(imageFilename) != type(np.ones((1,1))):
        grid = image_processing.load_image_from_filename(imageFilename)
    else:
        grid = imageFilename

    # Apply a threshold to make sure that there are only black and white pixels
    grid = (grid == 0) * 255

    counter = 1
    d = {} # for holding connected components and associated pixels
    d[1] = []
    background = {} # for holding the "mask" of the image with only the white pixels
    background[1] = np.ones(grid.shape) * 255

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
                        background[counter][x-1][y] = 0
                        queue.insert(0,[x-1,y])
                    if x+1 <= len(grid)-1 and grid[x+1][y] == 0:
                        grid[x+1][y] = counter
                        d[counter].append((x+1,y))
                        background[counter][x+1][y] = 0
                        queue.insert(0,[x+1,y])
                    if y-1 >= 0 and grid[x][y-1] == 0:
                        grid[x][y-1] = counter
                        d[counter].append((x,y-1))
                        background[counter][x][y-1] = 0
                        queue.insert(0,[x,y-1])
                    if y+1 <= len(grid[0])-1 and grid[x][y+1] == 0:
                        grid[x][y+1] = counter
                        d[counter].append((x,y+1))
                        background[counter][x][y+1] = 0
                        queue.insert(0,[x,y+1])
                    queue.pop()
                if len(d[counter]) == 0:
                    counter -= 1
                counter += 1
                d[counter] = []
                background[counter] = np.ones(grid.shape) * 255

    del d[counter]
    del background[counter]
    counter-=1

    #plt.imshow(grid)
    #plt.show()
    #print("test",[(key,len(d[key])) for key in d.keys()])

    if bounding_box_flag == True:
        # Get bounding boxes of components
        bounding_boxes = {}
        for component in d.keys():
            xpos = [t[0] for t in d[component]]
            xmax = max(xpos)
            xmin = min(xpos)
            ypos = [t[1] for t in d[component]]
            ymax = max(ypos)
            ymin = min(ypos)
            #print(component, xmin, ymin, xmax, ymax)
            bounding_boxes[component] = background[component][xmin:xmax,ymin:ymax]
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
            #print(c1,c2,DP,IP)
            if DP < 0.1 and IP > .70:
                pairingMatrix[c1-1][c2-1] = 1
            else:
                pairingMatrix[c1-1][c2-1] = 0
    print("=====")
                
    return pairingMatrix

def gateComponents(pairingMatrix,flag):
    d = {}
    d["rows"] = []
    d["cols"] = []
    rowlength = pairingMatrix.shape[0]
    collength = pairingMatrix.shape[1]
    for index,row in enumerate(pairingMatrix):
        if 1 in row:
            if flag == "AND":
                d["rows"].append(index)
        else:
            if flag == "XOR":
                d["rows"].append(index)
    for index,col in enumerate(pairingMatrix.T):
        if 1 in col:
            if flag == "AND":
                d["cols"].append(index)
        else:
            if flag == "XOR":
                d["cols"].append(index)
    return(d)

def getRelationship(bb1,bb2,pairingMatrix,flag):
    results = gateComponents(pairingMatrix,flag)

    if flag == "AND":
        return {index:bb1[item+1] for index,item in enumerate(results["rows"])}
    elif flag == "XOR":
        bb_common1 = {index:bb1[item+1] for index,item in enumerate(results["rows"])}
        bb_common2 = {index:bb2[item+1] for index,item in enumerate(results["rows"])}
        return (bb_common1,bb_common2)

def check3(inputA,inputB,inputC,flag):
    bb1 = computeComponents(inputA, True)
    bb2 = computeComponents(inputB, True)
    pairingMatrix = compareComponents(bb1,bb2)
    flag = "AND"
    bb_common = getRelationship(bb1,bb2,pairingMatrix,flag)
    
    if len(bb_common.keys())>0: # something in common
        
        bb3 = computeComponents(inputC, True)
        if flag is "AND":
            pairingMatrix = compareComponents(bb_common,bb3)
            
            answer = False
            for row in pairingMatrix:
                if 1 in row:
                    answer = True
    else:
        answer = False
    return answer