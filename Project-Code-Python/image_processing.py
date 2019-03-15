import os
import sys
import csv

from PIL import Image
from PIL import ImageFilter


import numpy as np
from matplotlib import pyplot as plt

DP_threshold = 0.01
IP_threshold = 0.77

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

def computeDP(input, flag):
    if flag == "filename":
        img = load_image_from_filename(input)
    elif flag == "image":
        img = input
    return np.count_nonzero(img != 255)/(img.shape[0]*img.shape[1])

def computeIP(inputA,inputB, flag):
    if flag == "filename":
        imgA = load_image_from_filename(inputA)
        imgB = load_image_from_filename(inputB)
    elif flag == "image":
        imgA = inputA
        imgB = inputB
    maskA = imgA != 255 # black in 1
    maskB = imgB != 255 # black in 2
    AandB = np.count_nonzero(np.bitwise_and(maskA,maskB))
    AxorB = np.count_nonzero(np.bitwise_xor(maskA,maskB))
    #print(AandB,AxorB)
    IP =   AandB / (AandB + AxorB)  

    return IP

def checkIdentity(inputFilenameA, inputFilenameB,flag):
    DP_A = computeDP(inputFilenameA,flag)
    DP_B = computeDP(inputFilenameB,flag)
    IP_AB = computeIP(inputFilenameA,inputFilenameB,flag)
    DP_AB = np.abs(DP_A - DP_B)

    #print(DP_A,DP_B,DP_AB,IP_AB)
    print(DP_AB,IP_AB)

    if (DP_AB < DP_threshold and IP_AB > IP_threshold) or (DP_AB < DP_threshold*2 and IP_AB > .95):
        return True
    else:
        return False

def computeIdentity(inputFilenameA, inputFilenameB,flag):
    DP_A = computeDP(inputFilenameA,flag)
    DP_B = computeDP(inputFilenameB,flag)
    IP_AB = computeIP(inputFilenameA,inputFilenameB,flag)
    DP_AB = np.abs(DP_A - DP_B)

    #print(DP_A,DP_B,DP_AB,IP_AB)
    #print(DP_AB,IP_AB)

    return (DP_AB,IP_AB)

def checkRotation(inputA,inputB,angle):
    orig_im = Image.open(inputA)
    
    im2 = orig_im.convert('RGBA')
    rot = im2.rotate(angle)
    fff = Image.new('RGBA',rot.size,(255,)*4)
    im = Image.composite(rot,fff,rot)

    #im = im.rotate(angle,fillcolor='white')
    #orig_im.show()
    #im.show()
    
    im = im.convert('L')

    imgA = image_to_array(im)
    imgB = load_image_from_filename(inputB)

    result = checkIdentity(imgA,imgB,"image")

    im2.close()
    rot.close()
    fff.close()
    im.close()

    return result

def checkReflection(inputFilenameA, inputFilenameB, direction):
    imgA = Image.open(inputFilenameA)
    if direction == "left_right":
        imgA = imgA.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "top_bottom":
        imgA = imgA.transpose(Image.FLIP_TOP_BOTTOM)
    elif direction == "double":
        imgA = imgA.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT )

    imgA = imgA.convert('L')

    inputImageA = image_to_array(imgA)
    inputImageB = load_image_from_filename(inputFilenameB)

    result = checkIdentity(inputImageA,inputImageB,"image")

    return result

# Check if an image is the sum of two other images
def checkAddition(inputA, inputB, inputC, returnFlag):
    if 1:
        #im1 = Image.open(inputFilename1)
        #im1.show()
        #im2 = Image.open(inputFilename2)
        #im2.show()
        #im3 = Image.open(outputFilename)
        #im3.show()
        pass
        
    imgA = load_image_from_filename(inputA)
    imgB = load_image_from_filename(inputB)
    imgC = load_image_from_filename(inputC)

    maskA = imgA != 255 # black in 1
    maskB = imgB != 255 # black in 2
    AorB = np.bitwise_or(maskA,maskB) # w = False, b = True
    addition = (AorB == 0) * 255
    #print(addition)

    # addition2 = imgA + imgB
    
    # for row in range(addition2.shape[0]):
    #     for col in range(addition2.shape[1]):
    #         # w + w
    #         if addition2[row][col] == 510:
    #             addition2[row][col] = 255
    #         # b + w or w + b
    #         elif addition2[row][col] == 255:
    #             addition2[row][col] = 0
    #         elif addition2[row][col] == 0:
    #             addition2[row][col] = 0
    
    #print(addition == addition2)
    #plt.show()
    #print(result)

    if returnFlag == "check":
        result = checkIdentity(addition,imgC,"image")
        return result
    else:
        DP,IP = result = computeIdentity(addition,imgC,"image")
        return (DP,IP)

def internalSymmetryCheck(inputA,inputB,flag,plane):
    if flag == "image":
        imageA = Image.open(inputA,"r")
        imageA = imageA.filter(ImageFilter.BLUR)
        imageA = imageA.filter(ImageFilter.BLUR)
        imageA = imageA.convert('L')
        imageA = image_to_array(imageA)
        
        imageB = Image.open(inputB,"r")
        imageB = imageB.filter(ImageFilter.BLUR)
        imageB = imageB.filter(ImageFilter.BLUR)

        imageB = imageB.convert('L')
        imageB = image_to_array(imageB)
        
    else:
        imageA = inputA
        imageB = inputB
    if plane == "vertical":
        left_halfA = imageA[:,0:imageA.shape[1]/2]
        right_halfA = imageA[:,imageA.shape[1]/2:]
        left_halfB = imageB[:,0:imageB.shape[1]/2]
        right_halfB = imageB[:,imageB.shape[1]/2:]

        #blurred = blurred.filter(ImageFilter.BLUR)
        #blurred.show()

    result1 = computeIdentity(left_halfA,right_halfB,"image")    
    result2 = computeIdentity(right_halfA,left_halfB,"image")    

    print(result1,result2)

    plt.matshow(left_halfA)
    plt.matshow(right_halfB)
    #plt.matshow(right_halfA)
    #plt.matshow(left_halfB)
    
    plt.show()
