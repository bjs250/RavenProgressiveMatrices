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
		
	def testB01(self):
		problem = self.problemDict["Basic Problem B-01"]
		imageFileNameA = problem.figures["A"].visualFilename
		count = connectedComponents.connectedComponents(imageFileNameA)
		self.assertEqual(count,1)

	def testB02(self):
		problem = self.problemDict["Basic Problem B-02"]
		imageFileNameA = problem.figures["A"].visualFilename
		count = connectedComponents.connectedComponents(imageFileNameA)
		self.assertEqual(count,2)
		

	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()