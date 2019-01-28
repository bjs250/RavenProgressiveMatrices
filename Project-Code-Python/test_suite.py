import unittest
import os
import sys
import csv

from Agent import Agent
from ProblemSet import ProblemSet
import image_processing

def getNextLine(r):
	return r.readline().rstrip()
 
class TestUM(unittest.TestCase):
 
	def setUp(self):
		print("=====Setup===== \n")
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
		print("=================================")

	def test_guessReflection(self):
		angles = ("270","0") #B3
		self.assertEqual(image_processing.guessRelection(angles),"vertical")
		angles = ("45","135") #B4
		self.assertEqual(image_processing.guessRelection(angles),"vertical")
		angles = ("45","315") #B4
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")
		angles = ("135","225") #B4
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")
		angles = ("270","180") #B5
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")
		angles = ("90","180") #B6
		self.assertEqual(image_processing.guessRelection(angles),"vertical")
		
	def test_checkReflection_horizontal(self):
		print("Testing checkReflection horizontal...")
		image = "Problems/Basic Problems B/Basic Problem B-04/A.png"
		horizontal_reflection = "Problems/Basic Problems B/Basic Problem B-04/C.png"
		result = image_processing.checkReflection(image,horizontal_reflection, "horizontal")
		self.assertTrue(result)
	
	def test_checkReflection_vertical(self):
		print("Testing checkReflection vertical...")
		image = "Problems/Basic Problems B/Basic Problem B-04/A.png"
		vertical_reflection = "Problems/Basic Problems B/Basic Problem B-04/B.png"
		result = image_processing.checkReflection(image,vertical_reflection, "vertical")
		self.assertTrue(result)	

	def test_agent_compareAttributes(self):
		print("Validate agent's compareObjects method...")
		print("Case where keys are the same...")
		object1 = self.problemDict["Basic Problem B-01"].figures["A"].objects["a"]
		object2 = self.problemDict["Basic Problem B-01"].figures["B"].objects["b"]
		answer = {}
		self.assertEqual(answer,self.agent.compareAttributes(object1.attributes,object2.attributes), msg="Case where keys are the same")

		print("Test different number of keys...")
		object1 = self.problemDict["Basic Problem B-10"].figures["A"].objects["a"]
		object2 = self.problemDict["Basic Problem B-10"].figures["A"].objects["b"]
		answer = {"inside":("b",None), "size" : ("very large", "huge")}
		self.assertEqual(answer,self.agent.compareAttributes(object1.attributes,object2.attributes), msg="object 1 has less keys than object 2")
		answer = {"inside":(None,"b"), "size" : ("huge","very large")}
		self.assertEqual(answer,self.agent.compareAttributes(object2.attributes,object1.attributes), msg="object 1 has more keys than object 2")
		
		print("Test different sets of keys...")
		object1 = self.problemDict["Basic Problem B-10"].figures["A"].objects["a"]
		object2 = self.problemDict["Basic Problem B-04"].figures["A"].objects["a"]
		answer = {'angle': (None, '45'),'fill': ('no', 'yes'),'inside': ('b', None),'shape': ('circle', 'pac-man')} 
		self.assertEqual(answer,self.agent.compareAttributes(object1.attributes,object2.attributes), msg="object 1 and 2 have same number of keys, but different values")

	def test_identity_transform(self):
		problemB1 = self.problemDict["Basic Problem B-01"]
		self.assertEqual(2,self.agent.Solve(problemB1), msg="No change to Figure A")
		self.Basic_B_Score += 1
		
	def test_angle_transform(self):
		problemB3 = self.problemDict["Basic Problem B-03"]
		self.assertEqual(1,self.agent.Solve(problemB3), msg="90 degree clockwise rotation of Figure A")      
		self.Basic_B_Score += 1

	def test_diagonal_relationship(self):
		problemB4 = self.problemDict["Basic Problem B-04"]
		self.assertEqual(3,self.agent.Solve(problemB4))
		self.Basic_B_Score += 1

	def test_one_object_multiple_transform(self):
		problemB4 = self.problemDict["Basic Problem B-05"]
		self.assertEqual(4,self.agent.Solve(problemB4))
		self.Basic_B_Score += 1

	def tearDown(self):
		print("=====Teardown=====")

if __name__ == '__main__':
	unittest.main()