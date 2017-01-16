from structure import _Corpus
from structure import _ParentDoc
from structure import _ChildDoc
from structure import _Stn
import os
import random

def loadModel(fileName, corpusObj, modelIndex):
	print "modelIndex\t", modelIndex
	f = open(fileName)

	parentObj = None

	stnNum = 0
	stnIndex = 0
	totalStnNum = 0
	for rawLine in f:
		line = rawLine.strip().split("\t")

		if stnIndex == 0:
			parentName = line[0]
			stnNum = float(line[1])

			parentObj = _ParentDoc(parentName)
			corpusObj.m_parentMap.setdefault(parentName, parentObj)
			stnIndex += 1 
		else:
			# stnName = str(int(line[0])+1)
			totalStnNum += 1
			stnName = line[0]
			stnObj = _Stn(stnName)
			stnObj.setParent2Stn(parentObj)

			parentObj.addStn2Parent(stnName, stnObj)

			lineLen = len(line)
			for i in range(1, lineLen):
				child = line[i].split(":")
				childName = child[0]
				childLikelihood = child[1]

				childObj = _ChildDoc(childName)
				childObj.setParent2Child(parentObj)

				parentObj.addChild2Parent(childName, childObj)
				stnObj.addChild2Stn(childName, childLikelihood, modelIndex)

			stnIndex += 1
			if stnNum < stnIndex:
				stnIndex = 0

	f.close() 
	print "totalStnNum\t", totalStnNum

def addModel(fileName, corpusObj, modelIndex):
	print "modelIndex\t", modelIndex
	f = open(fileName)

	parentObj = None

	likelihoodList = []

	stnNum = 0
	stnIndex = 0
	totalStnNum = 0
	for rawLine in f:
		line = rawLine.strip().split("\t")

		if stnIndex == 0:
			parentName = line[0]
			stnNum = float(line[1])

			if parentName not in corpusObj.m_parentMap.keys():
				parentObj = _ParentDoc(parentName)
				corpusObj.m_parentMap.setdefault(parentName, parentObj)
				print "previous model no parentName"
			else:
				parentObj = corpusObj.m_parentMap[parentName]
			stnIndex += 1 
		else:
			# stnName = str(int(line[0])+1)
			totalStnNum += 1
			stnName = line[0]
			stnObj = None
			if not parentObj.existStnInParent(stnName):
				stnObj = _Stn(stnName)

				stnObj.setParent2Stn(parentObj)

				parentObj.addStn2Parent(stnName, stnObj)
			else:
				stnObj = parentObj.m_stnMap[stnName]


			lineLen = len(line)
			for i in range(1, lineLen):
				child = line[i].split(":")
				childName = child[0]
				childLikelihood = float(child[1])

				if not parentObj.existChildInParent(childName):
					print "missing parent"
					childObj = _ChildDoc(childName)
					childObj.setParent2Child(parentObj)
					parentObj.addChild2Parent(childName, childObj)
					stnObj.addChild2Stn(childName, childLikelihood)
				else:
				
					childObj = parentObj.m_childDocMap[childName]
					stnObj.addChild2Stn(childName, childLikelihood, modelIndex)

			stnIndex += 1
			if stnNum < stnIndex:
				stnIndex = 0

	f.close()
	print "totalStnNum\t", totalStnNum

def outputTopComment(fileName, mergedFileName, corpusObj, modelList, topK):
	f = open(fileName, "w")
	mergedF = open(mergedFileName ,"w")

	totalStnNum = 0
	totalMergedCommentNum = 0
	totalMergedCommentPerArticleNum = 0
	totalParentNum = 0

	for parentName in corpusObj.m_parentMap.keys():
		totalParentNum += 1
		parentObj = corpusObj.m_parentMap[parentName]

		mergedCommentListPerArticle = []

		print "parent\t", parentName
		f.write(parentName+"\t"+str(len(parentObj.m_stnMap))+"\n")
		mergedF.write(parentName+"\t"+str(len(parentObj.m_stnMap))+"\n")

		for stnName in parentObj.m_stnMap.keys():
			stnObj = parentObj.m_stnMap[stnName]
			
			totalStnNum += 1

			f.write(stnName+"\t")
			mergedF.write(stnName+"\t")

			topCommentMergedList = []
			for modelIndex in range(len(modelList)):
				topCommentListByModel = topComment(stnObj, modelIndex, topK)
				f.write(modelList[modelIndex]+"\t")
				for commentID in topCommentListByModel:
					f.write(commentID+"\t")
					if commentID not in topCommentMergedList:
						topCommentMergedList.append(commentID)
					if commentID not in mergedCommentListPerArticle:
						mergedCommentListPerArticle.append(commentID)

			f.write("\n")

			totalMergedCommentNum += len(topCommentMergedList)

			for commentID in topCommentMergedList:
				mergedF.write(commentID+"\t")
			mergedF.write("\n")

		totalMergedCommentPerArticleNum += len(mergedCommentListPerArticle)


	f.close()
	mergedF.close()
	print "totalStnNum\t", totalStnNum
	print "totalMergedCommentNum\t", totalMergedCommentNum
	print "avgComment4StnNum\t", totalMergedCommentNum*1.0/totalStnNum
	print "totalParentNum\t", totalParentNum
	print "totalMergedCommentPerArticleNum\t", totalMergedCommentPerArticleNum*1.0/totalParentNum

def topComment(stnObj, modelIndex, topK):
	topChildList = []

	for childName in stnObj.m_childDocMap[modelIndex].keys():
		childLikelihood = float(stnObj.m_childDocMap[modelIndex][childName])
		stnObj.m_childDocMap[modelIndex][childName] = childLikelihood

	modelChildRankList = sorted(stnObj.m_childDocMap[modelIndex], key=stnObj.m_childDocMap[modelIndex].__getitem__, reverse=True)

	topChildNum = 0
	for childName in modelChildRankList:
		topChildNum += 1
		topChildList.append(childName)
		if topChildNum > topK:
			break
	return topChildList

if __name__ == '__main__':
	corpusObj = _Corpus()

	modelList = []

	ldaFile = "topChild4Stn_LDA.txt"
	corrLDAFile = "topChild4Stn_CorrLDA.txt"
	corrDCMLDAFile = "topChild4Stn_CorrDCMLDA.txt"
	CCTMFile = "topChild4Stn_CCTM.txt"
	SCTMFile = "topChild4Stn_SCTM.txt"

	loadModel(ldaFile, corpusObj, 0)
	modelList.append("lda")

	addModel(corrLDAFile, corpusObj, 1)
	modelList.append("corrLDA")

	addModel(corrDCMLDAFile, corpusObj, 2)
	modelList.append("corrDCMLDA")

	addModel(CCTMFile, corpusObj, 3)
	modelList.append("CCTM")

	addModel(SCTMFile, corpusObj, 4)
	modelList.append("SCTM")

	topK = 5

	mergedCommentFile = "./mergedCommentFile.txt"
	commentPoolFile = "./poolCommentFile.txt"

	outputTopComment(commentPoolFile, mergedCommentFile, corpusObj, modelList, topK)