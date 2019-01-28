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
        #print(problem.name)

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

        # Get relationships, hardcoded 2x2
        horizontal = self.compareAttributes(object1.attributes, object2.attributes)
        vertical = self.compareAttributes(object1.attributes, object3.attributes)

        #Get translational and diagonal answers, hardcoded 2x2
        #print("original: ")
        #print(object1.attributes)

        #print("horizontal: ")
        #print(horizontal)

        intermediate_answer = self.performTransform(object1.attributes,horizontal)
        #print("intermediate answer: ")
        #print(intermediate_answer)

        #print("vertical: ")
        #print(vertical)

        translational_answer = self.performTransform(intermediate_answer,vertical)
        #print("translational answer: ")
        #print(translational_answer)
        
        answer = translational_answer
        
        for potential_answer in answer_figures:
            for name, object in potential_answer.objects.items():
                #print(potential_answer.name, object.attributes)
                if answer == object.attributes:
                    #print("found answer: " + potential_answer.name + "\n")
                    return int(potential_answer.name)

        return -1

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


