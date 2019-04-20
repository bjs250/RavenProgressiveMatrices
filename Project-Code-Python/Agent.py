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
import copy
import operator
from RavensObject import RavensObject

import image_processing
import connectedComponents

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
		debug = False
		self.log(True, "Problem name", problem.name)

		answer_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == False]
		closeness_threshold = 0.7

		if problem.problemType == "2x2":
			# Get objects, hardcoded 2x2, single object per figure
			#horizontal_pairs = self.pairObjects(problem.figures["A"].objects,problem.figures["B"].objects)
			#vertical_pairs = self.pairObjects(problem.figures["A"].objects,problem.figures["C"].objects)
			
			# Objects dictionary from Figure A
			#original = copy.deepcopy(problem.figures["A"].objects)
			return -1
		
		elif problem.problemType == "3x3":
			if "Challenge" in problem.name:
				return -1
		
		if "D-" in problem.name:

			# Execute graphical hypothesis testing
			
			# Positive: Identity (Row 1 and Row 2 all equivalent)
			identityAB = image_processing.checkIdentity(problem.figures["A"].visualFilename,problem.figures["B"].visualFilename,"filename")
			identityBC = image_processing.checkIdentity(problem.figures["B"].visualFilename,problem.figures["C"].visualFilename,"filename")
			identityDE = image_processing.checkIdentity(problem.figures["D"].visualFilename,problem.figures["E"].visualFilename,"filename")
			identityEF = image_processing.checkIdentity(problem.figures["E"].visualFilename,problem.figures["F"].visualFilename,"filename")
			
			print("===Identity 1 Test:") #D1
			if (identityAB and identityBC) or (identityDE and identityEF):
				DPs = {}
				IPs = {}
				for answer_figure in answer_figures:
					DP,IP = image_processing.computeIdentity(problem.figures["H"].visualFilename,answer_figure.visualFilename,"filename")
					DPs[answer_figure.name] = DP
					IPs[answer_figure.name] = IP
				sorted_DP = sorted(DPs.items(), key=operator.itemgetter(1))
				sorted_DP_dict = {t[0]:t[1] for t in sorted_DP}
				sorted_IP = sorted(IPs.items(), key=operator.itemgetter(1))
				sorted_IP_dict = {t[0]:t[1] for t in sorted_IP}
				scores = self.computeScores(sorted_DP_dict,sorted_IP_dict)
				sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
				ans = sorted_scores[-1][0]
				print(sorted_scores)
				return int(ans)
			
			# Positive: Identity (Rolling Diagonals)
			identityAE = image_processing.checkIdentity(problem.figures["A"].visualFilename,problem.figures["E"].visualFilename,"filename")
			identityBF = image_processing.checkIdentity(problem.figures["B"].visualFilename,problem.figures["F"].visualFilename,"filename")
			identityDH = image_processing.checkIdentity(problem.figures["D"].visualFilename,problem.figures["H"].visualFilename,"filename")
			
			print("===Identity 2 Test:",identityAE, identityBF, identityDH) #D2,D3
			if (identityAE and identityBF and identityDH):
				DPs = {}
				IPs = {}
				for answer_figure in answer_figures:
					DP,IP = image_processing.computeIdentity(problem.figures["E"].visualFilename,answer_figure.visualFilename,"filename")
					DPs[answer_figure.name] = DP
					IPs[answer_figure.name] = IP
				sorted_DP = sorted(DPs.items(), key=operator.itemgetter(1))
				sorted_DP_dict = {t[0]:t[1] for t in sorted_DP}
				sorted_IP = sorted(IPs.items(), key=operator.itemgetter(1))
				sorted_IP_dict = {t[0]:t[1] for t in sorted_IP}
				scores = self.computeScores(sorted_DP_dict,sorted_IP_dict)
				sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
				ans = sorted_scores[-1][0]
				print(sorted_scores)
				return int(ans)

			# Try to do num components row wise
			numA = connectedComponents.computeComponents(problem.figures["A"].visualFilename,False)
			numB = connectedComponents.computeComponents(problem.figures["B"].visualFilename,False)
			numC = connectedComponents.computeComponents(problem.figures["C"].visualFilename,False)
			
			filtered_answer_figures = {answer_figure.name:answer_figure for answer_figure in answer_figures}

			if numA == numB and numB == numC:
				numH = connectedComponents.computeComponents(problem.figures["H"].visualFilename,False)
			
				for answer_figure in answer_figures:
					numAns = connectedComponents.computeComponents(answer_figure.visualFilename,False)
					if numAns != numH and answer_figure.name in filtered_answer_figures:
						del filtered_answer_figures[answer_figure.name]

				# Remove duplicates
				question_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == True]
				for answer_figure in answer_figures:
					for question_figure in question_figures:
						#print(question_figure.name,answer_figure.name)
						DP,IP = image_processing.computeIdentity(question_figure.visualFilename,answer_figure.visualFilename,"filename")
						score = (1.0-DP)+IP
						if score > 1.90:
							
							#print("======",question_figure.name,answer_figure.name)
							if answer_figure.name in filtered_answer_figures:
								del filtered_answer_figures[answer_figure.name]

			remaining_answer_figures = list(filtered_answer_figures.values())
			for a in remaining_answer_figures:
				print(a.name)
			if len(remaining_answer_figures) == 1:
				print("====Eliminated by repeat check after num")
				return int(remaining_answer_figures[0].name)


			print("===Component-wise AND Test: rows") #D4
			# Row check
			row_same = {}
			if connectedComponents.check3(problem.figures["A"].visualFilename,problem.figures["B"].visualFilename,problem.figures["C"].visualFilename,"AND"):
				
				# Every answer must have that connected component
				bb1 = connectedComponents.computeComponents(problem.figures["G"].visualFilename, True)
				bb2 = connectedComponents.computeComponents(problem.figures["H"].visualFilename, True)
				
				# Figure out which components are in common
				pairingMatrix = connectedComponents.compareComponents(bb1,bb2)
				flag = "AND"
				bb_common = connectedComponents.getRelationship(bb1,bb2,pairingMatrix,flag)
				
				# Compare that to answer choice
				answer_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == False]
				for answer_figure in answer_figures:

					bb3 = connectedComponents.computeComponents(answer_figure.visualFilename, True)
					if flag is "AND":
						pairingMatrix = connectedComponents.compareComponents(bb_common,bb3)
						
						answer = True
						for row in pairingMatrix:
							if 1 not in row:
								answer = False

					row_same[answer_figure.name] = answer
				
			print("===Component-wise AND Test: cols") #D5
			# Col check
			col_same = {}
			if connectedComponents.check3(problem.figures["A"].visualFilename,problem.figures["D"].visualFilename,problem.figures["G"].visualFilename,"AND"):
				
				# Every answer must have that connected component
				bb1 = connectedComponents.computeComponents(problem.figures["C"].visualFilename, True)
				bb2 = connectedComponents.computeComponents(problem.figures["F"].visualFilename, True)
				
				# Figure out which components are in common
				pairingMatrix = connectedComponents.compareComponents(bb1,bb2)
				flag = "AND"
				bb_common = connectedComponents.getRelationship(bb1,bb2,pairingMatrix,flag)
				
				# Compare that to answer choice
				answer_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == False]
				for answer_figure in answer_figures:

					bb3 = connectedComponents.computeComponents(answer_figure.visualFilename, True)
					if flag is "AND":
						pairingMatrix = connectedComponents.compareComponents(bb_common,bb3)
						
						answer = True
						for row in pairingMatrix:
							if 1 not in row:
								answer = False

					col_same[answer_figure.name] = answer

			print("row")
			for key in row_same.keys():
				print(key,row_same[key])


			print("col")
			for key in col_same.keys():
				print(key,col_same[key])

			# get the survivors 
			union = []
			for key in row_same.keys():
				if row_same[key]:
					if key not in union:
						union.append(key)
			for key in col_same.keys():
				if col_same[key]:
					if key not in union:
						union.append(key)
			
			intersection = []
			for key in union:
				if key in row_same and row_same[key] and key in col_same and col_same[key]:
					if key not in intersection:
						intersection.append(key)

			print("union",union)
			print("intersection",intersection)

			# If the intersection is one at this point, we are done
			if len(intersection) == 1:
				ans = intersection[0]
				print("Singleton intersection")
				return int(ans)

			# Remove duplicates from the union?
			filtered_answer_figures = {answer_figure.name:answer_figure for answer_figure in answer_figures}
			#print(filtered_answer_figures)
			question_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == True]
			for answer_figure in answer_figures:
				if answer_figure.name in union:
					for question_figure in question_figures:
						#print(question_figure.name,answer_figure.name)
						DP,IP = image_processing.computeIdentity(question_figure.visualFilename,answer_figure.visualFilename,"filename")
						score = (1.0-DP)+IP
						if score > 1.95:
							print(question_figure.name,answer_figure.name,score)

							#print("======",question_figure.name,answer_figure.name)
							if answer_figure.name in filtered_answer_figures:
								del filtered_answer_figures[answer_figure.name]
				else:
					del filtered_answer_figures[answer_figure.name]

			
			remaining_answer_figures = list(filtered_answer_figures.values())
			print(remaining_answer_figures)
			if len(remaining_answer_figures) == 1:
				print("====Eliminated After Row and Col Check for repeats")
				return int(remaining_answer_figures[0].name)

			# row an col checks must have failed
			# Diag check
			print("===Component-wise AND Test: diag")
			diag_same = {}
			if connectedComponents.check3(problem.figures["B"].visualFilename,problem.figures["F"].visualFilename,problem.figures["G"].visualFilename,"AND"):
				print("diag hit")

				# Every answer must have that connected component
				bb1 = connectedComponents.computeComponents(problem.figures["A"].visualFilename, True)
				bb2 = connectedComponents.computeComponents(problem.figures["E"].visualFilename, True)
				
				# Figure out which components are in common
				pairingMatrix = connectedComponents.compareComponents(bb1,bb2)
				flag = "AND"
				bb_common = connectedComponents.getRelationship(bb1,bb2,pairingMatrix,flag)
				
				# Compare that to answer choice
				answer_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == False]
				for answer_figure in answer_figures:

					bb3 = connectedComponents.computeComponents(answer_figure.visualFilename, True)
					if flag is "AND":
						pairingMatrix = connectedComponents.compareComponents(bb_common,bb3)
						
						answer = True
						for row in pairingMatrix:
							if 1 not in row:
								answer = False

					diag_same[answer_figure.name] = answer
			
			print("diag")
			# Remove duplicates from the diag?
			union = []
			for key in diag_same.keys():
				if diag_same[key]:
					if key not in union:
						union.append(key)
			
			filtered_answer_figures = {answer_figure.name:answer_figure for answer_figure in answer_figures}
			#print(filtered_answer_figures)
			question_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == True]
			for answer_figure in answer_figures:
				if answer_figure.name in union:
					for question_figure in question_figures:
						#print(question_figure.name,answer_figure.name)
						DP,IP = image_processing.computeIdentity(question_figure.visualFilename,answer_figure.visualFilename,"filename")
						score = (1.0-DP)+IP
						if score > 1.95:
							print(question_figure.name,answer_figure.name,score)

							#print("======",question_figure.name,answer_figure.name)
							if answer_figure.name in filtered_answer_figures:
								del filtered_answer_figures[answer_figure.name]
				else:
					del filtered_answer_figures[answer_figure.name]
			
			remaining_answer_figures = list(filtered_answer_figures.values())
			print(remaining_answer_figures)
			if len(remaining_answer_figures) == 1:
				print("====Eliminated After Diag Check for repeats")
				return int(remaining_answer_figures[0].name)

			# Try using number
			numB = connectedComponents.computeComponents(problem.figures["B"].visualFilename,False)
			numF = connectedComponents.computeComponents(problem.figures["F"].visualFilename,False)
			numG = connectedComponents.computeComponents(problem.figures["G"].visualFilename,False)
			
			filtered_answer_figures = {answer_figure.name:answer_figure for answer_figure in answer_figures}

			if numB == numG and numF == numG:
				numA = connectedComponents.computeComponents(problem.figures["A"].visualFilename,False)
			
				print("try numA = numE")
				for answer_figure in answer_figures:
					numAns = connectedComponents.computeComponents(answer_figure.visualFilename,False)
					if numAns != numA and answer_figure.name in filtered_answer_figures:
						del filtered_answer_figures[answer_figure.name]
			
			print([answer_figure.name for answer_figure in answer_figures])
			answer_figures = list(filtered_answer_figures.values())
			print([answer_figure.name for answer_figure in answer_figures])
			if len(answer_figures) == 1:
				print("====Elimination by number")
				return int(answer_figures[0].name)

			numB = connectedComponents.computeComponents_white(problem.figures["B"].visualFilename,False)
			numF = connectedComponents.computeComponents_white(problem.figures["F"].visualFilename,False)
			numG = connectedComponents.computeComponents_white(problem.figures["G"].visualFilename,False)
			
			filtered_answer_figures = {answer_figure.name:answer_figure for answer_figure in answer_figures}

			if numB == numG and numF == numG:
				numA = connectedComponents.computeComponents_white(problem.figures["A"].visualFilename,False)
			
				print("try numA = numE")
				for answer_figure in answer_figures:
					numAns = connectedComponents.computeComponents_white(answer_figure.visualFilename,False)
					if numAns != numA and answer_figure.name in filtered_answer_figures:
						del filtered_answer_figures[answer_figure.name]
			
			print([answer_figure.name for answer_figure in answer_figures])
			answer_figures = list(filtered_answer_figures.values())
			print([answer_figure.name for answer_figure in answer_figures])
			if len(answer_figures) == 1:
				print("====Elimination by number 2")
				return int(answer_figures[0].name)

			# Remove duplicates
			filtered_answer_figures = {answer_figure.name:answer_figure for answer_figure in answer_figures}
			question_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == True]
			for answer_figure in answer_figures:
				for question_figure in question_figures:
					#print(question_figure.name,answer_figure.name)
					DP,IP = image_processing.computeIdentity(question_figure.visualFilename,answer_figure.visualFilename,"filename")
					score = (1.0-DP)+IP
					if score > 1.95:
						print(question_figure.name,answer_figure.name,score)

						#print("======",question_figure.name,answer_figure.name)
						if answer_figure.name in filtered_answer_figures:
							del filtered_answer_figures[answer_figure.name]

			answer_figures = list(filtered_answer_figures.values())
			print([answer_figure.name for answer_figure in answer_figures])
			if len(answer_figures) == 1:
				print("====Eliminated by repeat check")
				return int(answer_figures[0].name)

			"""
			# Check imagewise AND
			andAE = image_processing.computeAND(problem.figures["A"].visualFilename,problem.figures["E"].visualFilename,"filename")
			DPs = {}
			IPs = {}
			for key in filtered_answer_figures.keys():
				answer_figure = filtered_answer_figures[key]
				a = image_processing.load_image_from_filename(answer_figure.visualFilename)
				andEAns = image_processing.computeAND(andAE,a,"image")
				DP,IP = image_processing.computeIdentity(andAE,andEAns,"image")
				DPs[answer_figure.name] = DP
				IPs[answer_figure.name] = IP
			sorted_DP = sorted(DPs.items(), key=operator.itemgetter(1))
			sorted_DP_dict = {t[0]:t[1] for t in sorted_DP}
			sorted_IP = sorted(IPs.items(), key=operator.itemgetter(1))
			sorted_IP_dict = {t[0]:t[1] for t in sorted_IP}
			scores = self.computeScores(sorted_DP_dict,sorted_IP_dict)
			sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
			ans = sorted_scores[-1][0]
			print("==========================white flag===================================")
			print(sorted_scores)
			return -1
			return int(ans)

				
			# andABC = image_processing.checkAND(problem.figures["A"].visualFilename,problem.figures["B"].visualFilename,problem.figures["C"].visualFilename,"check")
			# andDEF = image_processing.checkAND(problem.figures["D"].visualFilename,problem.figures["E"].visualFilename,problem.figures["F"].visualFilename,"check")
			# #print(andABC,andDEF)
			# if andABC and andDEF:
			# 	for answer_figure in answer_figures:
			# 		andGHAns = image_processing.checkAND(problem.figures["G"].visualFilename,problem.figures["H"].visualFilename,answer_figure.visualFilename,"check")
			# 		#print(answer_figure.name, andGHAns)
			# 		if andGHAns:
			# 			print("AND Gate", answer_figure.name)
			# 			return int(answer_figure.name)
			"""

			if len(answer_figures) > 0:
				index = np.random.choice(len(answer_figures),1)[0]
				ans = answer_figures[index].name
				return int(ans)
			else:
				return -1
		

		
			"""
			# Identity tests failed --> no repeats
			filtered_answer_figures = {answer_figure.name:answer_figure for answer_figure in answer_figures}
			#print(filtered_answer_figures)
			question_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == True]
			for answer_figure in answer_figures:
				for question_figure in question_figures:
					#print(question_figure.name,answer_figure.name)
					DP,IP = image_processing.computeIdentity(question_figure.visualFilename,answer_figure.visualFilename,"filename")
					if DP < 0.015 and IP > 0.75:
						#print("======",question_figure.name,answer_figure.name)
						if answer_figure.name in filtered_answer_figures:
							del filtered_answer_figures[answer_figure.name]
			
			print("dict", filtered_answer_figures.keys())
			answer_figures = list(filtered_answer_figures.values())
			if len(answer_figures) == 1:
				print("====Elimination 1")
				return int(answer_figures[0].name)

			# Remove answers that have similar connected components to A and E

			# Apply heuristic as last resort
			# DP_A = image_processing.computeDP(problem.figures["A"].visualFilename,"filename")
			# DP_E = image_processing.computeDP(problem.figures["E"].visualFilename,"filename")
			# DP_Avg = (DP_A + DP_E)/2.0
			# min_DP = 1
			# best_answer = None
			# print("Average DP: ", DP_Avg)
			# for answer_figure in answer_figures:
			# 	DP_Ans = image_processing.computeDP(answer_figure.visualFilename,"filename")
			# 	if DP_Ans < min_DP:
			# 		best_answer = int(answer_figure.name)
			# 		min_DP = DP_Ans
			# 	print(answer_figure.name, DP_Ans, np.abs(DP_Ans-DP_Avg))
			# 	print("===heuristic")
			# 	return best_answer
			"""

		elif "E-" in problem.name:

			# Positive: OR Gate
			orABC = image_processing.checkOR(problem.figures["A"].visualFilename,problem.figures["B"].visualFilename,problem.figures["C"].visualFilename,"check")
			orDEF = image_processing.checkOR(problem.figures["D"].visualFilename,problem.figures["E"].visualFilename,problem.figures["F"].visualFilename,"check")
			if orABC and orDEF:
				for answer_figure in answer_figures:
					orGHAns = image_processing.checkOR(problem.figures["G"].visualFilename,problem.figures["H"].visualFilename,answer_figure.visualFilename,"check")
					#print(answer_figure.name, orGHAns)
					if orGHAns:
						print("OR Gate", answer_figure.name)
						return int(answer_figure.name)

			# Positive: AND Gate
			andABC = image_processing.checkAND(problem.figures["A"].visualFilename,problem.figures["B"].visualFilename,problem.figures["C"].visualFilename,"check")
			andDEF = image_processing.checkAND(problem.figures["D"].visualFilename,problem.figures["E"].visualFilename,problem.figures["F"].visualFilename,"check")
			#print(andABC,andDEF)
			if andABC and andDEF:
				for answer_figure in answer_figures:
					andGHAns = image_processing.checkAND(problem.figures["G"].visualFilename,problem.figures["H"].visualFilename,answer_figure.visualFilename,"check")
					#print(answer_figure.name, andGHAns)
					if andGHAns:
						print("AND Gate", answer_figure.name)
						return int(answer_figure.name)

			# Positive: XOR Gate
			xorABC = image_processing.checkXOR(problem.figures["A"].visualFilename,problem.figures["B"].visualFilename,problem.figures["C"].visualFilename,"check")
			xorDEF = image_processing.checkXOR(problem.figures["D"].visualFilename,problem.figures["E"].visualFilename,problem.figures["F"].visualFilename,"check")
			#print("xor",xorABC,xorDEF)
			if xorABC and xorDEF:
				best = 0
				for answer_figure in answer_figures:
					xorGHAns = image_processing.checkXOR(problem.figures["G"].visualFilename,problem.figures["H"].visualFilename,answer_figure.visualFilename,"filename")
					if xorGHAns[1] > best:
						final_answer = answer_figure.name
						best = xorGHAns[1]
				print("XOR Gate", answer_figure.name)
				return int(final_answer)

		#return -1
		if len(answer_figures) > 0:
			index = np.random.choice(len(answer_figures),1)[0]
			ans = answer_figures[index].name
			return int(ans)
		else:
			return -1
		
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

	def computeScores(self,DP_dict,IP_dict):
		scores = {}
		for key in DP_dict.keys():
			scores[key] = (1.0-DP_dict[key]) + IP_dict[key]
		return scores

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
