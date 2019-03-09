import os
import sys
import csv

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

def load_image(infilename) :
    x = Image.open(infilename,"r")
    x = x.convert('L')
    y = np.asarray(x.getdata(),dtype=np.float64).reshape((x.size[1],x.size[0]))
    y = np.asarray(y,dtype=np.uint16)
    return y

# stolen
def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint32"), "L" )
    img.save( outfilename )

def checkIdentity(inputFilename, outputFilename):
    inputImage = load_image(inputFilename)
    outputImage = load_image(outputFilename)
    dim = inputImage.shape[0] * inputImage.shape[1]
    sum = inputImage + outputImage
    both_black = np.count_nonzero(sum == 510)
    both_white = np.count_nonzero(sum == 0)
    AandB = both_black + both_white

    diffAB = inputImage - outputImage
    AnotB = np.count_nonzero(diffAB != 0)
    diffBA = outputImage - inputImage
    BnotA = np.count_nonzero(diffBA != 0)

    alpha = 0.5
    beta = 0.5
    Tversky = AandB / (AandB + alpha * AnotB + beta * BnotA)
    print(AandB,AnotB,BnotA,dim,Tversky)

    closeness = np.abs(Tversky-1.0)
    print(closeness)
    if closeness < .05:
        return True
    else:
        return False






def checkReflection(image1_filename, image2_filename, axis):
    tolerance = 100000  
    image = load_image(image1_filename)
    possible_reflection = load_image(image2_filename)

    if axis == "vertical":
        processed_reflection = np.fliplr(image)
    elif axis == "horizontal":
        processed_reflection = np.flipud(image)

    debug = False
    if debug:
        plt.imshow(image, interpolation='nearest')
        plt.show()
        plt.imshow(possible_reflection, interpolation='nearest')
        plt.show()
        plt.imshow(processed_reflection, interpolation='nearest')
        plt.show()

    difference = np.sum(np.sum(abs(possible_reflection-processed_reflection)))
    #print(difference)
    if abs(difference) < tolerance:
        return True
    else:
        return False

# Given two angles, determine whether a vertical or horizontal reflection occurs
def guessRelection(angles):
    start_angle = int(angles[0])
    end_angle = int(angles[1])
    difference = end_angle - start_angle
    if difference < -90:
        difference += 360
    if difference > 90:
        difference -= 360
    if start_angle > 0 and start_angle <= 90:
        quadrant = 1
    elif start_angle > 90 and start_angle <= 180:
        quadrant = 2
    elif start_angle > 180 and start_angle <= 270:
        quadrant = 3
    elif (start_angle > 270 and start_angle <= 360) or start_angle == 0:
        quadrant = 4
    else:
        raise Exception("Invalid angle argument")
    #print(angles,quadrant,difference)
    
    if (quadrant == 1 or quadrant == 3) and difference == -90:
        return "horizontal"
    if (quadrant == 1 or quadrant == 3) and difference == 90:
        return "vertical"
    if (quadrant == 2 or quadrant == 4) and difference == 90:
        return "horizontal"
    if (quadrant == 2 or quadrant == 4) and difference == -90:
        return "vertical"


def performReflection(current_angle,reflection_type):
    #print(current_angle,reflection_type)
    current_angle = int(current_angle)
    if current_angle > 0 and current_angle <= 90:
        quadrant = 1
    elif current_angle > 90 and current_angle <= 180:
        quadrant = 2
    elif current_angle > 180 and current_angle <= 270:
        quadrant = 3
    elif (current_angle > 270 and current_angle <= 360) or current_angle == 0:
        quadrant = 4
    else:
        raise Exception("Invalid angle argument")
    if (quadrant == 1 or quadrant == 3) and reflection_type == "horizontal":
        current_angle -= 90
    if (quadrant == 1 or quadrant == 3) and reflection_type == "vertical":
        current_angle += 90
    if quadrant == 2 and reflection_type == "horizontal":
        current_angle += 90
    if current_angle < 0:
        current_angle += 360
    if current_angle >=360:
        current_angle -= 360
    return str(current_angle)

    
    


if __name__ == "__main__":
    pass
    
