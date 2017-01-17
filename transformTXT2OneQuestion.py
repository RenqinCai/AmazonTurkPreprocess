import json
import os
import random
import numpy as np

class parentDoc:

	def __init__(self, fileName):
		self.m_fileName = fileName;
		self.m_name = ""
		self.m_title = ""
		self.m_content = ""
		self.m_sentences = ""
		self.m_parent = ""
		self.m_childMap = {} ###childName:childObj
		self.m_mergedChildList = [] ###childName
		self.m_sentenceList = []
		self.m_jsonHashMap = {}

	def loadFile(self):
		with open(self.m_fileName) as f:
			lineNum = 0
			
			for rawLine in f:
				line = rawLine.strip()
				sentenceMap = {}
				if len(line) == 0:
					continue
			
				
				# if "___" in line:
					# break
				
				if lineNum == 0:
					self.m_title = line		
				else:	
					# line = line.split(" ")
					# line = " ".join(line[1:])
					sentenceMap.setdefault("sentence",line)
					self.m_sentenceList.append(sentenceMap)
					self.m_content += (line+" ")

				lineNum += 1

	def transformToJson(self):
		self.m_jsonHashMap.setdefault("name", self.m_name)
		self.m_jsonHashMap.setdefault("title", self.m_title)
		self.m_jsonHashMap.setdefault("content", self.m_content)
	
		self.m_jsonHashMap.setdefault("sentences", self.m_sentenceList)
		self.m_jsonHashMap.setdefault("parent", self.m_parent)
		childNames = ""		
		for child in self.m_childMap.keys():	
			childNames += child
			childNames += "\t"
		self.m_jsonHashMap.setdefault("child", childNames)

	def transformParentTxt2Question(self, childObj, iterationIndex, thresholdNum):
		message = """<h1 align="center">Rate the relevance of sentence to the comment</h1>
		      <h2>Instructions</h2>
		      <ul>
		      <li>Please carefully read the article, espeically the colored lines. The first line in the article is its title, and followed by the content of the article. The number at the front of each line is the index of each line (title is not indexed). </li>
		      <li>Please read the selected comment on this article.</li> 
		      <li>Please answer the prepared questions. Under the comment, we have selected a set of lines (include at least one sentence) from the article. Please carefully judge the relevance quality of each selected line to the comment. A selected line is considered to be relevant to the comment if the comment is talking about the same or related topic of the textual content in that line. We further categorize the relevance quality into five levels: <strong>Bad</strong> - totally irrelevant; <strong>Fair</strong> - not quite relevant; <strong>Good</strong> - somehow relevant; <strong>Excellent</strong> - relevant; <strong>Perfect</strong> - exact match. If you are not sure about your judgment in some lines, you can skip them. <br /></li>
		      <li>We have provided you an example annotation to help you better understand the task.</li>
		      </ul>
		      <br />
		      <hr />
		      <h3><font color="red">Step 1: please read the article</font></h3>
		      <h2>Article:"""
      		message += " s"+self.m_title+"</h2>"
      		message += "<p>"

      		for sentenceIndex in range(len(self.m_sentenceList)):
      			sentenceMap = self.m_sentenceList[sentenceIndex]

      			if sentenceIndex in childObj.m_sentenceList[iterationIndex*thresholdNum:(iterationIndex+1)*thresholdNum]:
				message += """<b><font color="green">["""+str(sentenceIndex)+"""] </font></b><font color="green" size="2.5" face="times">"""+sentenceMap["sentence"]+"""</font><br />"""
			else:
				message += """<font color="blue">["""+str(sentenceIndex)+"""] </font><font size="2.5" face="times">"""+sentenceMap["sentence"]+"""</font><br />"""
      		message += "</p>"

      		message +="<hr />"

      		message += """<h3><font color="red">Step 2: please read this user comment about the above news article</font></h3>"""
	    	message += "<h2>Comments:</h2>"
	    	message += """<p><font size="2.5" face="times">"""
	    	message += childObj.m_content
				# childObj = self.m_childMap[childName]
	    	message += """</font></p>"""

	    	message += """<hr />
	    	<h3><font color="red">Step 3: please answer the following questions regarding the article, the selected sentences and the comment</font></h3>"""

      		return message

	def transformChildTxt2Question(self, childObj):
	    	message = """<h3><font color="red">Step 2: please read this user comment about the above news article</font></h3>"""
	    	message += "<h2>Comments:</h2>"
	    	message += """<p><font size="2.5" face="times">"""
	    	message += childObj.m_content
				# childObj = self.m_childMap[childName]
	    	message += """</font></p>"""

    		return message


	def transformToHTML(self, outputParentDir, selectedCommentNum):
		if len(self.m_mergedChildList) < selectedCommentNum:
			print "parentName ", self.m_name, " with comments fewer than\t", selectedCommentNum
			return 

		randomChildIndexList = random.sample(range(0, len(self.m_mergedChildList)), selectedCommentNum)

		for childIndex in randomChildIndexList:
			htmlFileName = self.m_name+"_"+str(childIndex)
			outputHTMLFile = os.path.join(outputParentDir,"%s.html"%htmlFileName)

			childName = self.m_mergedChildList[childIndex]
			childObj = self.m_childMap[childName]

			f = open(outputHTMLFile, "w")
			message = """<html><head>
			<style>
			.fieldsetStyle{
			width:70%
			}
			</style>
			</head><body>"""
			message += """<font color="red">Thanks for your annotation, which is very important to our work.
		Please follow the following steps to finish the annotation.
		<br>
		<font size="4">
		1. Read the article. The first line in the article is the title, which is not associated with any number at the beginning. Then the following lines are the content of the article. The number at the front of each line is the index of each line. <br>

		2. Then read the comments on this article. The number at the front of each comment is the index of the comment within comments and the number does not influence the annotation task. <br>

		3. For lines listed under the question section, please give the relevance score of each line to the comment. The relevance score is in the range from 0 to 4. Notice that 0 means totally irrelevant, 1 means not relevant, 2 fair relevant, 3 relevant, 4 abosolutely relevant. If you are not sure, the default score will be 2.<br>

		4. If you still do not understand how to finish the task, please follow the example provided.
		</font>
		<br>

		Thanks so much for your effort.</font><br><br><font color="red">*********Please read the article*********</font><br><b>Article:</b><br>"""
			message += """<b><font size=4>"""+self.m_title+"""</font></b><br>"""
			for sentenceIndex in range(len(self.m_sentenceList)):
				sentenceMap = self.m_sentenceList[sentenceIndex]
				if sentenceIndex in childObj.m_sentenceList:
					# print self.m_name
					# print childName
					# print "bold sentence\t", sentenceIndex
					message += """<font size=2><b>["""+str(sentenceIndex)+"""]</b>   </font>"""
					message += """<font size=3 color="green"><b>"""+sentenceMap["sentence"]+"""</b></font><br>"""
					# print debug
				else:
					message += """<font size=2>["""+str(sentenceIndex)+"""]   </font>"""
					message += """<font size=3>"""+sentenceMap["sentence"]+"""</font><br>"""

				# f.write(sentenceIndex+"\t")
				# f.write(sentenceMap["sentence"])
				# f.write("\n")

			message += """<br><br><br><font color="red">*********Please read the comment*********</font><br><b>Comments:</b><br>"""

		# for childIndex in randomChildIndexList:
			
			message +="""<fieldset><font size=2>["""+childName+ """]    </font>"""
			# childObj = self.m_childMap[childName]
			message += """<font size=4>"""+childObj.m_content +"""</font><br><fieldset> <legend><font color="red">Please provide the relevance score of the comment with respect to each line</font></legend>"""

			# message += """<font size=4>"""+childObj.m_content +"""</font><br>"""

			for stnIndex in childObj.m_sentenceList:
				message += """<fieldset class="fieldsetStyle"><b>relevance </b> to <font color="green">[line  """+str(stnIndex) + """]</font> <input type="radio" name="stnIndex" value="relevance">totally irrelevant &nbsp;&nbsp;<input type="radio" name="stnIndex" value="relevance">not relevant &nbsp;&nbsp;<input type="radio" name="stnIndex" value="relevance">fair relevant &nbsp;&nbsp;<input type="radio" name="stnIndex" value="relevance">relevant &nbsp;&nbsp;<input type="radio" name="stnIndex" value="relevance">abosolutely relevant &nbsp;&nbsp;<br></fieldset>"""
			# message += """</fieldset></fieldset>"""			
			message += """</fieldset></fieldset>"""


			message += "</body></html>"
			f.write(message)
			f.close()

	def setName(self, name):
		self.m_name = name

	# def addParent(self, parentName):
	# 	self.m_parent = parentName

	def addChild(self, childObj):
		self.m_childMap.setdefault(childObj.m_name, childObj)

class childDoc:
	
	def __init__(self):
		self.m_name = ""
		self.m_title = "" #always null
		self.m_content = ""
		self.m_parent = "" 
		self.m_childList = [] #always null
		self.m_jsonHashMap = {}
		self.m_sentenceList = []

	def transformToJson(self):
		self.m_jsonHashMap.setdefault("name", self.m_name)
		self.m_jsonHashMap.setdefault("title", self.m_title)
		self.m_jsonHashMap.setdefault("content", self.m_content)
		self.m_jsonHashMap.setdefault("parent", self.m_parent)
		childNames = ""
		for child in self.m_childList:	
			childNames += child
			childNames += "\t"
		self.m_jsonHashMap.setdefault("child", childNames)

	def transformToHTML(self, outputHTMLFile):
		f = open(outputHTMLFile, "w")
		

		f.close()	

	def setName(self, parentName, name):
		self.m_name = parentName+"_"+name
		
	def setParent(self, parentName):
		self.m_parent = parentName

	def setContent(self, content):
		self.m_content = content

	# def addChild(self, childName):
	# 	self.m_childList.append(childName)


#parentChildFlag == 1, child
#parentChildFlag == 0, parent
class corpus:
	def __init__(self, parentDir, childDir):
		self.m_parentDir = parentDir
		self.m_childDir = childDir
		self.m_parentMap = {}
		self.m_parentObjectCollection = []
		self.m_childObjectCollection = []
		
	def loadParentDirectory(self):
		
		for fileName in os.listdir(self.m_parentDir):
			if fileName.endswith(".txt"):
				parentDocObj = parentDoc(os.path.join(self.m_parentDir, fileName))
				parentDocObj.setName(fileName.replace(".txt", "").replace("Article", ""))
				parentDocObj.loadFile()
				self.m_parentMap.setdefault(fileName, parentDocObj)
				
				self.m_parentObjectCollection.append(parentDocObj)

				

	def loadChildDirectory(self):
		
		for fileName in os.listdir(self.m_childDir):
			if fileName.endswith(".txt"):
				
				with open(os.path.join(self.m_childDir,fileName)) as f:
					commentNum = 1
					for rawLine in f:
						#line = rawLine.strip().split("}")
						line = rawLine.strip()
						
						if len(line) == 0:
							continue
						
						if not line:
							continue
						#line = " ".join(line[1:]).strip()
						
						# if "___" in line:
							# break
						
						# print "line:___",line 
						
						childDocObj = childDoc()
						childDocObj.setContent(line)
						
					#	print childDocObj.m_ID
				
						parentFileName = fileName.replace("Comments", "Article")
						childDocObj.setName(parentFileName.replace(".txt", "").replace("Article", ""), str(commentNum))
						correspondParentDocObj = self.m_parentMap[parentFileName]
						correspondParentID = correspondParentDocObj.m_name
						childDocObj.setParent(correspondParentID)

						correspondParentDocObj.addChild(childDocObj)
						self.m_childObjectCollection.append(childDocObj)
					
						commentNum += 1
				

	def writeJson(self, outputParentDir, outputChildDir):
		self.writeParentJson(outputParentDir)
		self.writeChildJson(outputChildDir)

	def writeHTML(self, outputParentDir):
		for obj in self.m_parentObjectCollection:
			jsonFile = os.path.join(outputParentDir,"%s.html"%obj.m_name)
			obj.transformToHTML(jsonFile)

	def writeHTML(self, outputParentDir, selectedParentNum, selectedCommentNum):

		randomParentIndexList = random.sample(range(0, len(self.m_parentObjectCollection)), selectedParentNum)
		
		for parentIndex in randomParentIndexList:
			obj = self.m_parentObjectCollection[parentIndex]
			obj.transformToHTML(outputParentDir, selectedCommentNum)


			###add tranformation for child
	
	def transformQuestionText(self, childName, sentenceIndex, stepIndex):
		message = """Question """+str(stepIndex-2)+""": please judge the relevance quality of this comment to <b><font color="green"> line """+str(sentenceIndex)+""" </font></b>in the article"""
		return message


	def generateSanityQuestion(self, childObj, sanityCheckQuestionIndex, iterationIndex, thresholdNum, stepIndex):
		sentenceIndex1 = childObj.m_sentenceList[iterationIndex*thresholdNum]
		sentenceIndex2 = childObj.m_sentenceList[iterationIndex*thresholdNum+1]
		message = """Question """+str(stepIndex-2)+""": please compare the relative relevance of the comment between<b><font color="green"> line """+ str(sentenceIndex1)+ """</font></b> and <b><font color="green"> line """+ str(sentenceIndex2)+"""</font></b>"""
		return message

	def writeQuestion(self, outputQuestionDir, selectedParentNum, selectedCommentNum, thresholdNum):

		randomParentIndexList = random.sample(range(0, len(self.m_parentObjectCollection)), selectedParentNum)


		questionID = ""
		questionNum = 0
		pageNum = 0
		articleNum = 0
		sanityCheckQuestionNum = 0  ##this should be the same as pageNum
		for parentIndex in randomParentIndexList:
		
			obj = self.m_parentObjectCollection[parentIndex]
			if len(obj.m_mergedChildList) < selectedCommentNum:
				print "parentName ", obj.m_name, " with comments fewer than\t", selectedCommentNum
				continue 


			articleNum += 1
			randomChildIndexList = random.sample(range(0, len(obj.m_mergedChildList)), selectedCommentNum)

			for childIndex in randomChildIndexList:
				childName = obj.m_mergedChildList[childIndex]
				childObj = obj.m_childMap[childName]

				iterationNum = len(childObj.m_sentenceList)/thresholdNum
				for iterationIndex in range(iterationNum+1):
					sanityCheckQuestionIndex = (iterationIndex)*thresholdNum+2
					randomBound = np.min([(iterationIndex+1)*thresholdNum, len(childObj.m_sentenceList)])
					
					if (iterationIndex)*thresholdNum+2 < randomBound:
						sanityCheckQuestionIndex = random.randint((iterationIndex)*thresholdNum+2, randomBound)
				
					stepIndex = 3
					pageNum += 1
					questionFileName = obj.m_name+"_"+str(childIndex)
					if(iterationIndex>0):
						questionFileName = obj.m_name+"_"+str(childIndex)+"_"+str(iterationIndex)
				
					outputQuestionFile = os.path.join(outputQuestionDir,"%s.question"%questionFileName)
					f = open(outputQuestionFile, "w")
					print "outputQuestionFile\t", outputQuestionFile
					f.write("""<?xml version="1.0" encoding="UTF-8"?>""")
					f.write("\n")
					f.write("""<QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionForm.xsd">""")
				
					f.write("""<Overview>""")
					f.write("\n")
					f.write("""<FormattedContent><![CDATA[""")
					articleAndComment = obj.transformParentTxt2Question(childObj, iterationIndex, thresholdNum)
					f.write(articleAndComment)
					f.write("""]]></FormattedContent>""")
					f.write("""</Overview>""")

					for stnIndexInList in range(iterationIndex*thresholdNum, (iterationIndex+1)*thresholdNum+1):
						if stnIndexInList > len(childObj.m_sentenceList):
							break;

						if stnIndexInList == len(childObj.m_sentenceList):
							if stnIndexInList < sanityCheckQuestionIndex:
								break;

						if stnIndexInList == sanityCheckQuestionIndex:
							questionID = childName + "_sanity_"+str(iterationIndex)
							print questionID

							questionNum += 1
							sanityCheckQuestionNum += 1

							f.write("""<Question>
				  			<QuestionIdentifier>""")
							f.write(questionID)
							f.write("""</QuestionIdentifier>""")
							f.write("""
							<QuestionContent>
				     <FormattedContent><![CDATA[""")
							
							questionText = self.generateSanityQuestion(childObj, sanityCheckQuestionIndex, iterationIndex, thresholdNum, stepIndex)
							stepIndex += 1
							f.write(questionText)
							f.write("""]]></FormattedContent>""")
				    			f.write("""</QuestionContent>
							    <AnswerSpecification>
							      <SelectionAnswer>
							        <MinSelectionCount>1</MinSelectionCount>
							        <MaxSelectionCount>1</MaxSelectionCount>
							        <StyleSuggestion>radiobutton</StyleSuggestion>
							        <Selections>""")
				    			f.write(""" <Selection>
							            <SelectionIdentifier>0</SelectionIdentifier>""")
				    			f.write("""<FormattedContent><![CDATA[ comment is more relevant to line """)
				    			f.write(str(childObj.m_sentenceList[iterationIndex*thresholdNum]))
				    			print "sanity vs\t", str(childObj.m_sentenceList[iterationIndex*thresholdNum]), "\t", str(childObj.m_sentenceList[iterationIndex*thresholdNum+1])
							f.write("""]]></FormattedContent> </Selection>""")
							f.write(""" <Selection>
							            <SelectionIdentifier>1</SelectionIdentifier>""")
				    			f.write("""<FormattedContent><![CDATA[ comment is more relevant to line """)
				    			f.write(str(childObj.m_sentenceList[iterationIndex*thresholdNum+1]))
							f.write("""]]></FormattedContent> </Selection>""")
							f.write(""" <Selection>
							            <SelectionIdentifier>2</SelectionIdentifier>""")
				    			f.write("""<FormattedContent><![CDATA[ comment has the same relevance to these two lines """)
							f.write("""]]></FormattedContent> </Selection>""")
							f.write(""" <Selection>
							            <SelectionIdentifier>2</SelectionIdentifier>""")
				    			f.write("""<FormattedContent><![CDATA[ comment is irrelevant to these two lines """)
							f.write("""]]></FormattedContent> </Selection>""")
							f.write("""</Selections>
							      </SelectionAnswer>
							    </AnswerSpecification>
				  				</Question>""")

						else:
							print "stnIndexInList\t", stnIndexInList, "\t sanityCheckQuestionIndex\t", sanityCheckQuestionIndex, "len(m_sentenceList)\t", len(childObj.m_sentenceList)
							if stnIndexInList > sanityCheckQuestionIndex:
								stnIndexInList -= 1
							sentenceIndex = childObj.m_sentenceList[stnIndexInList]

					# for sentenceIndex in childObj.m_sentenceList[iterationIndex*thresholdNum:(iterationIndex+1)*thresholdNum]:
							questionID = childName+"_"+str(sentenceIndex)
							print questionID

							questionNum += 1
							
							f.write("""<Question>
				  			<QuestionIdentifier>""")
							f.write(questionID)
							f.write("""</QuestionIdentifier>""")
							f.write("""
							<QuestionContent>
				     <FormattedContent><![CDATA[""")
							
							questionText = self.transformQuestionText(childName, sentenceIndex, stepIndex)
							stepIndex += 1
							f.write(questionText)
							f.write("""]]></FormattedContent>""")
				    			f.write("""</QuestionContent>
							    <AnswerSpecification>
							      <SelectionAnswer>
							        <MinSelectionCount>1</MinSelectionCount>
							        <MaxSelectionCount>1</MaxSelectionCount>
							        <StyleSuggestion>radiobutton</StyleSuggestion>
							        <Selections>
							          <Selection>
							            <SelectionIdentifier>0</SelectionIdentifier>
							            <Text>Bad</Text>
							          </Selection>
							          <Selection>
							            <SelectionIdentifier>1</SelectionIdentifier>
							            <Text>Fair</Text>
							          </Selection>
							           <Selection>
							            <SelectionIdentifier>2</SelectionIdentifier>
							            <Text>Good</Text>
							          </Selection>
							           <Selection>
							            <SelectionIdentifier>3</SelectionIdentifier>
							            <Text>Excellent</Text>
							          </Selection>
									      <Selection>
							            <SelectionIdentifier>4</SelectionIdentifier>
							            <Text>Perfect</Text>
							          </Selection>
							        </Selections>
							      </SelectionAnswer>
							    </AnswerSpecification>
				  				</Question>""")

					f.write("""</QuestionForm>""")
					f.close()
		print "questionNum\t", questionNum, "pageNum\t", pageNum, "\t articleNum\t", articleNum

	def writeParentJson(self, outputParentDir):
	
		for obj in self.m_parentObjectCollection:
			jsonFile = os.path.join(outputParentDir,"%s.json"%obj.m_name)
			outFile = open(jsonFile, 'w')
			obj.transformToJson()
			json.dump(obj.m_jsonHashMap, outFile)
			outFile.close()
			
	def writeChildJson(self, outputChildDir):
	
		for obj in self.m_childObjectCollection:
			jsonFile = os.path.join(outputChildDir,"%s.json"%obj.m_name)
			outFile = open(jsonFile, 'w')
			obj.transformToJson()
			json.dump(obj.m_jsonHashMap, outFile)
			outFile.close()

	def loadSelectedComment(self, inputCommentFile):
		f = open(inputCommentFile)

		stnNum = 0
		stnIndex = 0
		totalStnNum = 0
		parentObj = None
		for rawLine in f:
			line = rawLine.strip().split("\t")

			if stnIndex == 0:
				parentName = line[0]
				parentName = "Article"+parentName+".txt"
				stnNum = float(line[1])
				# print line

				if parentName not in self.m_parentMap.keys():
					print "error"
				else:
					parentObj = self.m_parentMap[parentName]

				stnIndex += 1
			else:
				totalStnNum += 1
				stnNameIndex = int(line[0])-1

				lineLen = len(line)
				for i in range(1, lineLen):
					child = line[i]
					if child not in parentObj.m_mergedChildList:
						parentObj.m_mergedChildList.append(child)
					childObj = parentObj.m_childMap[child]
					childObj.m_sentenceList.append(stnNameIndex)

				stnIndex += 1
				if stnNum < stnIndex:
					stnIndex = 0

		f.close()
		print "totalStnNum\t", totalStnNum


if __name__=="__main__":
	parentDir = "./Data/YahooArticles"
	childDir = "./Data/YahooComments"
	outputQuestionDir = "./outputQuestion/"		
	
	YahooNewsCorpus = corpus(parentDir, childDir)
	YahooNewsCorpus.loadParentDirectory()
	YahooNewsCorpus.loadChildDirectory()

	selectedParentNum = 5
	selectedCommentNum  = 15
	selectedStnNum = 3
	pageQuestionThresholdNum = 5
	selectCommentFile = "./Data/mergedCommentFile.txt"
	YahooNewsCorpus.loadSelectedComment(selectCommentFile)

	filelist = [ f for f in os.listdir(outputQuestionDir) if f.endswith(".question") ]
	for f in filelist:
		print f
		os.remove(os.path.join(outputQuestionDir, f))
	YahooNewsCorpus.writeQuestion(outputQuestionDir, selectedParentNum, selectedCommentNum, pageQuestionThresholdNum)
	# YahooNewsCorpus.writeJson(outputParentDir, outputChildDir)


# with open('data.json', 'w') as outFile:
# 	json.dump(data, outFile)