import sys, os, time, subprocess, math
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from tkinter import Tk, Canvas, PhotoImage

global mainClass
intro = {}
mainClass = ""

variableCommentsForLines = {}
methodCommentsForReturn = {}
methodCommentsForLines = {}

def checkInput(text, shouldWriteComments):
	if not shouldWriteComments:
		return ""
	inp = input(text)
	if "y" in input("Would you like to change your answer (y/n)? ").lower():
		return checkInput(text, shouldWriteComments)
	return inp

def outputPseudocode(texLines, fileName, shouldWriteComments):
	f = open(fileName)
	print("Loading file " + fileName)

	lines = f.readlines()

	f.close()
	foundIntro = False
	stripped = []

	for line in lines:
		if not foundIntro and line.strip()[:2] == "//":
			foundIntro = True
			intro[fileName.split("/")[1].split(".")[0]] = line.strip()[2:].strip()
		if len(line.strip()) == 0:
			stripped.append(line.strip())
			continue
		if line.strip()[0] == "/" or line.strip()[0] == "*":
			continue
		stripped.append(line.strip().replace("static ", "").replace("final ", ""))

	if not foundIntro:
		intro[fileName.split("/")[1].split(".")[0]] = ""

	finalLines = []

	className = ""

	variables = ""

	variableComments = {}

	variableTypes = []
	methods = []
	
	endStack = []
	pushToStack = ""

	commentedLines = []

	for x in range(len(stripped)):
		line = stripped[x]
		newLine = ""
		if "class" in line:
			newLine = "CLASS " + line.split(" ")[2]
			className = line.split(" ")[2]
			if shouldWriteComments:
				classComment = checkInput("Write a description for the class \"" + className + "\": ", shouldWriteComments)
				commentedLines.append("//" + classComment)
				intro[className] = classComment
			pushToStack = "CLASS"
		elif "public" in line or "protected" in line or "private" in line:
			if ";" in line and "private" in line:
				variables += line[len(str(line.split(" ")[0:2]).replace("', '", "").replace("['", "").replace("']", "")) + 2:]
				parts = line.split(" ")
				for i in range(2, len(parts)):
					variableTypes.append(parts[i].strip()[:-1] + ":" + parts[1])
			elif "{" in line:
				params = "("
				paramTypes = "("
				if not "()" in line:
					parts = line.split("(")[1].split(")")[0].split(" ")
					for i in range(1, len(parts), 2):
						params += parts[i].replace(",", "") + ", "
						paramTypes += parts[i - 1].replace(",", "") + ", "
					if len(params) > 1:
						params = params[:-2] + ")"
						paramTypes = paramTypes[:-2] + ")"
				methodName = line.split(" ")[2].split("(")[0]
				if className in line:
					methodName = className
				if shouldWriteComments:
						if len(variableComments) == 0:
							for var in variables.strip().replace(";", ",").split(","):
								var = var.strip()
								if len(var) == 0:
									continue
								variableComments[var] = checkInput("Write the description for the variable \"" + var + "\" for the class \"" + className + "\": ", shouldWriteComments)
				if params == "(":
					params = ""
					paramTypes = "()"

				newLine = "METHOD " + methodName + params
				returnType = ""
				if shouldWriteComments:
					commentedLines.append("\t/**")

				if methodName == "main":
					global mainClass
					mainClass = className
					if shouldWriteComments:
						commentedLines.append("\t* Java's main method where program execution begins")
						commentedLines.append("\t* args the command line arguments of the program")
						commentedLines.append("\t*/")
				if methodName != className:
					returnType = ":" + line.split(" ")[1]
				elif shouldWriteComments:
					commentedLines.append("\t* The constructor for " + className + " takes in the relevant variables and sets them")
					for variable in params[1:-1].split(", "):
						if not variable in variableComments:
							variable = variable.strip()
							if len(variable) == 0:
								continue
							variableComments[variable] = checkInput("Write the description for the variable \"" + variable + "\" for the class \"" + className + "\": ", shouldWriteComments)
						commentedLines.append("\t* @param " + variable + " " + variableComments[variable])
					
				if shouldWriteComments:
					for variable in variableComments:
						if "get" in line and variable.lower() in line.lower():
							commentedLines.append("\t* Returns the value of the " + variable + " variable")
							commentedLines.append("\t* @return " + variableComments[variable])
							commentedLines.append("\t*/")
						elif "set" in line and variable.lower() in line.lower():
							commentedLines.append("\t* Sets the value of the " + variable + " variable to the value passed in")
							commentedLines.append("\t* @param " + variable + " the new value of the " + variable + " variable")
							commentedLines.append("\t*/")
				
					if commentedLines[-1] == "\t/**":
						methodComment = checkInput("Write a description for this method \"" + methodName + "\" in class \"" + className + "\": ", shouldWriteComments)
						commentedLines.append("\t* " + methodComment)
						methodCommentsForLines[methodName] = methodComment
					if commentedLines[-1] != "\t*/":
						if className != methodName:
							for param in params[1:-1].split(", "):
								commentedLines.append("\t* @param " + param + " " + checkInput("Write a description for this parameter \"" + param + "\" of this method \"" + methodName + "\" in class \"" + className  + "\": ", shouldWriteComments))
						if returnType != "" and returnType != ":void":
							returnInput = checkInput("Write a description of the value this method \"" + methodName + "\" returns in class \"" + className + "\": ", shouldWriteComments)
							commentedLines.append("\t* @return " + returnInput)
							methodCommentsForReturn[methodName] = returnInput
						commentedLines.append("\t*/")
				methods.append(methodName + paramTypes + returnType)
				pushToStack = "METHOD"
		elif line == "}":
				newLine = "END " + endStack[-1]
				endStack = endStack[:-1]
		else:
			if "print" in line:
				newLine = line.replace("System.out.", "").replace("ln(", "(").replace("\")", ")").replace("(\"", "(").replace("\" + ", "\"").replace(" + \"", "\"")
			elif "if " in line:
				newLine = line.replace("if (", "IF ").replace(" else", "ELSE").replace(") {", " THEN").replace("&&", "AND").replace("||", "OR").replace("instanceof", "is an instance of")
				pushToStack = "IF"
				if " else " in line:
					pushToStack = ""
			elif "try " in line:
				newLine = line.replace("try {", "TRY")
				pushToStack = "TRY"
			elif "catch " in line:
				newLine += line.replace("catch (", "CATCH ").replace(") {", "")
				pushToStack = "CATCH"
			elif "while " in line:
				newLine = line.replace("while (", "WHILE ").replace(") {", " DO").replace("&&", "AND").replace("||", "OR")
				pushToStack = "WHILE"
			elif "for " in line:
				if " : " in line:
					newLine = "FOR EACH " + line[len(line.split("(")[0]):].split(" ")[1] + " IN " + line[len(line.split("(")[0]):].split(" ")[3][:-1]
				else:
					newLine = "FOR " + line.split(" ")[2] + " IN RANGE " + line.split(" ")[4][:-1] + " TO " + line.split(";")[1].split(" ")[3]
				pushToStack = "FOR"
			elif " = " in line:
				variableName = ""
				if line.split(" ")[1] == "=":
					variableName = line.split(" ")[0]
				else:
					variableName = line.split(" ")[1]
				newLine = "SET " + variableName.replace("this.", "") + " TO " + line.split(" = ")[1].replace("new ", "")
			elif "++" in line:
				newLine = "SET " + line.split("++")[0] + " TO " + line.split("++")[0] + " + 1"
			elif "--" in line:
				newLine = "SET " + line.split("--")[0] + " TO " + line.split("--")[0] + " - 1"
			elif " -= " in line or " += " in line or " \= " in line or " *= " in line:
				newLine = "SET " + line.split(" ")[0].replace("this.", "") + " TO " + line.split(" ")[0].replace("this.", "") + " " + line.split(" ")[1][:-1] + " " + line.split("= ")[1]
			elif " else {" in line:
				newLine = "ELSE"
			elif "import " in line:
				pass
			else:
				newLine = line
			newLine = newLine.replace("return", "RETURN").replace("-", "minus").replace("/", "divided by").replace("*", "multiplied by").replace("+", "plus").replace("}", "").replace(" > ", " is greater than ").replace(" < ", " is less than ").replace("==", "is equal to").replace("!=", "is not equal to").replace("!", "NOT ").replace("NOT )", "!)")
		if className != "":
			finalLines.append(((len(endStack) - (1 if "ELSE" in newLine else 0)) * "    ") + newLine)
		if pushToStack != "":
			endStack.append(pushToStack)
		pushToStack = ""
		
		if shouldWriteComments:
                	commentedLines.append(lines[x])

	if shouldWriteComments:
		commentedCode = open(fileName.split("/")[0] + "/commented-" + fileName.split("/")[1], "w")
		for l in commentedLines:
			commentedCode.write(l + ("\n" if len(l.strip()) > 0 and (l.strip()[0] == "/" or l.strip()[0] == "*") else ""))
		commentedCode.close()

	while finalLines[0] == "":
		finalLines.remove(finalLines[0])

	texLines += finalLines[0] + "\n"

	if len(variables) > 0:
		texLines += "\n    DEFINE " + variables[:-1].replace(";", ", ") + "\n"

	finalLines.remove(finalLines[0])

	prevNew = False

	for line in finalLines:
		if line.strip() == "":
			if prevNew:
				continue
			else:
				prevNew = True
		else:
			prevNew = False
		texLines += line.replace(";", "") + "\n"

	img = Image.new("RGB", (1, 1), color=(255, 255, 255))
	imgDraw = ImageDraw.Draw(img)
	font = ImageFont.truetype("LiberationSerif-Regular.ttf", 30)

	size = imgDraw.textsize(className, font=font)
	width = size[0]
	height = 10 + size[1]

	classHeight = height + 2

	for var in variableTypes:
		size = imgDraw.textsize(var, font=font)
		if size[0] > width:
			width = size[0]
		height += size[1] + 5
	
	if len(variableTypes) == 0:
		height += 5

	varHeight = height + 2

	height += 7

	for meth in methods:
		size = imgDraw.textsize(meth, font=font)
		if size[0] > width:
			width = size[0]
		height += size[1] + 5
	
	height += 2
	width += 14
	
	img = img.resize((width, height))
	imgDraw = ImageDraw.Draw(img)

	imgDraw.rectangle([0, 0, width - 1, height - 1], outline=(0, 0, 0))
	imgDraw.rectangle([1, 1, width - 2, height - 2], outline=(0, 0, 0))

	imgDraw.line([0, classHeight, width, classHeight], fill=(0, 0, 0))
	imgDraw.line([0, classHeight - 1, width, classHeight - 1], fill=(0, 0, 0))

	imgDraw.line([0, varHeight, width, varHeight], fill=(0, 0, 0))
	imgDraw.line([0, varHeight - 1, width, varHeight - 1], fill=(0, 0, 0))

	imgDraw.text(((width - imgDraw.textsize(className, font=font)[0]) / 2, 7), className, fill=(0, 0, 0), font=font)

	offset = 0

	for var in variableTypes:
		imgDraw.text(((width - imgDraw.textsize(var, font=font)[0]) / 2, classHeight + 2 + offset), var, fill=(0, 0, 0), font=font)
		offset += 5 + imgDraw.textsize(var, font=font)[1]
		
	offset = 0
	for meth in methods:
		imgDraw.text(((width - imgDraw.textsize(meth, font=font)[0]) / 2, varHeight + 2 + offset), meth, fill=(0, 0, 0), font=font)
		offset += 5 + imgDraw.textsize(meth, font=font)[1]

	img.save("PPA-COURSEWORK-" + sys.argv[1] + "/" + name[:-5] + ".gif")
	return texLines

def stepDist(x1, y1, x2, y2, dist):
	diffX = x2 - x1
	diffY = y2 - y1

	diff = math.sqrt(diffX * diffX + diffY * diffY)

	if dist == 0:
		return (x1, y1)

	if dist > diff:
		return (x2, y2)

	return (x1 + diffX * (dist / diff), y1 + diffY * (dist / diff))

def drawLine(imgDraw, x1, y1, x2, y2):
	diffX = x2 - x1
	diffY = y2 - y1
	diff = math.sqrt(diffX * diffX + diffY * diffY)
	dist = 0
	while dist < diff:
		start = stepDist(x1, y1, x2, y2, dist)
		dist += 10
		end = stepDist(x1, y1, x2, y2, dist)
		dist += 10

		imgDraw.line((start[0], start[1], end[0], end[1]), fill=0, width=3)

	if diffY == 0:
		diffY = 0.00001

	shift1 = 60 - math.degrees(math.atan(diffX / diffY))
	shift2 = 120 - math.degrees(math.atan(diffX / diffY))
	changeX1 = math.cos(math.radians(shift1)) * 20
	changeY1 = math.sin(math.radians(shift1)) * 20
	changeX2 = math.cos(math.radians(shift2)) * 20
	changeY2 = math.sin(math.radians(shift2)) * 20
	imgDraw.line((x2 + changeX1 if y2 < y1 else x2 - changeX1, y2 + changeY1 if y2 < y1 else y2 - changeY1, x2, y2), fill=0, width=3)
	imgDraw.line((x2 + changeX2 if y2 < y1 else x2 - changeX2, y2 + changeY2 if y2 < y1 else y2 - changeY2, x2, y2), fill=0, width=3)

def inUsedPoints(usedPoints, point):
	for p in usedPoints:
		if (point[0][0] == p[0][0] and point[0][1] == p[0][1]) or (point[1][0] == p[1][0] and point[1][1] == p[1][1]):
			return True
	return False

def closestToPoint(point, points, usedPoints):
	closest = point
	closestDist = 100000
	for p in points:
		if inUsedPoints(usedPoints, [point, p]):
			continue
		dist = math.sqrt((p[0] - point[0]) * (p[0] - point[0]) + (p[1] - point[1]) * (p[1] - point[1]))
		if dist < closestDist:
			closestDist = dist
			closest = p
	return closest

def placeClassDiagrams(classes, compositionPairs, dependencyPairs, assignmentNo):
	root = Tk()
	
	global canv, clas, currentClass, running, classObjects

	canv = Canvas(root, highlightthickness=0)
	canv.pack(fill='both', expand=True)

	classObjects = {}
	classImages = {}
	dependencyLines = []
	compositionLines = []

	clas = classes

	for cla in clas:
		classImages[cla] = PhotoImage(file="PPA-COURSEWORK-" + assignmentNo + "/" + cla + ".gif").subsample(2, 2)
		classObjects[cla] = canv.create_image((0, 0), image=classImages[cla])

	currentClass = classObjects[clas[0]]

	running = True

	def genLines(imgDraw=None, xOff=0, yOff=0):
		usedPoints = []
		for line in dependencyLines:
			canv.delete(line)
		for line in compositionLines:
			canv.delete(line)
		for dependency in dependencyPairs:
			x1, y1 = canv.coords(classObjects[dependency[0]])
			w1, h1 = classImages[dependency[0]].width(), classImages[dependency[0]].height()
			x2, y2 = canv.coords(classObjects[dependency[1]])
			w2, h2 = classImages[dependency[1]].width(), classImages[dependency[1]].height()
			points1 = [(x1 - w1 / 2, y1 - h1 / 2), (x1, y1 - h1 / 2), (x1 + w1 / 2, y1 - h1 / 2), (x1 - w1 / 2, y1), (x1 + w1 / 2, y1), (x1 - w1 / 2, y1 + h1 / 2), (x1, y1 + h1 / 2), (x1 + w1 / 2, y1 + h1 / 2)]
			points2 = [(x2 - w2 / 2, y2 - h2 / 2), (x2, y2 - h2 / 2), (x2 + w2 / 2, y2 - h2 / 2), (x2 - w2 / 2, y2), (x2 + w2 / 2, y2), (x2 - w2 / 2, y2 + h2 / 2), (x2, y2 + h2 / 2), (x2 + w2 / 2, y2 + h2 / 2)]
			
			shortest = 10000
			shortestPoints = []

			for point1 in points1:
				point2 = closestToPoint(point1, points2, usedPoints)
				shortDist = math.sqrt((point1[0] - point2[0]) * (point1[0] - point2[0]) + (point1[1] - point2[1]) * (point1[1] - point2[1]))
				if inUsedPoints(usedPoints, [point1, point2]):
					continue	

				if shortDist < shortest:
					shortest = shortDist
					shortestPoints = [point1, point2]

			usedPoints.append(shortestPoints)

			x1, y1, x2, y2 = shortestPoints[0][0], shortestPoints[0][1], shortestPoints[1][0], shortestPoints[1][1]

			if imgDraw == None:
				dependencyLines.append(canv.create_line(x1, y1, x2, y2, arrow="last", dash=(5)))
			else:
				drawLine(imgDraw, (x1 - xOff) * 2, (y1 - yOff) * 2, (x2 - xOff) * 2, (y2 - yOff) * 2)

		for composition in compositionPairs:
			x1, y1 = canv.coords(classObjects[composition[0]])
			w1, h1 = classImages[composition[0]].width(), classImages[composition[0]].height()
			x2, y2 = canv.coords(classObjects[composition[1]])
			w2, h2 = classImages[composition[1]].width(), classImages[composition[1]].height()
			points1 = [(x1 - w1 / 2, y1 - h1 / 2), (x1, y1 - h1 / 2), (x1 + w1 / 2, y1 - h1 / 2), (x1 - w1 / 2, y1), (x1 + w1 / 2, y1), (x1 - w1 / 2, y1 + h1 / 2), (x1, y1 + h1 / 2), (x1 + w1 / 2, y1 + h1 / 2)]
			points2 = [(x2 - w2 / 2, y2 - h2 / 2), (x2, y2 - h2 / 2), (x2 + w2 / 2, y2 - h2 / 2), (x2 - w2 / 2, y2), (x2 + w2 / 2, y2), (x2 - w2 / 2, y2 + h2 / 2), (x2, y2 + h2 / 2), (x2 + w2 / 2, y2 + h2 / 2)]

			shortest = 10000
			shortestPoints = []

			for point1 in points1:
				point2 = closestToPoint(point1, points2, usedPoints)
				shortDist = math.sqrt((point1[0] - point2[0]) * (point1[0] - point2[0]) + (point1[1] - point2[1]) * (point1[1] - point2[1]))

				if inUsedPoints(usedPoints, [point1, point2]):
					continue

				if shortDist < shortest:
					shortest = shortDist
					shortestPoints = [point1, point2]

			usedPoints.append(shortestPoints)

			x1, y1, x2, y2 = shortestPoints[0][0], shortestPoints[0][1], shortestPoints[1][0], shortestPoints[1][1]

			if imgDraw == None:
				compositionLines.append(canv.create_line(x1, y1, x2, y2, arrow="last"))
			else:
				drawLine(imgDraw, (x1 - xOff) * 2, (y1 - yOff) * 2, (x2 - xOff) * 2, (y2 - yOff) * 2)

	def outputKey(event):
		if event.char == '1' or event.char == '2' or event.char == '3' or event.char == '4' or event.char == '5' or event.char == '6' or event.char == '7' or event.char == '8' or event.char == '9':
			select(int(event.char) - 1)
		elif event.char == '0':
			select(9)

	def moveRight(event):
		global currentClass
		if currentClass != None:
			canv.move(currentClass, 1, 0)
			genLines()

	def moveLeft(event):
		global currentClass
		if currentClass != None:
			canv.move(currentClass, -1, 0)
			genLines()

	def moveUp(event):
		global currentClass
		if currentClass != None:
			canv.move(currentClass, 0, -1)
			genLines()

	def moveDown(event):
		global currentClass
		if currentClass != None:
			canv.move(currentClass, 0, 1)
			genLines()

	global pastX, pastY

	pastX = 0
	pastY = 0

	def grabClass(event):
		for cla in clas:
			if event.x > canv.coords(classObjects[cla])[0] - classImages[cla].width() / 2 and event.x < canv.coords(classObjects[cla])[0] + classImages[cla].width() / 2:
				if event.y > canv.coords(classObjects[cla])[1] - classImages[cla].height() / 2 and event.y < canv.coords(classObjects[cla])[1] + classImages[cla].height() / 2:
					global currentClass, pastX, pastY
					currentClass = classObjects[cla]
					pastX = event.x
					pastY = event.y

	def moveClass(event):
		if currentClass != None:
			global pastX, pastY
			diffX = event.x - pastX
			diffY = event.y - pastY
			pastX = event.x
			pastY = event.y
			canv.move(currentClass, diffX, diffY)
		genLines()

	def dropClass(event):
		global currentClass
		currentClass = None

	def stopCanvasKey(event):
		stopCanvas()

	def stopCanvas():
		global running, clas
		running = False
		maxWidth = 0
		maxHeight = 0
		xOff = 1000
		yOff = 1000
		for cla in clas:
			tx, ty = canv.coords(classObjects[cla])
			tw, th = classImages[cla].width(), classImages[cla].height()
			if tx - tw / 2 < xOff:
				xOff = tx - tw / 2
			if ty - th / 2 < yOff:
				yOff = ty - th / 2
			
			if tx + tw / 2 > maxWidth:
				maxWidth = tx + tw / 2
			if ty + th / 2 > maxHeight:
				maxHeight = ty + th / 2
		maxWidth -= xOff
		maxHeight -= yOff
		maxHeight *= 2
		maxWidth *= 2
		img = Image.new("RGB", (int(maxWidth), int(maxHeight)), (255, 255, 255))
		
		imageLocs = {}
		cImages = {}
		for cla in clas:
			imageLoc = canv.coords(classObjects[cla])
			cImages[cla] = Image.open("PPA-COURSEWORK-" + assignmentNo + "/" + cla + ".gif")
			img.paste(cImages[cla], (int((imageLoc[0] - xOff) * 2) - int(cImages[cla].width / 2), int((imageLoc[1] - yOff) * 2) - int(cImages[cla].height / 2)))

		imgDraw = ImageDraw.Draw(img)
		
		genLines(imgDraw, xOff, yOff)

		img.save("PPA-COURSEWORK-" + assignmentNo + "/classDiagram.png")
		
		if maxWidth > 600:
			runCommand("convert -size 600x PPA-COURSEWORK-" + assignmentNo + "/classDiagram.png PPA-COURSEWORK-" + assignmentNo + "/classDiagramSmall.png")

		if maxHeight > 600:
			runCommand("convert -size x600 PPA-COURSEWORK-" + assignmentNo + "/classDiagram.png PPA-COURSEWORK-" + assignmentNo + "/classDiagramSmall.png")


		root.destroy()
		
	def select(i):
		if len(classes) > i:
			global currentClass
			currentClass = classObjects[clas[i]]

	root.bind("<Right>", moveRight)
	root.bind("<Left>", moveLeft)
	root.bind("<Up>", moveUp)
	root.bind("<Down>", moveDown)
	root.bind("<Escape>", stopCanvasKey)
	root.bind("<Button-1>", grabClass)
	root.bind("<B1-Motion>", moveClass)
	root.bind("<ButtonRelease-1>", dropClass)
	root.bind("<Key>", outputKey)
	
	root.protocol("WM_DELETE_WINDOW", stopCanvas)

	root.geometry('%sx%s+%s+%s' %(600, 600, 100, 100))

	while running:
		time.sleep(0.001)
		canv.update()

	root.mainloop()

def runCommand(command):
	proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()

if len(sys.argv) > 1:
	shouldWriteComments = len(sys.argv) > 2 and sys.argv[2].lower() == "y"
	shouldPlaceClassDiagrams = len(sys.argv) > 3 and sys.argv[3].lower() == "y"
	shouldWriteDescription = len(sys.argv) > 4 and sys.argv[4].lower() == "y"
	
	texLines = "\\documentclass{article}\n\\usepackage[margin=0.5in]{geometry}\n\\usepackage{graphicx}\n\\usepackage{listings}\n\\begin{document}\n\n\\title{Assignment " + sys.argv[1] + "}\n\\author{Joshua Bradbury, Msci Computer Science, K1631175}\n\\date{<<DATE>>}\n\n\\maketitle\n\n\\section{Introduction}\n\n<<INTRODUCTION>>\n\n\\section{Pseudocode}\n\n\\lstset{breaklines=true,keepspaces=true,columns=flexible}\n\\begin{lstlisting}\n".replace("<<DATE>>", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][datetime.today().month - 1] + " " + str(datetime.today().day) + ", " + str(datetime.today().year))
	
	dependencyPairs = []
	compositionPairs = []
	classNames = []

	for name in os.listdir("PPA-COURSEWORK-" + sys.argv[1]):
		if name[-5:] == ".java" and not "commented" in name:
			classNames.append(name[:-5])

	for name in os.listdir("PPA-COURSEWORK-" + sys.argv[1]):
		if name[-5:] == ".java" and not "commented" in name:
			f = open("PPA-COURSEWORK-" + sys.argv[1] +"/" + name, "r")
			for line in f.readlines():
				for className in classNames:
					dependency = [name[:-5], className]
					if className + " " in line and not name[:-5] == className in line and not dependency in dependencyPairs and not dependency in compositionPairs:
						if not "private" in line:
							dependencyPairs.append(dependency)
						else:
							compositionPairs.append(dependency)
			f.close()
			texLines = outputPseudocode(texLines, "PPA-COURSEWORK-" + sys.argv[1] +"/" + name, shouldWriteComments)
	if not shouldWriteComments:
		for name in os.listdir("PPA-COURSEWORK-" + sys.argv[1]):
			if name[-5:] == ".java" and "commented" in name:
				commentedFile = open("PPA-COURSEWORK-" + sys.argv[1] + "/" + name, "r")
				lin = commentedFile.readlines()
				introLine = ""
				for l in lin:
					if "//" in l.strip():
						introLine = l.strip()[2:]
						break
				intro[name.split(".")[0].split("-")[1]] = introLine
	firstLine = "The task was to create " + str(len(intro)) + " classes called, "
	mainText = intro[mainClass]
	classes = list(intro.keys())
	del intro[mainClass]
	for key in intro:
		firstLine += key + ", "
	introText = firstLine[:-2] + " and " + mainClass + ". "
	for key in intro:
		introText += intro[key] + ". "
	introText += mainText + "."
	texLines = texLines.replace("<<INTRODUCTION>>", introText)

	if shouldPlaceClassDiagrams:
		placeClassDiagrams(classes, compositionPairs, dependencyPairs, sys.argv[1])

	description = ""

	for doc in os.listdir("PPA-COURSEWORK-" + sys.argv[1]):
		if doc == "description.txt":
			docFile = open("PPA-COURSEWORK-" + sys.argv[1] + "/description.txt", "r")
			description = docFile.readline()
			docFile.close()
	
	if shouldWriteDescription or (description == "" and shouldWriteDescription):
		description = checkInput("What would you like to be the description: ", True)
		docFile = open("PPA-COURSEWORK-" + sys.argv[1] + "/description.txt", "w")
		docFile.write(description)

	texLines += "\\end{lstlisting}\n\\section{Class Diagram}\n\\includegraphics[scale=0.4]{classDiagram}\n\n\\section{Description}\n" + description + "\n\n\\end{document}"

	f = open("PPA-COURSEWORK-" + sys.argv[1] + "/Documentation.tex", "w")
	f.write(texLines)
	f.close()

	classList = []

	for name in os.listdir("PPA-COURSEWORK-" + sys.argv[1]):
		if name[-5:] == ".java" and not "commented" in name:
			runCommand("cd PPA-COURSEWORK-" + sys.argv[1] + " && mv " + name + " backup-" + name + " && cp commented-" + name + " " + name)
			classList.append(name)
	
	runCommand("cd PPA-COURSEWORK-" + sys.argv[1] + " && zip Coursework.zip " + str(classList).replace("[", "").replace("]", "").replace(",", ""))

	for className in classList:
		runCommand("cd PPA-COURSEWORK-" + sys.argv[1] + " && mv backup-" + className + " " + className)

	runCommand("cd PPA-COURSEWORK-" + sys.argv[1] + " && pdflatex Documentation.tex && google-chrome Documentation.pdf")
