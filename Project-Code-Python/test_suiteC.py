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
		self.Basic_B_Score = 0

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

	def test3x3symmetryC04(self):
		print("Testing 3x3 G/C check C-04")
		problem = self.problemDict["Basic Problem C-04"]
		result = image_processing.checkRotation(problem.figures["G"].visualFilename,problem.figures["C"].visualFilename,90)
		self.assertEqual(result,True)

		result = image_processing.checkRotation(problem.figures["2"].visualFilename,problem.figures["2"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["4"].visualFilename,problem.figures["4"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["5"].visualFilename,problem.figures["5"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["6"].visualFilename,problem.figures["6"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["7"].visualFilename,problem.figures["7"].visualFilename,90)
		self.assertEqual(result,False)

		result = image_processing.checkRotation(problem.figures["1"].visualFilename,problem.figures["1"].visualFilename,90)
		self.assertEqual(result,True)
		result = image_processing.checkRotation(problem.figures["3"].visualFilename,problem.figures["3"].visualFilename,90)
		self.assertEqual(result,True)
		result = image_processing.checkRotation(problem.figures["8"].visualFilename,problem.figures["8"].visualFilename,90)
		self.assertEqual(result,True)
		
	def test3x3symmetryC06(self):
		print("Testing 3x3 G/C check C-06")
		problem = self.problemDict["Basic Problem C-06"]
		result = image_processing.checkRotation(problem.figures["G"].visualFilename,problem.figures["C"].visualFilename,90)
		self.assertEqual(result,True)

		result = image_processing.checkRotation(problem.figures["1"].visualFilename,problem.figures["1"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["2"].visualFilename,problem.figures["2"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["3"].visualFilename,problem.figures["3"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["5"].visualFilename,problem.figures["5"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["8"].visualFilename,problem.figures["8"].visualFilename,90)
		self.assertEqual(result,False)

		result = image_processing.checkRotation(problem.figures["4"].visualFilename,problem.figures["4"].visualFilename,90)
		self.assertEqual(result,True)
		result = image_processing.checkRotation(problem.figures["6"].visualFilename,problem.figures["6"].visualFilename,90)
		self.assertEqual(result,True)
		result = image_processing.checkRotation(problem.figures["7"].visualFilename,problem.figures["7"].visualFilename,90)
		self.assertEqual(result,True)

	def test3x3symmetryC10(self):
		print("Testing 3x3 G/C check C-10")
		problem = self.problemDict["Basic Problem C-10"]
		result = image_processing.checkRotation(problem.figures["G"].visualFilename,problem.figures["C"].visualFilename,90)
		self.assertEqual(result,True)

		result = image_processing.checkRotation(problem.figures["1"].visualFilename,problem.figures["1"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["2"].visualFilename,problem.figures["2"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["3"].visualFilename,problem.figures["3"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["4"].visualFilename,problem.figures["4"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["6"].visualFilename,problem.figures["6"].visualFilename,90)
		self.assertEqual(result,False)
		result = image_processing.checkRotation(problem.figures["8"].visualFilename,problem.figures["8"].visualFilename,90)
		self.assertEqual(result,False)

		result = image_processing.checkRotation(problem.figures["5"].visualFilename,problem.figures["5"].visualFilename,90)
		self.assertEqual(result,True)
		result = image_processing.checkRotation(problem.figures["7"].visualFilename,problem.figures["7"].visualFilename,90)
		self.assertEqual(result,True)

	def testC04(self):
		print("===================C04")
		problem = self.problemDict["Basic Problem C-04"]
		self.assertEqual(8, self.agent.Solve(problem))

	def testC06(self):
		print("===================C06")
		problem = self.problemDict["Basic Problem C-06"]
		self.assertEqual(7, self.agent.Solve(problem))

	def testC10(self):
		print("===================C10")
		problem = self.problemDict["Basic Problem C-10"]
		self.assertEqual(7, self.agent.Solve(problem))

	def testC02(self):
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
	


	def tearDown(self):
		pass
		#print("=====Teardown=====")


if __name__ == '__main__':
	unittest.main()