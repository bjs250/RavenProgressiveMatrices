import os
import sys
import csv

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

def load_image_from_filename(infilename):
    x = Image.open(infilename,"r")
    x = x.convert('L')
    y = np.asarray(x.getdata(),dtype=np.float64).reshape((x.size[1],x.size[0]))
    y = np.asarray(y,dtype=np.uint16)
    x.close()
    return y

def image_to_array(x):
    y = np.asarray(x.getdata(),dtype=np.float64).reshape((x.size[1],x.size[0]))
    y = np.asarray(y,dtype=np.uint16)       
    return y

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint32"), "L" )
    img.save( outfilename )
    img.close()

def computeTversky(imageA,imageB):
    
    sum = imageA + imageB
    both_black = np.count_nonzero(sum == 510)
    both_white = np.count_nonzero(sum == 0)
    AandB = both_black + both_white

    diffAB = imageA - imageB
    AnotB = np.count_nonzero(diffAB != 0)
    diffBA = imageB - imageA
    BnotA = np.count_nonzero(diffBA != 0)

    alpha = 0.5
    beta = 0.5
    Tversky = AandB / (AandB + alpha * AnotB + beta * BnotA)
    #print(AandB,AnotB,BnotA,Tversky)

    return Tversky
    
def checkIdentity(inputFilename, outputFilename):
    inputImage = load_image_from_filename(inputFilename)
    outputImage = load_image_from_filename(outputFilename)
    
    Tversky = computeTversky(inputImage,outputImage)

    closeness = np.abs(Tversky-1.0)
    #print(closeness)

    if closeness < .05:
        return True
    else:
        return False

def checkRotation(inputFilename,outputFilename,angle):
    orig_im = Image.open(inputFilename)
    
    im2 = orig_im.convert('RGBA')
    rot = im2.rotate(angle)
    fff = Image.new('RGBA',rot.size,(255,)*4)
    im = Image.composite(rot,fff,rot)

    #im = im.rotate(angle,fillcolor='white')
    #im.show()
    
    im = im.convert('L')

    inputImage = image_to_array(im)
    outputImage = load_image_from_filename(outputFilename)

    #print(inputFilename)
    Tversky = computeTversky(inputImage,outputImage)

    closeness = np.abs(Tversky-1.0)
    #print(inputFilename,outputFilename,closeness)

    im2.close()
    rot.close()
    fff.close()
    im.close()

    if closeness < .07:
        return True
    else:
        return False

def checkReflection(inputFilename, outputFilename, direction):
    im = Image.open(inputFilename)
    if direction == "left_right":
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "top_bottom":
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    #im.show()

    im = im.convert('L')

    inputImage = image_to_array(im)
    outputImage = load_image_from_filename(outputFilename)

    Tversky = computeTversky(inputImage,outputImage)

    closeness = np.abs(Tversky-1.0)
    #print(closeness)

    im.close()

    if closeness < .07:
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
    
