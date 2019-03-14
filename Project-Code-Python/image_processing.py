import os
import sys
import csv

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

closeness_threshold = 0.07

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
    
    #sum = imageA + imageB
    #both_black = np.count_nonzero(sum == 510)
    #both_white = np.count_nonzero(sum == 0)
    #AandB = both_black + both_white

    """
    diffAB = XOR(imageA,imageB)#imageA - imageB
    AnotB = np.count_nonzero(diffAB != 0)
    diffBA = XOR(imageB,imageA)#imageB - imageA
    BnotA = np.count_nonzero(diffBA != 0)
    """

    AnotB,BnotA,AandB = diffs(imageA,imageB)

    alpha = 0.5
    beta = 0.5
    Tversky = AandB / (AandB + alpha * AnotB + beta * BnotA)
    print(AandB,AnotB,BnotA,AandB+AnotB+BnotA,Tversky,1.0-Tversky)

    return Tversky

def XOR(arr1,arr2):
    out = np.zeros((arr1.shape[0],arr1.shape[1]))
    for row in range(arr1.shape[0]):
        for col in range(arr1.shape[1]):
            if arr1[row][col] == 255 and arr2[row][col] == 255:
                out[row][col] = 255
            elif arr1[row][col] == 0 and arr2[row][col] == 255:
                out[row][col] = 0
            elif arr1[row][col] == 0 and arr2[row][col] == 0:
                out[row][col] = 255
            elif arr1[row][col] == 255 and arr2[row][col] == 0:
                out[row][col] = 255
    return out

def diffs(arr1,arr2):
    AnotB = 0
    BnotA = 0
    AandB = 0
    for row in range(arr1.shape[0]):
        for col in range(arr1.shape[1]):
            if arr1[row][col] == 0 and arr2[row][col] == 255:
                AnotB +=1
            elif arr1[row][col] == 255 and arr2[row][col] == 0:
                BnotA +=1
            elif arr1[row][col] == 0 and arr2[row][col] == 0:
                AandB += 1
    return (AnotB,BnotA,AandB)


def checkIdentity(inputFilename, outputFilename):
    inputImage = load_image_from_filename(inputFilename)
    outputImage = load_image_from_filename(outputFilename)
    
    Tversky = computeTversky(inputImage,outputImage)

    closeness = np.abs(Tversky-1.0)
    print(closeness,closeness_threshold)

    if closeness < closeness_threshold:
        return True
    else:
        return False

def checkIdentityArrays(input, output):
    Tversky = computeTversky(input,output)

    closeness = np.abs(Tversky-1.0)
    #print(closeness)

    if closeness < closeness_threshold:
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

    if closeness < closeness_threshold:
        return True
    else:
        return False

def checkReflection(inputFilename, outputFilename, direction):
    im = Image.open(inputFilename)
    if direction == "left_right":
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "top_bottom":
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    elif direction == "double":
        im = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT )
    #im.show()

    im = im.convert('L')

    inputImage = image_to_array(im)
    outputImage = load_image_from_filename(outputFilename)

    Tversky = computeTversky(inputImage,outputImage)

    closeness = np.abs(Tversky-1.0)
    #print(closeness)

    im.close()

    if closeness < closeness_threshold:
        return True
    else:
        return False

# Check if an image is the sum of two other images
def checkAddition(inputFilename1, inputFilename2, outputFilename):
    if 1:
        #im1 = Image.open(inputFilename1)
        #im1.show()
        #im2 = Image.open(inputFilename2)
        #im2.show()
        #im3 = Image.open(outputFilename)
        #im3.show()
        pass
        
    in1 = load_image_from_filename(inputFilename1)
    in2 = load_image_from_filename(inputFilename2)
    out = load_image_from_filename(outputFilename)
    addition = in1 + in2
    for row in range(addition.shape[0]):
        for col in range(addition.shape[1]):
            # w + w
            if addition[row][col] == 510:
                addition[row][col] = 255
            # b + w or w + b
            elif addition[row][col] == 255:
                addition[row][col] = 0
            elif addition[row][col] == 0:
                addition[row][col] = 0
    plt.show()
    result = checkIdentityArrays(addition,out)
    print(result)
    return result












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
    
