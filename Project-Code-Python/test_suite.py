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

	def test_fillTransform(self):
		#flip occurs
		attributes = {}
		attributes["fill"] = "no"
		transform = ("yes","no")
		result = self.agent.fillTransform(attributes,transform)
		self.assertTrue(result["fill"],"yes")

		attributes = {}
		attributes["fill"] = "yes"
		transform = ("yes","no")
		result = self.agent.fillTransform(attributes,transform)
		self.assertTrue(result["fill"],"no")

		attributes = {}
		attributes["fill"] = "no"
		transform = ("no","yes")
		result = self.agent.fillTransform(attributes,transform)
		self.assertTrue(result["fill"],"yes")

		attributes = {}
		attributes["fill"] = "yes"
		transform = ("no","yes")
		result = self.agent.fillTransform(attributes,transform)
		self.assertTrue(result["fill"],"no")

		#nothing should occur
		attributes = {}
		attributes["fill"] = "no"
		transform = ("yes","yes")
		result = self.agent.fillTransform(attributes,transform)
		self.assertTrue(result["fill"],"no")

		attributes = {}
		attributes["fill"] = "no"
		transform = ("no","no")
		result = self.agent.fillTransform(attributes,transform)
		self.assertTrue(result["fill"],"no")

		attributes = {}
		attributes["fill"] = "yes"
		transform = ("no","no")
		result = self.agent.fillTransform(attributes,transform)
		self.assertTrue(result["fill"],"yes")

		attributes = {}
		attributes["fill"] = "yes"
		transform = ("yes","yes")
		result = self.agent.fillTransform(attributes,transform)
		self.assertTrue(result["fill"],"yes")

	def test_guessReflection(self):
		
		# Quadrant 1 interior
		angles = ("45","135") #B4
		self.assertEqual(image_processing.guessRelection(angles),"vertical")
		angles = ("45","315") #B4
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")

		# Quadrant 2 interior
		angles = ("135","225") #B4
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")
		angles = ("135","45") 
		self.assertEqual(image_processing.guessRelection(angles),"vertical")

		# Quadrant 3 interior
		angles = ("225","135") 
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")
		angles = ("225","315") 
		self.assertEqual(image_processing.guessRelection(angles),"vertical")

		# Quadrant 4 interior
		angles = ("315","45") 
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")
		angles = ("315","225") 
		self.assertEqual(image_processing.guessRelection(angles),"vertical")

		# Quadrant 1 corner
		angles = ("90","180") #B6
		self.assertEqual(image_processing.guessRelection(angles),"vertical")
		angles = ("90","0") 
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")

		# Quadrant 2 corner
		angles = ("180","270") 
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")
		angles = ("180","90") 
		self.assertEqual(image_processing.guessRelection(angles),"vertical")

		# Quadrant 3 corner
		angles = ("270","0") #B3
		self.assertEqual(image_processing.guessRelection(angles),"vertical")
		angles = ("270","180") #B5
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")

		# Quadrant 4 corner
		angles = ("0","90") 
		self.assertEqual(image_processing.guessRelection(angles),"horizontal")
		angles = ("0","270") 
		self.assertEqual(image_processing.guessRelection(angles),"vertical")

	def test_alignment_transform(self):
		# horizontal flip
		attributes = {}
		attributes["alignment"] = "bottom-right"
		transform = ("top-left","top-right")
		result = self.agent.alignmentTransform(attributes,transform)
		self.assertTrue(result["alignment"],"bottom-left")

		# symmetric horizontal flip
		attributes = {}
		attributes["alignment"] = "bottom-right"
		transform = ("top-right","top-left")
		result = self.agent.alignmentTransform(attributes,transform)
		self.assertTrue(result["alignment"],"bottom-left")

		# vertical flip
		attributes = {}
		attributes["alignment"] = "top-left"
		transform = ("top-left","bottom-left")
		result = self.agent.alignmentTransform(attributes,transform)
		self.assertTrue(result["alignment"],"bottom-left")

		# symmetric vertical flip
		attributes = {}
		attributes["alignment"] = "top-left"
		transform = ("bottom-left","top-left")
		result = self.agent.alignmentTransform(attributes,transform)
		self.assertTrue(result["alignment"],"bottom-left")

		#double
		attributes = {}
		attributes["alignment"] = "top-right"
		transform = ("bottom-left","top-right")
		result = self.agent.alignmentTransform(attributes,transform)
		self.assertTrue(result["alignment"],"bottom-left")

		#none
		attributes = {}
		attributes["alignment"] = "top-right"
		transform = ("bottom-left","bottom-left")
		result = self.agent.alignmentTransform(attributes,transform)
		self.assertTrue(result["alignment"],"top-right")

	def test_size_transform(self):
		# increase
		attributes = {}
		attributes["size"] = "medium"
		transform = ("small","large")
		result = self.agent.sizeTransform(attributes,transform)
		self.assertTrue(result["size"],"very-large")

		# increase
		attributes = {}
		attributes["size"] = "medium"
		transform = ("large","small")
		result = self.agent.sizeTransform(attributes,transform)
		self.assertTrue(result["size"],"very-small")

		# none
		attributes = {}
		attributes["size"] = "medium"
		transform = ("large","large")
		result = self.agent.sizeTransform(attributes,transform)
		self.assertTrue(result["size"],"medium")
		
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

	def test_one_object_multiple_transform2(self):
		problemB7 = self.problemDict["Basic Problem B-07"]
		self.assertEqual(6, self.agent.Solve(problemB7))

	def test_one_object_multiple_transform_3(self):
		problemB9 = self.problemDict["Basic Problem B-09"]
		self.assertEqual(5, self.agent.Solve(problemB9))

	def tearDown(self):
		pass
		#print("=====Teardown=====")

if __name__ == '__main__':
	unittest.main()