import unittest
import os
import sys
import csv
import copy
import warnings

from Agent import Agent
from ProblemSet import ProblemSet
import image_processing
import numpy as np
from RavensObject import RavensObject

def getNextLine(r):
	return r.readline().rstrip()
 
class TestUM(unittest.TestCase):
 
	def setUp(self):
		with warnings.catch_warnings():
			warnings.simplefilter("ignore")
			
			#print("=====Setup===== \n")

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
			#print("=================================")

    # Identity
	def testD01(self):
		print("===================D01")
		problem = self.problemDict["Basic Problem D-01"]
		self.assertEqual(3, self.agent.Solve(problem))

	def testD02(self):
		print("===================D02")
		problem = self.problemDict["Basic Problem D-02"]
		self.assertEqual(1, self.agent.Solve(problem))

	def testD03(self):
		print("===================D03")
		problem = self.problemDict["Basic Problem D-03"]
		self.assertEqual(3, self.agent.Solve(problem))

	def testD11(self):
		print("===================D11")
		problem = self.problemDict["Basic Problem D-11"]
		self.assertEqual(3, self.agent.Solve(problem))

	def tearDown(self):
		pass
		#print("=====Teardown=====")
	

if __name__ == '__main__':
	unittest.main()
