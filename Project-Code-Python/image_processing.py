import os
import sys
import csv

from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

DP_threshold = 0.01
IP_threshold = 0.75

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

def computeDP(inputFilename, flag):
    img = load_image_from_filename(inputFilename)
    return np.count_nonzero(img == 0)/(img.shape[0]*img.shape[1])

def computeIP(inputFilenameA,inputFilenameB):
    imgA = load_image_from_filename(inputFilenameA)
    imgB = load_image_from_filename(inputFilenameB)
    maskA = imgA == 0 # black in 1
    maskB = imgB == 0 # black in 2
    AandB = np.count_nonzero(np.bitwise_and(maskA,maskB))
    AxorB = np.count_nonzero(np.bitwise_xor(maskA,maskB))
    IP =   AandB / (AandB + AxorB)  

    return IP

def checkIdentity(inputFilenameA, inputFilenameB):
    DP_A = computeDP(inputFilenameA)
    DP_B = computeDP(inputFilenameB)
    IP_AB = computeIP(inputFilenameA,inputFilenameB)
    DP_AB = np.abs(DP_A - DP_B)

    #print(DP_A,DP_B,DP_AB,IP_AB)
    print(DP_AB,IP_AB)

    if DP_AB < DP_threshold and IP_AB > IP_threshold:
        return True
    else:
        return False

def checkRotation(inputFilename,outputFilename,angle, closeness_threshold):
    orig_im = Image.open(inputFilename)
    
    im2 = orig_im.convert('RGBA')
    rot = im2.rotate(angle)
    fff = Image.new('RGBA',rot.size,(255,)*4)
    im = Image.composite(rot,fff,rot)

    #im = im.rotate(angle,fillcolor='white')
    #orig_im.show()
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

def checkReflection(inputFilenameA, inputFilenameB, direction):
    imgA = Image.open(inputFilename)
    if direction == "left_right":
        imgA = imgA.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "top_bottom":
        imgA = imgA.transpose(Image.FLIP_TOP_BOTTOM)
    elif direction == "double":
        imgA = imgA.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT )

    imgA = imgA.convert('L')

    inputImage = image_to_array(im)
    outputImage = load_image_from_filename(outputFilename)

    Tversky = computeTversky(inputImage,outputImage)

    closeness = np.abs(Tversky-1.0)
    #print(closeness)

    im.close()

    if closeness < closeness_threshold:
        return (True,Tversky)
    else:
        return (False,Tversky)

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
    #print(result)
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
    
