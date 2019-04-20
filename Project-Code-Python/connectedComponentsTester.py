import unittest
import os
import sys
import csv
import operator

from Agent import Agent
from ProblemSet import ProblemSet
import image_processing
import numpy as np
from RavensObject import RavensObject
import connectedComponents
import matplotlib.pyplot as plt

def getNextLine(r):
	return r.readline().rstrip()
 
class TestUM(unittest.TestCase):
 
	def setUp(self):
		# taken from RavensProject.py
		self.sets=[] 
		r = open(os.path.join("Problems","ProblemSetList.txt"))    # ProblemSetList.txt lists the sets to solve.
		line = getNextLine(r)                                   # Sets will be solved in the order they appear in the file.
		while not line=="":                                     # You may modify ProblemSetList.txt for design and debugging.
			self.sets.append(ProblemSet(line))                       # We will use a fresh copy of all problem sets when grading.
			line=getNextLine(r)  
		r.close()

		self.agent=Agent()
		self.problemDict = {}
		for set in self.sets:
			for problem in set.problems: 
				self.problemDict[problem.name] = problem
	
	"""
	def test_D12(self):
		problem = self.problemDict["Basic Problem D-12"]
		imageFileName = problem.figures["A"].visualFilename
		count = connectedComponents.computeComponents(imageFileName,False)
		self.assertEqual(count,3)
		imageFileName = problem.figures["B"].visualFilename
		count = connectedComponents.computeComponents(imageFileName,False)
		self.assertEqual(count,4)
		imageFileName = problem.figures["C"].visualFilename
		count = connectedComponents.computeComponents(imageFileName,False)
		self.assertEqual(count,5)
		imageFileName = problem.figures["D"].visualFilename
		count = connectedComponents.computeComponents(imageFileName,False)
		self.assertEqual(count,5)
		imageFileName = problem.figures["E"].visualFilename
		count = connectedComponents.computeComponents(imageFileName,False)
		self.assertEqual(count,3)
		imageFileName = problem.figures["F"].visualFilename
		count = connectedComponents.computeComponents(imageFileName,False)
		self.assertEqual(count,4)

	def test_B01_A(self):
		problem = self.problemDict["Basic Problem B-01"]
		imageFileNameA = problem.figures["A"].visualFilename
		count = connectedComponents.connectedComponents(imageFileNameA)
		self.assertEqual(count,1)

	def test_B02_A(self):
		problem = self.problemDict["Basic Problem B-02"]
		imageFileNameA = problem.figures["A"].visualFilename
		count = connectedComponents.connectedComponents(imageFileNameA)
		self.assertEqual(count,2)
		
	def test_B03_1(self):
		problem = self.problemDict["Basic Problem B-03"]
		imageFileNameA = problem.figures["1"].visualFilename
		count = connectedComponents.connectedComponents(imageFileNameA)
		self.assertEqual(count,1)

	def test_CC(self):
		grid = np.ones((10,10)) * 255
		grid[1][2] = 0
		grid[2][2:8] = 0
		grid[4][2:8] = 0
		grid[6][2:8] = 0
		grid[3][2] = 0
		grid[5][2] = 0
		grid[3][7] = 0
		grid[5][7] = 0
		
		np.set_printoptions(threshold=np.inf)
		print("\n")
		print(grid)
		count = connectedComponents.computePixelRatio(grid,0)
		print(count)
	

	def test_D07_E(self):
		problem = self.problemDict["Basic Problem D-07"]
		imageFileName = problem.figures["E"].visualFilename
		count = connectedComponents.computeComponents(imageFileName, False)
		self.assertEqual(count,5)
	
	def test_D07_AE(self):
		problem = self.problemDict["Basic Problem D-07"]

		# Get bounding boxes of components in A and E
		bb1 = connectedComponents.computeComponents(problem.figures["A"].visualFilename, True)
		bb2 = connectedComponents.computeComponents(problem.figures["E"].visualFilename, True)
		
		# Figure out which components are in common
		pairingMatrix = connectedComponents.compareComponents(bb1,bb2)
		results = connectedComponents.gateComponents(pairingMatrix,"AND")
		bb_common = {index:bb1[item+1] for index,item in enumerate(results["rows"])}

		# Compare that to answer choice
		bb3 = connectedComponents.computeComponents(problem.figures["1"].visualFilename, True)
		pairingMatrix = connectedComponents.compareComponents(bb_common,bb3)
		print(pairingMatrix)

		answer = True
		for row in pairingMatrix:
			if 1 not in row:
				answer = False
		self.assertEqual(answer,True)	
	

	def test_D07_AE(self):
		problem = self.problemDict["Basic Problem D-07"]

		# Get bounding boxes of components in A and E
		bb1 = connectedComponents.computeComponents(problem.figures["A"].visualFilename, True)
		bb2 = connectedComponents.computeComponents(problem.figures["E"].visualFilename, True)
		
		# Figure out which components are in common
		pairingMatrix = connectedComponents.compareComponents(bb1,bb2)
		flag = "XOR"
		results = connectedComponents.gateComponents(pairingMatrix,flag)
		if flag is "AND":
			bb_common = {index:bb1[item+1] for index,item in enumerate(results["rows"])}
		if flag is "XOR":
			bb_common1 = {index:bb1[item+1] for index,item in enumerate(results["rows"])}
			bb_common2 = {index:bb2[item+1] for index,item in enumerate(results["rows"])}

		# Compare that to answer choice
		bb3 = connectedComponents.computeComponents(problem.figures["5"].visualFilename, True)
		if flag is "AND":
			pairingMatrix = connectedComponents.compareComponents(bb_common,bb3)
			print(pairingMatrix)

			answer = True
			for row in pairingMatrix:
				if 1 not in row:
					answer = False
			
			#self.assertEqual(answer,True)

		if flag is "XOR":
			pairingMatrix = connectedComponents.compareComponents(bb_common1,bb3)
			print(pairingMatrix)

			answer1 = True
			for row in pairingMatrix:
				if 1 not in row:
					answer1 = False

			pairingMatrix = connectedComponents.compareComponents(bb_common2,bb3)
			print(pairingMatrix)

			answer2 = True
			for row in pairingMatrix:
				if 1 not in row:
					answer2 = False

			self.assertEqual(answer1 or answer2,True)

	def test_D04(self):
		problem = self.problemDict["Basic Problem D-06"]

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
		print(diag_same)

		if flag is "XOR":
			pairingMatrix = connectedComponents.compareComponents(bb_common1,bb3)
			print(pairingMatrix)

			answer1 = True
			for row in pairingMatrix:
				if 1 not in row:
					answer1 = False

			pairingMatrix = connectedComponents.compareComponents(bb_common2,bb3)
			print(pairingMatrix)

			answer2 = True
			for row in pairingMatrix:
				if 1 not in row:
					answer2 = False

			#self.assertEqual(answer1 or answer2,True)
	"""
	
	"""
	def test_corners(self):
		problem = self.problemDict["Basic Problem D-08"]
		question_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == True]
		
		a = list()
		c1 = {}
		for question_figure in question_figures:
			bb = connectedComponents.computeComponents(question_figure.visualFilename, True)
			corners = connectedComponents.computeCornersBB(bb)
			c1[question_figure.name] = corners
			for key in corners:
				a.append((question_figure.name,key,corners[key]))
				#print(question_figure.name,key,corners[key])
		
		for thing in a:
			print(thing)

		question_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == False]
		
		a = list()
		for question_figure in question_figures:
			bb = connectedComponents.computeComponents(question_figure.visualFilename, True)
			corners = connectedComponents.computeCornersBB(bb)
			c1[question_figure.name] = corners
			for key in corners:
				a.append((question_figure.name,key,corners[key]))
				#print(question_figure.name,key,corners[key])
		print("")
		for thing in a:
			print(thing)

		connectedComponents.computeDifference(c1['A'],c1['B'])
	"""

	def test_w(self):
		problem = self.problemDict["Basic Problem D-09"]
		imageFileName = problem.figures["D"].visualFilename
		count = connectedComponents.computeComponents_white(imageFileName,False)
		print(count)

	


	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()