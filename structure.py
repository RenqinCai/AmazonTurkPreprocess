##model1: Bm25
##model2: lda
##model3: corrLDA
##model4: sctm
##model5: ACCTM
##


class _ParentDoc:
	def __init__(self, name):
		self.m_name = name
		self.m_stnMap = {} ##stnIndex, stnObj
		self.m_childDocMap = {}  ###childName, childObj
		self.m_stnList = []
		self.m_childList = []
		self.m_copiedStn4ChildList = []

	def getName(self):
		return self.m_name

	def addStn2Parent(self, stnIndex, stnObj):
		self.m_stnMap.setdefault(stnIndex, stnObj)

	def addChild2Parent(self, childName, childObj):
		self.m_childDocMap.setdefault(childName, childObj)

	def selectChild2Parent(self, childName):
		self.m_childList.append(childName)

	def selectStn2Parent(self, stnIndex):
		self.m_stnList.append(stnIndex)

	def existStnInParent(self, stnIndex):
		if stnIndex in self.m_stnMap.keys():
			return True
		else:
			return False

	def existChildInParent(self, childName):
		if childName in self.m_childDocMap.keys():
			return True
		else:
			return False

class _ChildDoc:
	def __init__(self, name):
		self.m_name = name
		self.m_parent = None
		self.m_stnMap = {} ###modelIndex:stnIndex:sim
		self.m_APMap = {} ###modelIndex:AP
		self.m_groundTruthStnList=[]

	def getName(self):
		return self.m_name

	def addStn2Child(self, stnIndex, sim, modelIndex):
		if modelIndex not in self.m_stnMap.keys():
			self.m_stnMap.setdefault(modelIndex, {})
			self.m_stnMap[modelIndex].setdefault(stnIndex, sim)
		else:
			self.m_stnMap[modelIndex].setdefault(stnIndex, sim)

	def setParent2Child(self, parentObj):
		self.m_parent = parentObj

	def addStn2Ground(self, stnIndex):
		self.m_groundTruthStnList.append(stnIndex)


class _Stn:
	def __init__(self, name):
		self.m_name = name
		self.m_parent = None
		self.m_groundTruthChildList = []
		self.m_childDocMap = {} ##modelIndex:childName:likelihood
		self.m_APMap = {} ###modelIndex:AP
		
	def getName(self):
		return self.m_name

	def addChild2Stn(self, childName, likelihood, modelIndex):
		if modelIndex not in self.m_childDocMap.keys():
			self.m_childDocMap.setdefault(modelIndex, {})
			self.m_childDocMap[modelIndex].setdefault(childName, likelihood)
		else:
			self.m_childDocMap[modelIndex].setdefault(childName, likelihood)

	def setParent2Stn(self, parentObj):
		self.m_parent = parentObj

	def addChild2Ground(self, childName):
		self.m_groundTruthChildList.append(childName)

class _Corpus:
	def __init__(self):
		self.m_parentMap = {}

	def addParent2Corpus(self, parentName, parentObj):
		self.m_parentMap.setdefault(parentName, parentObj)



