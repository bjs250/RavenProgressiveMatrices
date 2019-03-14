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
import numpy as np
import image_processing
import copy
from RavensObject import RavensObject

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
		# Setup
		self.problem = problem
		dummycount = 0
		debug = False
		self.log(True, "Problem name", problem.name)

		if problem.problemType == "2x2":
			# Get objects, hardcoded 2x2, single object per figure
			horizontal_pairs = self.pairObjects(problem.figures["A"].objects,problem.figures["B"].objects)
			vertical_pairs = self.pairObjects(problem.figures["A"].objects,problem.figures["C"].objects)
			
			# Objects dictionary from Figure A
			original = copy.deepcopy(problem.figures["A"].objects)
		
		elif problem.problemType == "3x3":
			horizontal_pairs = self.pairObjects(problem.figures["E"].objects,problem.figures["F"].objects)
			vertical_pairs = self.pairObjects(problem.figures["E"].objects,problem.figures["H"].objects)
			
			original = copy.deepcopy(problem.figures["E"].objects)
			
		del_list = []
		
		# Change the original by using the horizontal and vertical pairs as reference
		self.mutateByTransform(horizontal_pairs,original,del_list,dummycount)
		self.mutateByTransform(vertical_pairs,original,del_list,dummycount)
		
		# 
		for element in del_list:
			self.log(debug,"del",element)
			del original[element]

		# Obtain list of interdependent attributes in the proposed answer
		interdependent_attributes = list()
		for obj_name,obj in original.items():
			for attr_name,attribute in obj.attributes.items():
				if attribute is not None:
					if (len(attribute) == 1 and attribute[0].isalpha()) or ("," in attribute):
						if attr_name not in interdependent_attributes:
							interdependent_attributes.append(attr_name)

		# Modify interdependencies (for example, if objects have been deleted)
		for key,obj in original.items():
			for attr_name in interdependent_attributes:
				if attr_name in obj.attributes and obj.attributes[attr_name] is not None:
					current_str = obj.attributes[attr_name]
					entries = current_str.split(",")
					edit_string = ""
					for entry in entries:
						if entry in original.keys():
							edit_string += entry + ","
					if edit_string == "":
						del obj.attributes[attr_name]
					else:
						edit_string = edit_string[:-1]
						obj.attributes[attr_name] = edit_string

		# Compare prediction to answers
		answer_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == False]
		
		#Execute smart tester
		if problem.problemType == "3x3":

			# Rotation Symmetry Test
			check = image_processing.checkRotation(problem.figures["G"].visualFilename,problem.figures["C"].visualFilename,90)
			selfcheck = image_processing.checkRotation(problem.figures["G"].visualFilename,problem.figures["G"].visualFilename,90)
			check2 = image_processing.checkRotation(problem.figures["H"].visualFilename,problem.figures["F"].visualFilename,90)
			selfcheck2 = image_processing.checkRotation(problem.figures["H"].visualFilename,problem.figures["H"].visualFilename,90)
			
			#print(check,selfcheck)
			if check and not selfcheck or (check2 and not selfcheck2):
				
				passed = list()
				
				# Do the rotation check
				for answer_figure in answer_figures:
					result = image_processing.checkRotation(answer_figure.visualFilename,answer_figure.visualFilename,90)
					#print(answer_figure.name,result)
					if result == True:
						passed.append(answer_figure)

				# Check if answer already appears
				final_passed = list()
				question_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == True]
				for index,answer_figure in enumerate(passed):
					falseCount = 0
					for question_figure in question_figures:
						result = image_processing.checkIdentity(answer_figure.visualFilename,question_figure.visualFilename)
						#print(question_figure.name,answer_figure.name,result, falseCount)
						if result == False:
							falseCount += 1
							if falseCount == 8:
								final_passed.append(answer_figure)
				
				answer_figures = final_passed

			# Check if num count stays the same
			objectCounts = list()
			minObjects = 0
			numTL = len(problem.figures["E"].objects.keys())
			numTR = len(problem.figures["F"].objects.keys())
			numBL = len(problem.figures["H"].objects.keys())

			if numTR == numTL and numBL == numTL:
				objectCount = numTR

				passed = list()
				for answer_figure in answer_figures:
					num = len(answer_figure.objects.keys())
					#print(answer_figure.name,num)
					if num == objectCount:
						passed.append(answer_figure)	
				answer_figures = passed
		
			# Eliminate based on num count
			elif numTR >= numTL and numBL >= numTL:
				minObjects = max([numTL,numTR,numBL])

				#print(minObjects)
				passed = list()
				for answer_figure in answer_figures:
					num = len(answer_figure.objects.keys())
					#print(answer_figure.name,num)
					if num >= minObjects:
						passed.append(answer_figure)
				answer_figures = passed
			
			# Try the addition trick
			numA = len(problem.figures["A"].objects.keys())
			numB = len(problem.figures["B"].objects.keys())
			numC = len(problem.figures["C"].objects.keys())
			
			numD = len(problem.figures["D"].objects.keys())
			numE = len(problem.figures["E"].objects.keys())
			numF = len(problem.figures["F"].objects.keys())

			#print(numA,numB,numC,numD,numE,numF)
			
			if numC == numB + (numB - numA) and numF == numE + (numE - numD):
				numG = len(problem.figures["G"].objects.keys())
				numH = len(problem.figures["H"].objects.keys())
				numTarget = numH + (numH-numG)
				#print(numG,numH,numTarget)
				
				passed = list()
				for answer_figure in answer_figures:
					num = len(answer_figure.objects.keys())
					#print(answer_figure.name,num)
					if num == numTarget:
						passed.append(answer_figure)	
				answer_figures = passed

			#print("-----")
			#print("remaining answers:")

			#for answer_figure in answer_figures:
			#	print(answer_figure.name)

		best = 1000
		answer = -1
		for answer_figure in answer_figures:
			pairs = self.pairObjects(original,answer_figure.objects)
			sum = 0

			# fix interdependent attributes
			pairMap = {}
			for pair in pairs:
				str_pair = self.pairToString(pair)
				pairMap[str_pair[1]] = str_pair[0]
			for key,obj in answer_figure.objects.items():
				for attr_name in interdependent_attributes:
					if attr_name in obj.attributes:
						inside_str = obj.attributes[attr_name]
						entries = inside_str.split(",")
						edit_string = ""
						#print(answer_figure.name,pairMap)
						for entry in entries:
							if pairMap[entry] is not None:
								edit_string += pairMap[entry] + ","
						edit_string = edit_string[:-1]
						#print(edit_string)
						obj.attributes[attr_name] = edit_string

			for pair in pairs:
				if pair[0] is not None:
					str1 = pair[0].name
					attr1 = original[str1].attributes
				else:
					str1 = None
					attr1 = {}
				if pair[1] is not None:
					str2 = pair[1].name
					attr2 = answer_figure.objects[str2].attributes
				else:
					str2 = None
					attr2 = {}
				differences = self.compareAttributes(attr1, attr2)
				sum += len(differences)
			self.log(debug,answer_figure.name,sum)
			if sum < best:
				answer = answer_figure.name
				best_answer = answer_figure
				best_pairs = pairs
				best_pairMap = pairMap
				best = sum
			#print(answer_figure.name,sum)
		if best != 0:
			self.log(True,"End of main:","True answer never found: " + str(best))
			#print("Answer: " + answer)
			#print("Generated")
			#for key,value in original.items():
			#	print(key,value.attributes)
			#print("Answer")
			#for key,value in best_answer.objects.items():
			#	print(key,value.attributes)
			#print(best_pairMap)

		return int(answer)

#=======================================================================================

# Get relationships and transform, hardcoded 2x2
	def mutateByTransform(self,pairs,original,del_list,dummycount):
			
		pairMap = {}
		for pair in pairs:
			str_pair = self.pairToString(pair)
			pairMap[str_pair[1]] = str_pair[0]

		for pair in pairs:
			#self.log(debug,"pair",self.pairToString(pair))

			# get transform
			if pair[1] is None:
				del_list.append(pair[0].name)
				continue
			funct = self.getFunction(pair[0], pair[1])

			
			# Obtain list of interdependent attributes in the proposed answer
			interdependent_attributes = list()
			for obj_name,obj in original.items():
				for attr_name,attribute in obj.attributes.items():
					if attribute is not None:
						if (len(attribute) == 1 and attribute[0].isalpha()) or ("," in attribute):
							if attr_name not in interdependent_attributes:
								interdependent_attributes.append(attr_name)
			
			# handle interdepencies
			for attr_name in interdependent_attributes:	
				if attr_name in funct:
					if funct[attr_name] in pairs:
						del funct[attr_name]

			# Perform transform carefully
			if pair[0] is not None:
				result = self.performTransform(original[pair[0].name].attributes,funct)
				original[pair[0].name].attributes = result
			else:
				dummyname = "d"+str(dummycount)
				original[dummyname] = RavensObject(dummyname)
				original[dummyname].attributes = {}

				for attr_name in interdependent_attributes:	
					if attr_name in pair[1].attributes:
						inside_str = pair[1].attributes[attr_name]
						entries = inside_str.split(",")
						edit_string = ""
						for entry in entries:
							if pairMap[entry] is not None:
								edit_string += pairMap[entry] + ","
						edit_string = edit_string[:-1]
						pair[1].attributes[attr_name] = edit_string

					result = pair[1].attributes
					original[dummyname].attributes = result
					dummycount +=1

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
	
	def getFunction(self,object1,object2):
		if object1 is None:
			object1 = RavensObject("dummy")
			object1.attributes = {}
		if object2 is None:
			object2 = RavensObject("dummy")
			object2.attributes = {}
		differences = self.compareAttributes(object1.attributes, object2.attributes)
		return differences			

	# Input: A set of attributes and a tranform (usually from figure A) and the differences dict
	def performTransform(self,attributes,transform):
		
		attributes_copy = attributes.copy() #make sure no side effects in this method

		indep_attrs = set()
		inter_attrs = set()
		for key in transform.keys():
			#self.log(True,"key",key)
			if key == "inside" or key == "above" or key =="overlaps" or key == "left-of":
				inter_attrs.add(key)
			else:
				indep_attrs.add(key)
			
		if transform == {}: # handle identity transform
			return attributes_copy
		if "angle" in transform and "angle" in attributes: # handle angle transform
			if transform["angle"][1] is None:
				del attributes_copy["angle"]
			else:
				attributes_copy = self.angleTransform(attributes_copy,transform["angle"])
			indep_attrs.remove("angle")
		
		
		if "alignment" in transform: # handle alignment transform
			attributes_copy = self.alignmentTransform(attributes_copy,transform["alignment"]) 
			indep_attrs.remove("alignment")
		
		
		L = list(indep_attrs)
		for key in L:
			attributes_copy = self.stateTransform(attributes_copy,key,transform[key]) 
			L.remove(key)

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
	
	def log(self, debug, header,text):
		if debug:
			print(header,text)

	def pairObjects(self,objects1,objects2):
		objs1 = [(key,value) for key,value in objects1.items()]
		objs2 = [(key,value) for key,value in objects2.items()]
		
		while len(objs1) > len(objs2):
			dummy = RavensObject("dummy")
			dummy.attributes = {}
			objs2.append((None,dummy))
		
		while len(objs1) < len(objs2):
			dummy = RavensObject("dummy")
			dummy.attributes = {}
			objs1.append((None,dummy))

		rows = len(objs1)
		cols = len(objs2)
		pairMatrix = np.zeros((rows,cols))
		pairs = set()

		#Generate the pairing matrix
		for r in range(rows):
			for c in range(cols):
				diff = self.compareAttributes(objs1[r][1].attributes,objs2[c][1].attributes)
				# handle interdependencies:
				diffCount = len(diff)
				if "inside" in diff:
					diffCount -= 1
				pairMatrix[r,c] = diffCount
				
		# Systematically pair objects by the global min
		while pairMatrix.shape != (0,0):
			min = np.unravel_index(pairMatrix.argmin(),pairMatrix.shape)
			obj1_name = objs1[min[0]][0]
			obj2_name = objs2[min[1]][0]
			if obj1_name is not None:
				obj1 = objects1[obj1_name]
			else:
				obj1 = None
			if obj2_name is not None:
				obj2 = objects2[obj2_name]
			else:
				obj2 = None
			pairs.add((obj1,obj2))
			pairMatrix = np.delete(pairMatrix,(min[0]),axis=0)
			pairMatrix = np.delete(pairMatrix,(min[1]),axis=1)
			del objs1[min[0]]
			del objs2[min[1]]
			
		return pairs

	# Given a tuple of Ravens Objects, return a string tuple of their names
	def pairToString(self,pair):
		if pair[0] is not None:
			str1 = pair[0].name
		else:
			str1 = None
		if pair[1] is not None:
			str2 = pair[1].name
		else:
			str2 = None
		return (str1,str2)
