import unittest
import os
import sys
import csv

from Agent import Agent
from ProblemSet import ProblemSet
import image_processing
import numpy as np
from RavensObject import RavensObject
import connectedComponents

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
	"""
	
	def test_D07_AE(self):
		problem = self.problemDict["Basic Problem D-07"]
		#bb1 = connectedComponents.computeComponents(problem.figures["A"].visualFilename, True)
		#bb2 = connectedComponents.computeComponents(problem.figures["E"].visualFilename, True)
		bb1 = connectedComponents.computeComponents(problem.figures["C"].visualFilename, True)
		bb2 = connectedComponents.computeComponents(problem.figures["E"].visualFilename, True)
		
		pairingMatrix = connectedComponents.compareComponents(bb1,bb2)
		print(pairingMatrix,bb1[2].shape,bb2[2].shape)


	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()