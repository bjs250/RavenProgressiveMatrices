import unittest
import os
import sys
import csv
import copy

from Agent import Agent
from ProblemSet import ProblemSet
import image_processing
import numpy as np
from RavensObject import RavensObject

def getNextLine(r):
	return r.readline().rstrip()
 
class TestUM(unittest.TestCase):
 
	def setUp(self):
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

	def testC01(self):
		print("===================C01")
		problem = self.problemDict["Basic Problem C-01"]
		self.assertEqual(3, self.agent.Solve(problem))
		print()

	def testC07(self):
		print("===================C07")
		problem = self.problemDict["Basic Problem C-07"]
		self.assertEqual(2, self.agent.Solve(problem))
		print()

	def testC12(self):
		print("===================C12")
		problem = self.problemDict["Basic Problem C-12"]
		self.assertEqual(8, self.agent.Solve(problem))
		print()	

	"""
	def testC04(self):
		print("===================C04")
		problem = self.problemDict["Basic Problem C-04"]
		self.assertEqual(8, self.agent.Solve(problem))
		print()

	def testC06(self):
		print("===================C06")
		problem = self.problemDict["Basic Problem C-06"]
		self.assertEqual(7, self.agent.Solve(problem))
		print()

	def testC10(self):
		print("===================C10")
		problem = self.problemDict["Basic Problem C-10"]
		self.assertEqual(7, self.agent.Solve(problem))
		print()
	
	def testC02(self):
		print("===================C02")
		problem = self.problemDict["Basic Problem C-02"]
		self.assertEqual(4, self.agent.Solve(problem))

		print("===================C02")
		print("Testing object pairing on Problem C02")
		problem = self.problemDict["Basic Problem C-02"]
		objects1 = problem.figures["E"].objects
		objects2 = problem.figures["F"].objects
		pairs = self.agent.pairObjects(objects1,objects2)
		result = set()
		for pair in pairs:
			result.add(self.agent.pairToString(pair))
		answer = set()
		answer.add(("i","k"))
		answer.add(("j","l"))
		self.assertEqual(result,answer,msg="Case:horizontal")	

		objects1 = problem.figures["E"].objects
		objects2 = problem.figures["H"].objects
		pairs = self.agent.pairObjects(objects1,objects2)
		result = set()
		for pair in pairs:
			result.add(self.agent.pairToString(pair))
		answer = set()
		answer.add(("i","o"))
		answer.add(("j","p"))
		self.assertEqual(result,answer,msg="Case:vertical")	
		
		print("...good")	
		
		original = copy.deepcopy(problem.figures["E"].objects)
		del_list = []
		dummycount = 0
		horizontal_pairs = self.agent.pairObjects(problem.figures["E"].objects,problem.figures["F"].objects)
		vertical_pairs = self.agent.pairObjects(problem.figures["E"].objects,problem.figures["H"].objects)

		for key,value in original.items():
			print(key,value.attributes)
		self.agent.mutateByTransform(horizontal_pairs,original,del_list,dummycount)
		for key,value in original.items():
			print(key,value.attributes)
	
		self.agent.mutateByTransform(vertical_pairs,original,del_list,dummycount)
		for key,value in original.items():
			print(key,value.attributes)

		objects3 = problem.figures["4"].objects
		for key,value in objects3.items():
			print(key,value.attributes)
		print()
	
	def testC03(self):
		print("===================C03")
		problem = self.problemDict["Basic Problem C-03"]
		self.assertEqual(4, self.agent.Solve(problem))
		print()
	
	def testC05(self):
		print("===================C05")
		problem = self.problemDict["Basic Problem C-05"]
		self.assertEqual(3, self.agent.Solve(problem))
		print()
	
	def testC09(self):
		print("===================C09")
		problem = self.problemDict["Basic Problem C-09"]
		self.assertEqual(2, self.agent.Solve(problem))
		print()
	
	def testC11(self):
		print("===================C11")
		problem = self.problemDict["Basic Problem C-11"]
		self.assertEqual(4, self.agent.Solve(problem))
		print()

	def testC08(self):
		print("===================C08")
		problem = self.problemDict["Basic Problem C-08"]
		self.assertEqual(5, self.agent.Solve(problem))
		print()
	"""

	def tearDown(self):
		pass
		#print("=====Teardown=====")


if __name__ == '__main__':
	unittest.main()