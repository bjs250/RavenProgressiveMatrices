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
		self.log(debug, "Problem name", problem.name)

		# Get objects, hardcoded 2x2, single object per figure
		horizontal_pairs = self.pairObjects(problem.figures["A"].objects,problem.figures["B"].objects)
		vertical_pairs = self.pairObjects(problem.figures["A"].objects,problem.figures["C"].objects)
		
		# Objects dictionary from Figure A
		original = copy.deepcopy(problem.figures["A"].objects)
		del_list = []

		# Get relationships and transform, hardcoded 2x2
		for pair in horizontal_pairs:
			self.log(debug,"pair",self.pairToString(pair))

			# get transform
			if pair[1] is None:
				del_list.append(pair[0].name)
				continue
			horizontal = self.getFunction(pair[0], pair[1])
			
			# handle interdepencies
			if "inside" in horizontal:
				if horizontal["inside"] in horizontal_pairs:
					del horizontal["inside"]

			# Perform transform carefully
			if pair[0] is not None:
				result = self.performTransform(original[pair[0].name].attributes,horizontal)
				original[pair[0].name].attributes = result
			else:
				dummyname = "d"+str(dummycount)
				original[dummyname] = RavensObject(dummyname)
				original[dummyname].attributes = {}
				result = pair[1].attributes
				original[dummyname].attributes = result
				dummycount +=1
			
		for pair in vertical_pairs:
			self.log(debug,"pair",self.pairToString(pair))

			if pair[1] is None:
				del_list.append(pair[0].name)
				continue

			# get transform
			vertical = self.getFunction(pair[0], pair[1])
			
			# handle interdepencies
			if "inside" in vertical:
				if vertical["inside"] in vertical_pairs:
					del vertical["inside"]

			# Perform transform carefilly
			if pair[0] is not None:
				result = self.performTransform(original[pair[0].name].attributes,vertical)
				original[pair[0].name].attributes = result
			else:
				dummyname = "d"+str(dummycount)
				original[dummyname] = RavensObject(dummyname)
				original[dummyname].attributes = {}
				result = pair[1].attributes
				original[dummyname].attributes = result
				dummycount +=1
		
		for element in del_list:
			self.log(debug,"del",element)
			del original[element]
		
		# Compare prediction to answers
		answer_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == False]
		
		best = 1000
		answer = -1
		for answer_figure in answer_figures:
			pairs = self.pairObjects(original,answer_figure.objects)
			sum = 0
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
			if sum < best:
				answer = answer_figure.name
				best = sum
		if best != 0:
			self.log(debug,"End of main:","True answer never found")

		return int(answer)

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
		d = {}
		d["very small"] = 1
		d["small"] = 2
		d["medium"] = 3
		d["large"] = 4
		d["very large"] = 5
		d["huge"] = 6
		r = {}
		r[1] = "very small"
		r[2] = "small"
		r[3] = "medium"
		r[4] = "large"
		r[5] = "very large"
		r[6] = "huge"

		current_size = attributes["size"]
		
		try:
			difference = d[transform[1]]-d[transform[0]]
			attributes_copy["size"] = r[d[current_size]+difference]
		except:
			print("error occcurred in size transform!")
		finally:   
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
