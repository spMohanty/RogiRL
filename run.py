#!/usr/bin/env python

# -------------------- IMPORTS --------------------

import pygame
import random
from enum import Enum
from pygame.locals import *

pygame.init()

# -------------------- CONSTANTS --------------------

#targetFrameRate = 60

bgCol = pygame.Color(0, 0, 0)
liveCellCol = pygame.Color(32, 200, 32)
deadCellCol = pygame.Color(16, 16, 16)
separatorCol = pygame.Color(255, 255, 255)
textCol = pygame.Color(255, 255, 255)
redTextCol = pygame.Color(255, 32, 32)
yellowTextCol = pygame.Color(255, 255, 32)
greenTextCol = pygame.Color(32, 255, 32)
blueTextCol = pygame.Color(64, 64, 255)
boundingBoxCol = pygame.Color(200, 200, 32)
mousePosCol = pygame.Color(200, 200, 200)

topBarSizeY = 26
leftBarSize = 8*25

controlsSectionOffsetY = 94

topTextPadding = 4
leftTextPadding = 4

numCellsX = 80
numCellsY = 60
sizeCellsX = 10
sizeCellsY = 10

sizeX = numCellsX*sizeCellsX + leftBarSize
sizeY = numCellsY*sizeCellsY + topBarSizeY

# -------------------- VARIABLES --------------------

class UpdateMode(Enum):
     SIMPLE = 1
     BOUNDING = 2
     ACTIVE = 3

cells = [[[0 for col in range(numCellsX)]for row in range(numCellsY)] for i in range(2)]
liveCells = [[(-1, -1) for pos in range(numCellsX*numCellsY)] for i in range(2)]
cellIsProcessed = [[False for col in range(numCellsX)]for row in range(numCellsY)]

numberOfNeighbors = 0
numberOfGenerations = 0
numberOfMemoryAccesses = 0

currentLiveCellIndex = 0
currentBuffer = 0
otherBuffer = 1 - currentBuffer
currentMode = UpdateMode.SIMPLE

boundingBoxMinX = 0
boundingBoxMaxX = numCellsX - 1
boundingBoxMinY = 0
boundingBoxMaxY = numCellsY - 1

mousePos = (-1, -1)
mouseLeftClicked = False
mouseRightClicked = False

didChangeCellValue = False
isFullyStillLife = False
displayPrevIteration = True
separateCells = True
needToPopulateLiveCellList = True
step = False
paused = True
done = False

# -------------------- INITIALIZATION / OBJECT CREATION --------------------

clock = pygame.time.Clock()
pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION])
pygame.display.set_caption('Mohanty - Disease Simulation')
screen = pygame.display.set_mode((sizeX, sizeY))

font = pygame.font.SysFont("consolas", 20)
smallFont = pygame.font.SysFont("consolas", 12)
fontHeight = font.get_height()
smallFontHeight = smallFont.get_height()

statusHeadingText = font.render("Status", True, textCol, bgCol)
controlsHeadingText = font.render("Controls", True, textCol, bgCol)
runningText = font.render("RUNNING", True, greenTextCol, bgCol)
stepText = font.render("STEP", True, greenTextCol, bgCol)
pausedText = font.render("PAUSED", True, yellowTextCol, bgCol)
numberOfGenerationsLabelText = smallFont.render("# of steps:", True, textCol, bgCol)
timePerGenerationLabelText = smallFont.render("Time/step:", True, textCol, bgCol)
generationsPerSecondLabelText = smallFont.render("steps/second:", True, textCol, bgCol)
updateTimeUnitText = smallFont.render("ms", True, textCol, bgCol)
updateFPSUnitText = smallFont.render("g/s", True, textCol, bgCol)
memAccessStringText = smallFont.render("# of mem. accesses:", True, textCol, bgCol)

controlsStrings = [ "[Enter] = Step",
					"[Space] = Run/Pause", 
					"[MMB]   = Run/Pause",
					"[LMB]   = Set cells",
					"[RMB]   = Clear cells",
					"[M]     = Change mode",
					"[S]     = Toggle separation",
					"[P]     = Toggle prev state",
					"[C]     = Clear all",
					"[G]     = Gosper glider gun",
					"[g]     = Glider pattern",
					"[R]     = Random pattern",
					"[ESC]   = Quit"]

# controlsTexts = [smallFont.render(currentControlsString, True, textCol, bgCol) for currentControlsString in controlsStrings]

# -------------------- FUNCTIONS --------------------

# Clamp number within range function
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

	
# Create glider (on both buffers) function
def createGlider(col, row, ori):

	global cells
	
	for i in range (0, 2):
		if ori == 0: # Facing left
			cells[i][row+0][col+1] = 1
			cells[i][row+1][col+2] = 1
			cells[i][row+2][col+0] = 1
			cells[i][row+2][col+1] = 1
			cells[i][row+2][col+2] = 1
			
		if ori == 1: # Facing right
			cells[i][row+0][col+1] = 1
			cells[i][row+1][col+0] = 1
			cells[i][row+2][col+0] = 1
			cells[i][row+2][col+1] = 1
			cells[i][row+2][col+2] = 1	
		
def initBoardGosperGliderGun(col, row):
	
	global cells
	
	clearCells()
	
	for i in range (0, 2):
		cells[i][row+5][col+1] = 1
		cells[i][row+5][col+2] = 1
		cells[i][row+6][col+1] = 1
		cells[i][row+6][col+2] = 1
		cells[i][row+5][col+11] = 1
		cells[i][row+6][col+11] = 1
		cells[i][row+7][col+11] = 1
		cells[i][row+4][col+12] = 1
		cells[i][row+3][col+13] = 1
		cells[i][row+3][col+14] = 1
		cells[i][row+8][col+12] = 1
		cells[i][row+9][col+13] = 1
		cells[i][row+9][col+14] = 1
		cells[i][row+6][col+15] = 1
		cells[i][row+4][col+16] = 1
		cells[i][row+5][col+17] = 1
		cells[i][row+6][col+17] = 1
		cells[i][row+7][col+17] = 1
		cells[i][row+6][col+18] = 1
		cells[i][row+8][col+16] = 1
		cells[i][row+3][col+21] = 1
		cells[i][row+4][col+21] = 1
		cells[i][row+5][col+21] = 1
		cells[i][row+3][col+22] = 1
		cells[i][row+4][col+22] = 1
		cells[i][row+5][col+22] = 1
		cells[i][row+2][col+23] = 1
		cells[i][row+6][col+23] = 1
		cells[i][row+1][col+25] = 1
		cells[i][row+2][col+25] = 1
		cells[i][row+6][col+25] = 1
		cells[i][row+7][col+25] = 1
		cells[i][row+3][col+35] = 1
		cells[i][row+4][col+35] = 1
		cells[i][row+3][col+36] = 1
		cells[i][row+4][col+36] = 1
		
		cells[i][row+27][col+41] = 1
		cells[i][row+27][col+42] = 1
		cells[i][row+28][col+41] = 1
		cells[i][row+28][col+43] = 1
		cells[i][row+29][col+43] = 1
		cells[i][row+30][col+43] = 1
		cells[i][row+30][col+44] = 1
	
# Initialize board (with 2 gliders) function
def initBoardGliders():
	
	clearCells()
	createGlider(1, 1, 0)
	createGlider((40 - 4), 2, 1)

	
# Initialize board (randomly) function
def initBoardRandom():

	global cells

	clearCells()
	
	for row in range(numCellsY-1, -1, -1):
		for col in range(numCellsX-1, -1, -1):
			for i in range (0, 2):
				cells[i][row][col] = random.randint(0, 1)
			

# Clear all cells (from both buffers) function
def clearCells():

	global cells
	global numberOfGenerations
	global needToPopulateLiveCellList
	global isFullyStillLife
	global currentBuffer
	
	currentBuffer = 0
	numberOfGenerations = 0
	needToPopulateLiveCellList = True
	isFullyStillLife = False
	#print("[Clear] Set isFullyStillLife to: " + str(isFullyStillLife))
	
	for row in range(numCellsY-1, -1, -1):
		for col in range(numCellsX-1, -1, -1):
			for i in range (0, 2):
				cells[i][row][col] = 0


# Cell drawing function
def drawCell(col, row):
	
	#print("Drawing cell at col: %d, row: %d, i: %d" % (col, row, i))

	if cells[currentBuffer][row][col]: color = liveCellCol
	else: color = deadCellCol
	if separateCells:
		pygame.draw.rect(screen, color, pygame.Rect(leftBarSize + col*sizeCellsX + 1, topBarSizeY + row*sizeCellsY + 1, sizeCellsX-2, sizeCellsY-2))
	else:
		pygame.draw.rect(screen, color, pygame.Rect(leftBarSize + col*sizeCellsX, topBarSizeY + row*sizeCellsY, sizeCellsX, sizeCellsY))

	if displayPrevIteration and cells[otherBuffer][row][col]: 
		color = yellowTextCol
		pygame.draw.rect(screen, color, pygame.Rect(leftBarSize + col*sizeCellsX + 4, topBarSizeY + row*sizeCellsY + 4, sizeCellsX-8, sizeCellsY-8))
	

# Process drawing function
def processCell(col, row, idle):

	global cells
	global liveCells
	global numberOfMemoryAccesses
	global currentLiveCellIndex 
	global didChangeCellValue		
	
	if not isFullyStillLife:
	
		minX = clamp((col-1), 0, (numCellsX-1))
		maxX = clamp((col+1), 0, (numCellsX-1))
		minY = clamp((row-1), 0, (numCellsY-1))
		maxY = clamp((row+1), 0, (numCellsY-1))
		
		neighborCount = 0
		thisCellIsAlive = cells[otherBuffer][row][col]
		numberOfMemoryAccesses += 1
		
		for currY in range(minY, maxY+1):
			for currX in range(minX, maxX+1):
				#print("Reading cell at col: %d, row: %d, buff: %d" % (col, row, otherBuffer))
				neighborCount += cells[otherBuffer][currY][currX]
				numberOfMemoryAccesses += 1
	
		neighborCount -= cells[otherBuffer][row][col]
		numberOfMemoryAccesses += 1
		
		#if thisCellIsAlive:
			#pygame.draw.rect(screen, boundingBoxCol, pygame.Rect(minX*sizeCellsX, topBarSizeY + minY*sizeCellsY, (maxX - minX + 1) * sizeCellsX, (maxY - minY + 1) * sizeCellsY), 1)
			#pygame.display.flip()
			
		if not idle:
			if thisCellIsAlive and neighborCount < 2:
				cells[currentBuffer][row][col] = 0
				didChangeCellValue = True
				#print("A cell was changed!")
			elif thisCellIsAlive and neighborCount > 3:
				cells[currentBuffer][row][col] = 0
				didChangeCellValue = True
				#print("A cell was changed!")
			elif not thisCellIsAlive and neighborCount == 3:
				cells[currentBuffer][row][col] = 1
				didChangeCellValue = True
				#print("A cell was changed!")
			else:
				cells[currentBuffer][row][col] = cells[otherBuffer][row][col]
		
		if currentMode == UpdateMode.ACTIVE and cells[currentBuffer][row][col]:
			liveCells[currentBuffer][currentLiveCellIndex] = (col, row)
			currentLiveCellIndex += 1
			numberOfMemoryAccesses += 2
	

# Calculate bounding box (based on prev. alive cells) function
def calculateBoundingBox():

	global boundingBoxMinX
	global boundingBoxMaxX
	global boundingBoxMinY
	global boundingBoxMaxY
	global numberOfMemoryAccesses

	currMinX = numCellsX - 1
	currMaxX = 0
	currMinY = numCellsY - 1
	currMaxY = 0

	for row in range(numCellsY-1, -1, -1):
		for col in range(numCellsX-1, -1, -1):
			if cells[otherBuffer][row][col]:
				currMinX = min(currMinX, col)
				currMaxX = max(currMaxX, col)
				currMinY = min(currMinY, row)
				currMaxY = max(currMaxY, row)
			numberOfMemoryAccesses += 1
	
	boundingBoxMinX = clamp(currMinX - 2, 0, (numCellsX-1))
	boundingBoxMaxX = clamp(currMaxX + 2, 0, (numCellsX-1))
	boundingBoxMinY = clamp(currMinY - 2, 0, (numCellsY-1))
	boundingBoxMaxY = clamp(currMaxY + 2, 0, (numCellsY-1))
	
	#print("Calculated bounding box: (%d, %d, %d, %d)" % (boundingBoxMinX, boundingBoxMinY, boundingBoxMaxX, boundingBoxMaxY))
	

# Populate the live cell list function
def populateLiveCellList():

	global liveCells
	global numberOfMemoryAccesses

	pos = 0
	for row in range(numCellsY-1, -1, -1):
		for col in range(numCellsX-1, -1, -1):
			if cells[currentBuffer][row][col]:
				for i in range (0, 2):
					liveCells[i][pos] = (col, row)
				pos += 1
			numberOfMemoryAccesses += 3
	
	for i in range (0, 2):
		liveCells[i][pos] = (-1, -1)

	print("Found %d live cells" % (pos))
	for currentLiveIndex in range(0, numCellsX*numCellsY):
			currentLiveX = (liveCells[currentBuffer][currentLiveIndex])[0]
			currentLiveY = (liveCells[currentBuffer][currentLiveIndex])[1]
			if currentLiveX != -1 and currentLiveY != -1:
				print("%d, %d" % (currentLiveX, currentLiveY))
			else:
				break

# Process the neighbors of the current live cell (ignoring duplicates) function
def processLiveCellNeighbors(col, row):

	global cellIsProcessed
	global numberOfMemoryAccesses
	global numberOfNeighbors
	
	minX = clamp((col-1), 0, (numCellsX-1))
	maxX = clamp((col+1), 0, (numCellsX-1))
	minY = clamp((row-1), 0, (numCellsY-1))
	maxY = clamp((row+1), 0, (numCellsY-1))
	
	#print("Will process all neighbor cells within : ((%d, %d), (%d, %d))" % (minX, minY, maxX, maxY))
	
	for currY in range(minY, maxY+1):
		for currX in range(minX, maxX+1):
			if not cellIsProcessed[currY][currX]:
				
				pygame.draw.rect(screen, blueTextCol, pygame.Rect(leftBarSize + currX*sizeCellsX, topBarSizeY + currY*sizeCellsY, sizeCellsX, sizeCellsY), 1)
				#pygame.display.flip()			# Update the screen
				#pygame.time.wait(5)
				
				numberOfNeighbors += 1
				
				if not paused or step:
					processCell(currX, currY, False)
				else:
					processCell(currX, currY, True)
				cellIsProcessed[currY][currX] = True
				numberOfMemoryAccesses += 1
			numberOfMemoryAccesses += 1
			
# Update board function
def updateBoard():
	
	global cells
	global liveCells
	global cellIsProcessed
	global numberOfMemoryAccesses
	global numberOfGenerations
	global needToPopulateLiveCellList
	global currentLiveCellIndex
	global numberOfNeighbors
	global didChangeCellValue
	global isFullyStillLife
	
	didChangeCellValue = False
	
	if not paused or step:
		numberOfGenerations += 1

	if currentMode == UpdateMode.SIMPLE:
		# Loop over all cells, updating (if not paused or if stepping)
		for row in range(numCellsY-1, -1, -1):
			for col in range(numCellsX-1, -1, -1):
				if not paused or step:
					processCell(col, row, False)
				else:
					processCell(col, row, True)
				numberOfMemoryAccesses += 1
				
	elif currentMode == UpdateMode.BOUNDING:
		# Loop over all cells within bounding box, updating (if not paused or if stepping)
		for row in range(boundingBoxMaxY, boundingBoxMinY-1, -1):
			for col in range(boundingBoxMaxX, boundingBoxMinX-1, -1):
				if not paused or step:
					processCell(col, row, False)
				else:
					processCell(col, row, True)
				numberOfMemoryAccesses += 1
				
		if not isFullyStillLife:
			calculateBoundingBox()
		
	elif currentMode == UpdateMode.ACTIVE:
		if needToPopulateLiveCellList:
			print("Populating live cell list...")
			populateLiveCellList()
			needToPopulateLiveCellList = False
		
		currentLiveCellIndex = 0
		numberOfNeighbors = 0
		numberOfLiveCells = 0
		
		# Process the neighbors around each live cell
		for currentLiveIndex in range(0, numCellsX*numCellsY):
			currentLiveX = (liveCells[otherBuffer][currentLiveIndex])[0]
			currentLiveY = (liveCells[otherBuffer][currentLiveIndex])[1]
			if currentLiveX != -1 and currentLiveY != -1:
				processLiveCellNeighbors(currentLiveX, currentLiveY)
				pygame.draw.rect(screen, redTextCol, pygame.Rect(leftBarSize + currentLiveX*sizeCellsX, topBarSizeY + currentLiveY*sizeCellsY, sizeCellsX, sizeCellsY), 1)
				numberOfLiveCells += 1
			else:
				break
		
		liveCells[otherBuffer][currentLiveCellIndex] = (-1, -1)
		
		#print("Live cells: %d, Neighbors: %d" % (numberOfLiveCells, numberOfNeighbors))

		# Loop over all cells, drawing each one
		for row in range(numCellsY-1, -1, -1):
			for col in range(numCellsX-1, -1, -1):
				cellIsProcessed[row][col] = False
				numberOfMemoryAccesses += 1
				
		#print(liveCells)
		
	isFullyStillLife = not didChangeCellValue
	#print("[Update] Set isFullyStillLife to: " + str(isFullyStillLife))

	
def displayBoard():

	# Loop over all cells, drawing each one
	for row in range(numCellsY-1, -1, -1):
		for col in range(numCellsX-1, -1, -1):
			drawCell(col, row)
	
	if currentMode == UpdateMode.BOUNDING:
		# Draw the bounding box
		pygame.draw.rect(screen, boundingBoxCol, pygame.Rect(leftBarSize + boundingBoxMinX*sizeCellsX, topBarSizeY + boundingBoxMinY*sizeCellsY, (boundingBoxMaxX - boundingBoxMinX + 1) * sizeCellsX, (boundingBoxMaxY - boundingBoxMinY + 1) * sizeCellsY), 1)
		
	
def processMouseInput():

	global needToPopulateLiveCellList
	global isFullyStillLife

	# Loop over all cells, drawing each one
	for row in range(numCellsY-1, -1, -1):
		for col in range(numCellsX-1, -1, -1):
		
			cellBorderRect = pygame.Rect(leftBarSize + col*sizeCellsX, topBarSizeY + row*sizeCellsY, sizeCellsX, sizeCellsY)
			if cellBorderRect.collidepoint(mousePos):
				pygame.draw.rect(screen, mousePosCol, cellBorderRect, 1)
				
				if mouseLeftClicked:
					for i in range (0, 2):
						cells[i][row][col] = 1
					needToPopulateLiveCellList = True
					isFullyStillLife = False
					#print("[Mouse] Set isFullyStillLife to: " + str(isFullyStillLife))
						
				if mouseRightClicked:
					for i in range (0, 2):
						cells[i][row][col] = 0
					needToPopulateLiveCellList = True
					isFullyStillLife = False
					#print("[Mouse] Set isFullyStillLife to: " + str(isFullyStillLife))


# -------------------- INITIALIZE BOARD --------------------
	
# Initialize the board to be empty
#clearCells()
	
# Initialize the board with 2 gliders facing each other
#initBoardGliders()

# Initialize the board with a Gosper glider gun in the top left corner
# initBoardGosperGliderGun(0, 0)

# Initialize the board randomly
initBoardRandom()

#populateLiveCellList()
#print(liveCells)

# -------------------- MAIN LOOP --------------------

while not done:

	# -------------------- EVENT HANDLING --------------------

	for event in pygame.event.get():
		# Check to exit
		if event.type == QUIT:
			done = True
		# Check keyboard input
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				done = True
			if event.key == K_SPACE:
				paused = not paused
				isFullyStillLife = False
				#print("[Main] Set isFullyStillLife to: " + str(isFullyStillLife))
			if event.key == K_RETURN:
				isFullyStillLife = False
				paused = True
				step = True
			if event.key == K_c:
				paused = True
				clearCells()
			if event.key == K_g:
				if pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]:
					initBoardGosperGliderGun(0, 0)
				else:
					initBoardGliders()
			if event.key == K_r:
				initBoardRandom()
			if event.key == K_s:
				separateCells = not separateCells
			if event.key == K_p:
				displayPrevIteration = not displayPrevIteration
			if event.key == K_m:
				if currentMode == UpdateMode.SIMPLE: 
					currentMode = UpdateMode.BOUNDING
					calculateBoundingBox()
				elif currentMode == UpdateMode.BOUNDING:
					currentMode = UpdateMode.ACTIVE
				elif currentMode == UpdateMode.ACTIVE: currentMode = UpdateMode.SIMPLE
		# Check mouse down input
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1: # Left button down
				paused = True
				mouseLeftClicked = True
			if event.button == 2: # Mouse wheel button down
				paused = not paused
				isFullyStillLife = False
				#print("[Main] Set isFullyStillLife to: " + str(isFullyStillLife))
			elif event.button == 3: # Right button down
				paused = True
				mouseRightClicked = True
		# Check for mouse up input
		if event.type == MOUSEBUTTONUP:
			if event.button == 1: # Left button up
				mouseLeftClicked = False
			elif event.button == 3: # Right button up
				mouseRightClicked = False    
		# Get the mouse position	
		if event.type == MOUSEMOTION:
			mousePos = event.pos
	
	# -------------------- UPDATE FRAME --------------------
	
	# Clear the screen
	screen.fill(bgCol)
	
	if not paused or step:
		# Swap buffers
		otherBuffer = currentBuffer
		currentBuffer = 1 - currentBuffer
		
	# -------------------- SIMULATION LOGIC / MOUSE INPUT --------------------
	
	# Start timing
	startUpdateTime = pygame.time.get_ticks()
	
	# Update the board using the method based on the current mode
	updateBoard()
	
	# Draw the cells 
	displayBoard()
	
	# Stop Timing
	updateTime = pygame.time.get_ticks() - startUpdateTime
	
	# Draw the mouse position and set/clear cells with mouse
	processMouseInput()
	
	# -------------------- MODE & RUN STATUS INDICATORS --------------------
	
	# Draw current mode text
	if currentMode == UpdateMode.SIMPLE: currentModeString = "Simple"
	elif currentMode == UpdateMode.BOUNDING: currentModeString = "Bounding Box"
	elif currentMode == UpdateMode.ACTIVE: currentModeString = "Active Cells"
	currentModeText = font.render("Mode: " + currentModeString, True, textCol, bgCol)
	screen.blit(currentModeText, (leftBarSize + leftTextPadding, topTextPadding))
	
	if not paused:
		# Draw running text
		screen.blit(runningText, ((sizeX + leftBarSize - runningText.get_width()) // 2, topTextPadding))
		
	if step:
		# Draw step text
		screen.blit(stepText, ((sizeX + leftBarSize - stepText.get_width()) // 2, topTextPadding))

	if paused and not step:
		# Draw paused text
		screen.blit(pausedText, ((sizeX + leftBarSize - pausedText.get_width()) // 2, topTextPadding))
		
	# -------------------- LEFT BAR SEPARATOR --------------------
	
	# Draw left bar separator
	pygame.draw.line(screen, separatorCol, (leftBarSize-1, 0), (leftBarSize-1, sizeY), 1)
	
	# -------------------- STATUS INFO TEXTS --------------------
	
	# Draw status heading text
	screen.blit(statusHeadingText, (leftTextPadding, topTextPadding))
	
	# Draw number of generations text
	numberOfGenerationsValueText = smallFont.render(str(numberOfGenerations), True, textCol, bgCol)
	screen.blit(numberOfGenerationsLabelText, (leftTextPadding, topBarSizeY + topTextPadding))
	screen.blit(numberOfGenerationsValueText, (leftBarSize - numberOfGenerationsValueText.get_width() - leftTextPadding, topBarSizeY + topTextPadding))	
	
	# Set generation timing color
	timeTextCol = redTextCol
	if updateTime < 1:
		updateFPS = 999
		timeTextCol = greenTextCol
	else:
		updateFPS = (1000 // updateTime)
		if updateFPS >= 10:	timeTextCol = yellowTextCol
		if updateFPS >= 20:	timeTextCol = greenTextCol
	
	# Draw time per generation text
	timePerGenerationValueText = smallFont.render(str(updateTime), True, timeTextCol, bgCol)
	screen.blit(timePerGenerationLabelText, (leftTextPadding, topBarSizeY + topTextPadding + smallFontHeight))
	screen.blit(updateTimeUnitText, (leftBarSize - updateTimeUnitText.get_width() - leftTextPadding, topBarSizeY + topTextPadding + smallFontHeight))
	screen.blit(timePerGenerationValueText, (leftBarSize - timePerGenerationValueText.get_width() - updateTimeUnitText.get_width() - leftTextPadding, topBarSizeY + topTextPadding + smallFontHeight))
	
	# Draw generations per second text
	generationsPerSecondValueText = smallFont.render(str(updateFPS), True, timeTextCol, bgCol)
	screen.blit(generationsPerSecondLabelText, (leftTextPadding, topBarSizeY + topTextPadding + smallFontHeight*2))
	screen.blit(updateFPSUnitText, (leftBarSize - updateFPSUnitText.get_width() - leftTextPadding, topBarSizeY + topTextPadding + smallFontHeight*2))
	screen.blit(generationsPerSecondValueText, (leftBarSize - generationsPerSecondValueText.get_width() - updateFPSUnitText.get_width() - leftTextPadding, topBarSizeY + topTextPadding + smallFontHeight*2))
	
	# Draw current number of memory accesses text
	memAccessValueText = smallFont.render(str(numberOfMemoryAccesses), True, blueTextCol, bgCol)
	screen.blit(memAccessStringText, (leftTextPadding, topBarSizeY + topTextPadding + smallFontHeight*3))
	screen.blit(memAccessValueText, (leftBarSize - memAccessValueText.get_width() - leftTextPadding, topBarSizeY + topTextPadding + smallFontHeight*3))
	
	# -------------------- CONTROLS TEXTS --------------------
	
	# Draw controls texts separator
	pygame.draw.line(screen, separatorCol, (0, controlsSectionOffsetY), (leftBarSize - 1, controlsSectionOffsetY), 1)	
	
	# Draw controls heading text
	screen.blit(controlsHeadingText, (leftTextPadding, controlsSectionOffsetY + topTextPadding))
	
	# Draw bottom key controls text
	# for	curerntControlTextIndex in range (0, len(controlsTexts)):
	# 	screen.blit(controlsTexts[curerntControlTextIndex], (leftTextPadding, controlsSectionOffsetY + topBarSizeY + topTextPadding + curerntControlTextIndex*smallFontHeight))
	
	# -------------------- UPDATE SCREEN --------------------
	
	pygame.display.flip()			# Update the screen
	#clock.tick(targetFrameRate)	# Don't pause, update screen as fast as possible
	#if currentMode == UpdateMode.ACTIVE:
	#	clock.tick(0.2)
	
	# -------------------- RESET VARIABLES --------------------
	
	step = False					# Step only once
	numberOfMemoryAccesses = 0		# Reset memory access to 0