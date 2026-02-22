#! /bin/python3
from os import listdir, mkdir
from os.path import isfile, join, splitext, isdir, relpath
import re
import json

def createDirIfNotReal(path):
	if not isdir(path):
		mkdir(path)


createDirIfNotReal("./docs/")
createDirIfNotReal("./docs/subpage/")
createDirIfNotReal("./docs/js/")

TARGET_DIRECTORY_PARSE = "./togen/"

foundFiles = []
allowedExt = {
	".lua": True,
}

bannedFolders = {
	".vscode": True,
	".git": True,
}

def recursive_find(path):
	filesGet = listdir(path)

	for file in filesGet:
		filePath = join(path, file)

		if isfile(filePath):
			fName, fExt = splitext(file)

			if not (fExt in allowedExt):
				continue

			foundFiles.append(filePath)
		else:
			if (file in bannedFolders):
				continue

			recursive_find(filePath)
	

recursive_find(TARGET_DIRECTORY_PARSE)


fileDefs = []
def push_current_file_def(currDef):
	fileDefs.append(currDef)
	currDef = {}

currExampleTitle = "None"
currExampleLines = ""
def parse_at(atContent, currDef):
	global currExampleTitle
	global currExampleLines
	#print(f"|{atContent}")

	atType = re.search(r"@([^ \n]+) ?(.*)", atContent)
	if atType == None:
		return
		
	atTypeStr = atType.group(1)
	atRestStr = atType.group(2)
	
	if not "params" in currDef:
		currDef["params"] = []

	if not "returns" in currDef:
		currDef["returns"] = []

	if not "examples" in currDef:
		currDef["examples"] = []
	
	# crime here let's gooo
	# realms
	if atTypeStr == "client":
		currDef["realm"] = "client"
	elif atTypeStr == "server":
		currDef["realm"] = "server"
	elif atTypeStr == "shared":
		currDef["realm"] = "shared"
	# flags
	elif atTypeStr == "internal":
		currDef["internal"] = True
	elif atTypeStr == "deprecated":
		currDef["deprecated"] = True

	# warns and comments
	elif atTypeStr == "warn":
		currDef["warn"] = atRestStr
	elif atTypeStr == "comment":
		currDef["comment"] = atRestStr

	# category parsing
	elif atTypeStr == "group":
		currDef["group"] = atRestStr
	elif atTypeStr == "category":
		currDef["category"] = atRestStr
		

	# params & rets
	elif atTypeStr == "param":
		paramMatch = re.search(r"([^ ]+) ([^ ]+) ?(.*)", atRestStr)
		paramName = paramMatch.group(1)
		paramType = paramMatch.group(2)
		paramDesc = paramMatch.group(3)

		currDef["params"].append({
			"name": paramName,
			"type": paramType,
			"desc": paramDesc,
		})
	elif atTypeStr == "return":
		retMatch = re.search(r"([^ ]+) ([^ ]+) ?(.*)", atRestStr)
		retType = retMatch.group(1)
		retName = retMatch.group(2)
		retDesc = retMatch.group(3)

		currDef["returns"].append({
			"name": retName,
			"type": retType,
			"desc": retDesc,
		})
	# example parsing
	elif atTypeStr == "example_begin":
		currExampleTitle = atRestStr
		currExampleLines = ""
	elif atTypeStr == "example":
		currExampleLines += atRestStr + "\n"
	elif atTypeStr == "example_end":
		currDef["examples"].append({
			"title": currExampleTitle,
			"content": currExampleLines
		})

	



def obtain_file_defs(filePath):
	fPtr = open(filePath, "r")

	messageDesc = ""
	foundFlag = False
	sendableFlag = False

	currentDef = {}
	lineAcc = 0
	for line in fPtr:
		lineAcc = lineAcc + 1
		if not foundFlag:
			hasThree = re.search(r"-{3}([^@\n]*)", line)

			if hasThree == None:
				continue

			foundFlag = True
			messageDesc = hasThree.group(1)
			currentDef["desc"] = messageDesc
		else:
			hasAt = re.search(r"-{3}(@.*)", line)

			if hasAt == None:
				foundFlag = False

				sendableFlag = True
				sendableFlag = sendableFlag and "realm" in currentDef
				sendableFlag = sendableFlag and "category" in currentDef
				sendableFlag = sendableFlag and len(currentDef["desc"]) > 0


				if sendableFlag:
					sigMatch = re.search(r"function ([^(]+)", line)
					sig = sigMatch.group(1)
					currentDef["sig"] = sig

					splitSig = sig.split(".")
					currentDef["lonesig"] = splitSig[len(splitSig) - 1]
					currentDef["src"] = relpath(filePath, TARGET_DIRECTORY_PARSE)
					currentDef["line"] = lineAcc

					push_current_file_def(currentDef)
					currentDef = {}
				continue

			atContent = hasAt.group(1)
			parse_at(atContent, currentDef)
			


	fPtr.close()


for filePath in foundFiles:
	obtain_file_defs(filePath)



#for defGet in fileDefs:
	#print(defGet)

with open("docs/js/defs.json", "w") as fPtr:
	json.dump(fileDefs, fPtr)


# generate html pages
# template for funcs
templateStr = ""
with open("templates/function.html", "r") as fPtr:
	templateStr = fPtr.read()


def fillTemplate(funcDef):
	newStr = templateStr

	# 1 -> page title lone sig
	# 2 -> realm
	# 3 -> inline func
	# 4 -> path & line
	# 5 -> description
	# 6 -> params
	# 7 -> returns
	# 8 -> examples

	loneFuncStr = ""
	for i in range(0, len(funcDef["returns"])):
		ret = funcDef["returns"][i]
		loneFuncStr += (ret["type"] + ((i != (len(funcDef["returns"]) - 1)) and ", " or " "))

	loneFuncStr += funcDef["sig"] + "("

	for i in range(0, len(funcDef["params"])):
		param = funcDef["params"][i]
		loneFuncStr += (param["type"] + " " + param["name"] + ((i != (len(funcDef["params"]) - 1)) and ", " or ""))
	loneFuncStr += ")"

	descStr = funcDef["desc"]
	if "internal" in funcDef:
		descStr += f"""\n<div class="internal-block">\n<h3>Internal</h3>\nThis function is internal, so you probably shouldn't use it!</div>\n"""

	if "warn" in funcDef:
		descStr += f"""\n<div class="warn-block">\n<h3>Warning</h3>{funcDef["warn"]}</div>"""


	paramsStr = ""
	if len(funcDef["params"]) > 0:
		paramsStr += """<h2>Arguments</h2><div class="arg-block"><ol>"""

	for param in funcDef["params"]:
		paramsStr += f"""<li><span class="span-arg-type">{param["type"]}</span> <span class="span-arg-name">{param["name"]}</span><br><span class="span-arg-desc">{param["desc"]}</span></li>\n"""

	if len(funcDef["params"]) > 0:
		paramsStr += """</ol></div>"""

	returnsStr = ""
	if len(funcDef["returns"]) > 0:
		returnsStr += """<h2>Returns</h2><div class="ret-block"><ol>"""
	
	for ret in funcDef["returns"]:
		returnsStr += f"""<li><span class="span-arg-type">{ret["type"]}</span> <span class="span-arg-name">{ret["name"]}</span><br><span class="span-arg-desc">{ret["desc"]}</span></li>\n"""
	
	if len(funcDef["returns"]) > 0:
		returnsStr += """</ol></div>"""


	examplesStr = ""
	if len(funcDef["examples"]) > 0:
		examplesStr += """<h2>Examples</h2><div class="example-block">"""

	for example in funcDef["examples"]:
		examplesStr += f"""<h3>{example["title"]}</h3>\n<pre style="font-size: 14px;" class="line-numbers"><code class="language-lua">{example["content"]}</code></pre>"""

	if len(funcDef["examples"]) > 0:
		examplesStr += """</div>"""

	return newStr.format(
		funcDef["sig"], # page title
		funcDef["realm"], # realm
		loneFuncStr, # single line func def
		f"{funcDef["src"]}#L{funcDef["line"]}", # path & line
		descStr, # desc
		paramsStr, # params
		returnsStr, # returns
		examplesStr # examples
		)



for funcDef in fileDefs:
	createDirIfNotReal(f"./docs/subpage/{funcDef["group"]}/")
	createDirIfNotReal(f"./docs/subpage/{funcDef["group"]}/{funcDef["category"]}/")

	fPath = f"./docs/subpage/{funcDef["group"]}/{funcDef["category"]}/{funcDef["lonesig"]}.html" 

	with open(fPath, "w") as fPtr:
		fPtr.write(fillTemplate(funcDef))