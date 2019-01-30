# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import numpy
import image_processing
from enum import Enum

class Size(Enum):
    very_small = 1
    small = 2
    medium = 3
    large = 4
    very_large = 5
    huge = 6

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        self.problem = problem
        debug = False
        #self.print(debug,problem.name)

        #Segregate the Ravens figures into questions and answers based on letters vs numbers
        #question_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha()]
        answer_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == False]

        # Get objects, hardcoded 2x2, single object per figure
        try:
            object1 = problem.figures["A"].objects["a"]
            object2 = problem.figures["B"].objects["b"]
            object3 = problem.figures["C"].objects["c"]        
        except:
            return -1
        
        objectsA = problem.figures["A"].objects
        objectsB = problem.figures["B"].objects
        objectsC = problem.figures["C"].objects
        #self.pairObjects(objectsA,objectsB)

        # Get relationships, hardcoded 2x2
        horizontal = self.compareAttributes(object1.attributes, object2.attributes)
        vertical = self.compareAttributes(object1.attributes, object3.attributes)

        #Get translational and diagonal answers, hardcoded 2x2
        #self.print(debug,"original: ")
        #self.print(debug,object1.attributes)

        #self.print(debug,"horizontal: ")
        #self.print(debug,horizontal)

        intermediate_answer = self.performTransform(object1.attributes,horizontal)
        #self.print(debug,"intermediate answer: ")
        #self.print(debug,intermediate_answer)

        #self.print(debug,"vertical: ")
        #self.print(debug,vertical)

        translational_answer = self.performTransform(intermediate_answer,vertical)
        #self.print(debug,"translational answer: ")
        #self.print(debug,translational_answer)
        
        answer = translational_answer
        
        for potential_answer in answer_figures:
            for name, object in potential_answer.objects.items():
                #self.print(debug,object.attributes)
                if answer == object.attributes:
                    #self.print(debug,"found answer: " + potential_answer.name + "\n")
                    return int(potential_answer.name)

        return -1

    def pairObjects(self,objects1,objects2):
        L = list()
        for key in objects2.keys():
            L.append(key)

        #print(L)

        pairs = set()
        for key1 in objects1.keys():
            min = 1000
            minkey = None
            for key2 in L:
                #print(key2)
                differences = self.compareAttributes(objects1[key1].attributes,objects2[key2].attributes)
                if len(differences) < min:
                    minkey = key2
                    min = len(differences)
                #print(key1,key2,min,minkey)
            pairs.add((key1,minkey))
            #print(key1,min,minkey,L)
            L.remove(minkey)
        return pairs

    # Output: dictionary of differences
    def compareAttributes(self,attributes1,attributes2):
        differences = {}
        for key in attributes1.keys():
            if key not in attributes2.keys():
                differences[key] = (attributes1[key],None)
            elif attributes1[key] != attributes2[key]:
                differences[key] = (attributes1[key],attributes2[key])
        for key in attributes2.keys():
            if key not in attributes1.keys():
                differences[key] = (None, attributes2[key])
        return differences

    # Input: A set of attributes and a tranform (usually from figure A) and the differences dict
    def performTransform(self,attributes,transform):
        attributes_copy = attributes.copy() #make sure no side effects in this method
        if transform == {}: # handle identity transform
            return attributes_copy
        if "angle" in transform and "angle" in attributes: # handle angle transform
            if transform["angle"][1] is None:
                del attributes_copy["angle"]
            else:
                attributes_copy = self.angleTransform(attributes_copy,transform["angle"])
        if "shape" in transform: # handle shape transform
            attributes_copy = self.stateTransform(attributes_copy,"shape",transform["shape"])    
        if "alignment" in transform: # handle alignment transform
            attributes_copy = self.alignmentTransform(attributes_copy,transform["alignment"]) 
        if "fill" in transform: # handle fill transform
            attributes_copy = self.fillTransform(attributes_copy,transform["fill"]) 
        if "size" in transform:
            attributes_copy = self.sizeTransform(attributes_copy,transform["size"]) 

        return attributes_copy

    def angleTransform(self,attributes,transform):
        attributes_copy = attributes.copy() #make sure no side effects in this method
        reflection_type = image_processing.guessRelection(transform)
        attributes_copy["angle"] = image_processing.performReflection(attributes_copy["angle"],reflection_type)
        return attributes_copy

    def stateTransform(self,attributes,state,transform):
        attributes_copy = attributes.copy() #make sure no side effects in this method
        attributes_copy[state] = transform[1]
        return attributes_copy

    def alignmentTransform(self, attributes, transform):
        attributes_copy = attributes.copy() #make sure no side effects in this method
        
        start = transform[0].split("-")
        end = transform[1].split("-")
        if start[0] != end[0]:
            ud_bit = -1
        else:
            ud_bit = 1
        if start[1] != end[1]:
            lr_bit = -1
        else:
            lr_bit = 1
        
        current_alignment = attributes_copy["alignment"]
        if current_alignment.split("-")[0] == "top" and ud_bit == -1:
            ud = "bottom"
        elif current_alignment.split("-")[0] == "bottom" and ud_bit == -1:
            ud = "top"
        else:
            ud = current_alignment.split("-")[0]
        if current_alignment.split("-")[1] == "left" and lr_bit == -1:
            lr = "right"
        elif current_alignment.split("-")[1] == "right" and lr_bit == -1:
            lr = "left"
        else:
            lr = current_alignment.split("-")[1]
        attributes_copy["alignment"] = ud+"-"+lr
        return attributes_copy

    def fillTransform(self,attributes,transform):
        attributes_copy = attributes.copy() #make sure no side effects in this method
        current_fill = attributes["fill"]
        if transform[0] != transform[1]:
            if current_fill == "yes":
                current_fill = "no"
            elif current_fill == "no":
                current_fill = "yes"
        attributes_copy["fill"] = current_fill
        return attributes_copy

    def sizeTransform(self,attributes,transform):
        attributes_copy = attributes.copy() #make sure no side effects in this method
        current_size = attributes["size"]
        difference = Size[transform[1]].value-Size[transform[0]].value
        attributes_copy["size"] =  Size(Size[current_size].value+difference).name
        return attributes_copy

   # def print(self, debug, text):
   #     if debug:
   #         print(text)


