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

	#OR Gate
	def testE01(self):
		print("===================E01")
		problem = self.problemDict["Basic Problem E-01"]
		self.assertEqual(1, self.agent.Solve(problem))

	def testE02(self):
		print("===================E02")
		problem = self.problemDict["Basic Problem E-02"]
		self.assertEqual(7, self.agent.Solve(problem))

	def testE03(self):
		print("===================E03")
		problem = self.problemDict["Basic Problem E-03"]
		self.assertEqual(2, self.agent.Solve(problem))

	#AND Gate
	def testE10(self):
		print("===================E10")
		problem = self.problemDict["Basic Problem E-10"]
		self.assertEqual(8, self.agent.Solve(problem))

	def testE11(self):
		print("===================E11")
		problem = self.problemDict["Basic Problem E-11"]
		self.assertEqual(5, self.agent.Solve(problem))
	
	#XOR Gate
	def testE05(self):
		print("===================E05")
		problem = self.problemDict["Basic Problem E-05"]
		self.assertEqual(5, self.agent.Solve(problem))

	def testE07(self):
		print("===================E07")
		problem = self.problemDict["Basic Problem E-07"]
		self.assertEqual(3, self.agent.Solve(problem))

	def testE08(self):
		print("===================E08")
		problem = self.problemDict["Basic Problem E-08"]
		self.assertEqual(1, self.agent.Solve(problem))


	def tearDown(self):
		pass
		#print("=====Teardown=====")
	

if __name__ == '__main__':
	unittest.main()
