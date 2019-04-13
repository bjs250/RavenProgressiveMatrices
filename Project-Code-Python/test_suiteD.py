import unittest
import os
import sys
import csv
import copy
import warnings
import operator

from Agent import Agent
from ProblemSet import ProblemSet
import image_processing
import numpy as np
import connectedComponents
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
	def testD04(self):
		print("===================D04")
		problem = self.problemDict["Basic Problem D-04"]
		self.assertEqual(1, self.agent.Solve(problem))

	def testD05(self):
		print("===================D05")
		problem = self.problemDict["Basic Problem D-05"]
		self.assertEqual(7, self.agent.Solve(problem))


	"""
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
	
	def testD10(self):
		print("===================D10")
		problem = self.problemDict["Basic Problem D-10"]
		self.assertEqual(1, self.agent.Solve(problem))

	def testD07(self):
		print("===================D07")
		problem = self.problemDict["Basic Problem D-07"]
		self.assertEqual(1, self.agent.Solve(problem))
	
	def testD09(self):
		print("===================D09")
		problem = self.problemDict["Basic Problem D-09"]
		self.assertEqual(3, self.agent.Solve(problem))

	def testD05(self):
		print("===================D05")
		problem = self.problemDict["Basic Problem D-05"]
		self.assertEqual(7, self.agent.Solve(problem))

#########################

	def testD06(self):
		print("===================D06")
		problem = self.problemDict["Basic Problem D-06"]
		self.assertEqual(1, self.agent.Solve(problem))

	def testD12(self):
		print("===================D12")
		problem = self.problemDict["Basic Problem D-12"]
		self.assertEqual(3, self.agent.Solve(problem))

	def testD08(self):
		print("===================D08")
		problem = self.problemDict["Basic Problem D-08"]
		self.assertEqual(4, self.agent.Solve(problem))
	"""
	
	"""
	def test_seg(self):
		print("===================D08")
		problem = self.problemDict["Basic Problem D-10"]
		question_figures = [problem.figures[key] for key in problem.figures.keys() if key.isalpha() == True]
		
		DPs = {}
		for question_figure in question_figures:
			DP = image_processing.computeDP(question_figure.visualFilename, "filename")
			DPs[question_figure.name] = DP
		sorted_DPs = sorted(DPs.items(), key=operator.itemgetter(1))
		print(sorted_DPs)

		CCs = {}
		for question_figure in question_figures:
			CC = connectedComponents.computeComponents(question_figure.visualFilename,False)
			CCs[question_figure.name] = CC
		sorted_CCs = sorted(CCs.items(), key=operator.itemgetter(1))
		print(sorted_CCs)
	"""

	def tearDown(self):
		pass
		#print("=====Teardown=====")
	

if __name__ == '__main__':
	unittest.main()
