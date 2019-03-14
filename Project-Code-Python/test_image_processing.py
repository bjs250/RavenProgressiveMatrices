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

	def testIdentity(self):
		print("Testing image identity transform B-01 AB")
		problem = self.problemDict["Basic Problem B-01"]
		imageFileNameA = problem.figures["A"].visualFilename
		imageFileNameB = problem.figures["B"].visualFilename
		result = image_processing.checkIdentity(imageFileNameA,imageFileNameB)
		self.assertEqual(result,True)

		print("Testing image identity transform B-01 A1")
		problem = self.problemDict["Basic Problem B-01"]
		imageFileNameA = problem.figures["A"].visualFilename
		imageFileNameB = problem.figures["1"].visualFilename
		result = image_processing.checkIdentity(imageFileNameA,imageFileNameB)
		self.assertEqual(result,False)

		print("Testing image identity transform B-02 AB")
		problem = self.problemDict["Basic Problem B-02"]
		imageFileNameA = problem.figures["A"].visualFilename
		imageFileNameB = problem.figures["B"].visualFilename
		result = image_processing.checkIdentity(imageFileNameA,imageFileNameB)
		self.assertEqual(result,True)

		print("Testing image identity transform B-02 A1")
		problem = self.problemDict["Basic Problem B-02"]
		imageFileNameA = problem.figures["A"].visualFilename
		imageFileNameB = problem.figures["1"].visualFilename
		result = image_processing.checkIdentity(imageFileNameA,imageFileNameB)
		self.assertEqual(result,False)

		print("Testing image identity transform B-02 A2")
		problem = self.problemDict["Basic Problem B-02"]
		imageFileNameA = problem.figures["A"].visualFilename
		imageFileNameB = problem.figures["2"].visualFilename
		result = image_processing.checkIdentity(imageFileNameA,imageFileNameB)
		self.assertEqual(result,False)

		print("Testing image identity transform B-02 A4")
		problem = self.problemDict["Basic Problem B-02"]
		imageFileNameA = problem.figures["A"].visualFilename
		imageFileNameB = problem.figures["4"].visualFilename
		result = image_processing.checkIdentity(imageFileNameA,imageFileNameB)
		self.assertEqual(result,False)

		print()

	def testRotation(self):
		print("Testing image rotation transform")
		problem = self.problemDict["Basic Problem B-04"]
		imageFileNameA = problem.figures["A"].visualFilename
		imageFileNameB = problem.figures["B"].visualFilename
		result = image_processing.checkRotation(imageFileNameA,imageFileNameB,270)
		self.assertEqual(result,True)
		print()

	def testReflection(self):
		print("Testing image rotation transform")
		problem = self.problemDict["Basic Problem B-03"]
		imageFileNameA = problem.figures["A"].visualFilename
		imageFileNameB = problem.figures["B"].visualFilename
		result = image_processing.checkReflection(imageFileNameA,imageFileNameB,"left_right")
		print()
	
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
		print()
		
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
		print()

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
		print()

	def testAddition(self):
		print("Testing Addition on C-12")
		problem = self.problemDict["Basic Problem C-12"]
		result = image_processing.checkAddition(problem.figures["B"].visualFilename,problem.figures["D"].visualFilename,problem.figures["E"].visualFilename)
		self.assertEqual(result,True)

	def tearDown(self):
		pass
		#print("=====Teardown=====")

if __name__ == '__main__':
	unittest.main()