# -*- coding: utf-8 -*-

# Inspection tool for FreeCAD macro development.
# Author: Darek L (aka dprojects)
# Version: 2.5
# Latest version: https://github.com/dprojects/scanObjects

import FreeCAD
from PySide import QtGui, QtCore


# ############################################################################
# Qt Main
# ############################################################################
	

def showQtGUI():
	
	class QtMainClass(QtGui.QDialog):
		
		# ############################################################################
		# database
		# ############################################################################

		# database for selection
		dbSO = [] # objects
		dbSL = [] # labels
		dbSI = -1 # index
		dbSP = [] # path
		dbSLI = [] # last index

		# globals
		gDefaultRoot = ""
		gPalette = ""
		gW = 1200 # width
		gH = 600 # hight

		# ############################################################################
		# init
		# ############################################################################

		def __init__(self):
			super(QtMainClass, self).__init__()
			self.initUI()

		def initUI(self):

			# set default 
			try:
				test = FreeCAD.activeDocument().Objects
				self.gDefaultRoot = "project"
			except:
				self.gDefaultRoot = "FreeCAD"

			# window
			self.result = userCancelled
			self.setGeometry(10, 10, self.gW, self.gH)
			self.setWindowTitle("scanObjects - inspection tool for macro development")
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

			# ############################################################################
			# selection view
			# ############################################################################

			self.list = QtGui.QListView()
			self.listsw = QtGui.QMdiSubWindow(self)
			self.listsw.setWindowTitle("Select object:")
			self.listsw.setGeometry(0, 0, 180, 430)
			self.listsw.setWidget(self.list)

			# ############################################################################
			# select root path
			# ############################################################################

			# label
			self.rootL = QtGui.QLabel("Select root path:", self)
			self.rootL.move(10, 440)
			
			# options
			self.rootList = (
				"my project root",
				"FreeCAD", 
				"QtGui", 
				"QtCore", 
				"Path", 
				"Draft", 
				"TechDraw", 
				"Spreadsheet"
			)

			self.rootO = QtGui.QComboBox(self)
			self.rootO.addItems(self.rootList)
			if self.gDefaultRoot == "project":
				self.rootO.setCurrentIndex(self.rootList.index("my project root"))
			else:
				self.rootO.setCurrentIndex(self.rootList.index("FreeCAD"))
			self.rootO.activated[str].connect(self.setRootPath)
			self.rootO.move(10, 460)

			# ############################################################################
			# custom module
			# ############################################################################

			# label
			self.rootCL = QtGui.QLabel("Custom module:", self)
			self.rootCL.move(10, 490)

			# text input
			self.rootCO = QtGui.QLineEdit(self)
			self.rootCO.setText("")
			self.rootCO.setFixedWidth(70)
			self.rootCO.move(10, 510)
			
			# button
			self.rootCLoad = QtGui.QPushButton("load", self)
			self.rootCLoad.clicked.connect(self.loadCustomModule)
			self.rootCLoad.move(85, 510)

			# ############################################################################
			# select windows layout
			# ############################################################################

			# label
			self.layL = QtGui.QLabel("Select windows layout:", self)
			self.layL.move(10, 540)
			
			# options
			self.layList = (
				"all windows",
				"modules",
				"content", 
				"docs", 
				"array",
				"matrix red pill",
				"matrix blue pill",
			)

			self.layO = QtGui.QComboBox(self)
			self.layO.addItems(self.layList)
			self.layO.setCurrentIndex(self.layList.index("all windows"))
			self.layO.activated[str].connect(self.setWindowsLayout)
			self.layO.move(10, 560)

			# ############################################################################
			# output 1
			# ############################################################################

			self.o1 = QtGui.QTextEdit()
			self.o1sw = QtGui.QMdiSubWindow(self)
			self.o1sw.setWindowTitle("dir(): & Help Window")
			self.o1sw.setGeometry(180, 0, 260, 430)
			self.o1sw.setWidget(self.o1)

			# ############################################################################
			# output 2
			# ############################################################################
			
			self.o2 = QtGui.QTextEdit()
			self.o2sw = QtGui.QMdiSubWindow(self)
			self.o2sw.setWindowTitle("__dict__:")
			self.o2sw.setGeometry(440, 0, 220, 430)
			self.o2sw.setWidget(self.o2)
			
			# ############################################################################
			# output 3
			# ############################################################################

			self.o3 = QtGui.QTextEdit()
			self.o3sw = QtGui.QMdiSubWindow(self)
			self.o3sw.setWindowTitle("__doc__:")
			self.o3sw.setGeometry(660, 0, 320, 150)
			self.o3sw.setWidget(self.o3)

			# ############################################################################
			# output 4
			# ############################################################################

			self.o4 = QtGui.QTextEdit()
			self.o4sw = QtGui.QMdiSubWindow(self)
			self.o4sw.setWindowTitle("getAllDerivedFrom():")
			self.o4sw.setGeometry(660, 230, 320, 100)
			self.o4sw.setWidget(self.o4)

			# ############################################################################
			# output 5
			# ############################################################################

			self.o5 = QtGui.QTextEdit()
			self.o5sw = QtGui.QMdiSubWindow(self)
			self.o5sw.setWindowTitle("Content & Error Console:")
			self.o5sw.setGeometry(180, 430, 1020, 170)
			self.o5sw.setWidget(self.o5)

			# ############################################################################
			# output 6
			# ############################################################################

			self.o6 = QtGui.QTextEdit()
			self.o6sw = QtGui.QMdiSubWindow(self)
			self.o6sw.setWindowTitle("<class 'str'>:")
			self.o6sw.setGeometry(660, 330, 540, 100)
			self.o6sw.setWidget(self.o6)

			# ############################################################################
			# output 7
			# ############################################################################

			self.o7 = QtGui.QTextEdit()
			self.o7sw = QtGui.QMdiSubWindow(self)
			self.o7sw.setWindowTitle("<class 'float'>:")
			self.o7sw.setGeometry(660, 150, 320, 80)
			self.o7sw.setWidget(self.o7)

			# ############################################################################
			# output 8
			# ############################################################################

			self.o8 = QtGui.QTextEdit()
			self.o8sw = QtGui.QMdiSubWindow(self)
			self.o8sw.setWindowTitle("<class 'list'>:")
			self.o8sw.setGeometry(980, 0, 220, 330)
			self.o8sw.setWidget(self.o8)

			# ############################################################################
			# keyboard keys
			# ############################################################################

			QtGui.QShortcut(QtGui.QKeySequence("left"), self, self.keyLeft)
			QtGui.QShortcut(QtGui.QKeySequence("right"), self, self.keyRight)

			# ############################################################################
			# show
			# ############################################################################

			# init default selection db
			if self.gDefaultRoot == "project":
				self.setRootPath("my project root")
			else:
				self.setRootPath("FreeCAD")

			self.show()

			# save colors
			self.gPalette = self.palette()
		
		# ############################################################################
		# functions
		# ############################################################################

		def setWindowsLayout(self, selectedText):

			if selectedText == "all windows":
				self.listsw.setGeometry(0, 0, 180, 430)
				self.listsw.show()
				self.list.show()
				self.o1sw.setGeometry(180, 0, 260, 430)
				self.o1sw.show()
				self.o1.show()
				self.o2sw.setGeometry(440, 0, 220, 430)
				self.o2sw.show()
				self.o2.show()
				self.o3sw.setGeometry(660, 0, 320, 150)
				self.o3sw.show()
				self.o3.show()
				self.o4sw.setGeometry(660, 230, 320, 100)
				self.o4sw.show()
				self.o4.show()
				self.o5sw.setGeometry(180, 430, 1020, 170)
				self.o5sw.show()
				self.o5.show()
				self.o6sw.setGeometry(660, 330, 540, 100)
				self.o6sw.show()
				self.o6.show()
				self.o7sw.setGeometry(660, 150, 320, 80)
				self.o7sw.show()
				self.o7.show()
				self.o8sw.setGeometry(980, 0, 220, 330)
				self.o8sw.show()
				self.o8.show()

			if selectedText == "modules":
				self.listsw.setGeometry(0, 0, 260, 430)
				self.listsw.show()
				self.list.show()
				self.o1sw.setGeometry(260, 0, 260, 500)
				self.o1sw.show()
				self.o1.show()
				self.o2sw.setGeometry(520, 0, 220, 500)
				self.o2sw.show()
				self.o2.show()
				self.o3sw.setGeometry(740, 0, 460, 500)
				self.o3sw.show()
				self.o3.show()

				self.o4sw.hide()
				self.o4.hide()

				self.o5sw.setGeometry(260, 500, 940, 100)
				self.o5sw.show()
				self.o5.show()

				self.o6sw.hide()
				self.o6.hide()
				self.o7sw.hide()
				self.o7.hide()
				self.o8sw.hide()
				self.o8.hide()

			if selectedText == "content":
				self.listsw.setGeometry(0, 0, 180, 430)
				self.listsw.show()
				self.list.show()

				self.o1sw.hide()
				self.o1.hide()
				self.o2sw.hide()
				self.o2.hide()
				self.o3sw.hide()
				self.o3.hide()
				self.o4sw.hide()
				self.o4.hide()

				self.o5sw.setGeometry(180, 0, 1020, 600)
				self.o5sw.show()
				self.o5.show()

				self.o6sw.hide()
				self.o6.hide()
				self.o7sw.hide()
				self.o7.hide()
				self.o8sw.hide()
				self.o8.hide()

			if selectedText == "docs":
				self.listsw.setGeometry(0, 0, 180, 430)
				self.listsw.show()
				self.list.show()

				self.o1sw.hide()
				self.o1.hide()
				self.o2sw.hide()
				self.o2.hide()

				self.o3sw.setGeometry(180, 0, 1020, 600)
				self.o3sw.show()
				self.o3.show()

				self.o4sw.hide()
				self.o4.hide()
				self.o5sw.hide()
				self.o5.hide()
				self.o6sw.hide()
				self.o6.hide()
				self.o7sw.hide()
				self.o7.hide()
				self.o8sw.hide()
				self.o8.hide()

			if selectedText == "array":
				self.listsw.setGeometry(0, 0, 180, 430)
				self.listsw.show()
				self.list.show()

				self.o1sw.hide()
				self.o1.hide()
				self.o2sw.hide()
				self.o2.hide()
				self.o3sw.hide()
				self.o3.hide()
				self.o4sw.hide()
				self.o4.hide()
				self.o5sw.hide()
				self.o5.hide()
				self.o6sw.hide()
				self.o6.hide()
				self.o7sw.hide()
				self.o7.hide()

				self.o8sw.setGeometry(180, 0, 1020, 600)
				self.o8sw.show()
				self.o8.show()

			if selectedText == "matrix red pill":
				p = QtGui.QPalette()
				p.setColor(p.Base, QtGui.QColor(0, 0, 0))
				p.setColor(p.Text, QtGui.QColor(0, 255, 0))
				self.setPalette(p)

			if selectedText == "matrix blue pill":
				self.setPalette(self.gPalette)

		def showError(self, iError):
		
			try:
				e = ""
				e += "ERROR: "
				e += " | "
				e += str(iError)

				self.o5.setPlainText(e)
			except:
				self.o5.setPlainText("kernel panic or even FreeCAD panic :-)")
				
		def clearDB(self):

			# database for selection
			self.dbSO = [] # objects
			self.dbSL = [] # labels
			self.dbSI = -1 # index
			self.dbSP = [] # path
			self.dbSLI = [] # last index

		def setRootPath(self, selectedText):

			# clear db before root set
			self.clearDB()

			if selectedText == "my project root":
					
				try:
					root = FreeCAD.activeDocument().Objects
					rootS= "FreeCAD.activeDocument().Objects"
					self.addSelection("", root, rootS, -1)
				except:
					self.showError("You have to set active document (project) to use this root path.")

			if selectedText == "FreeCAD":

				root = dir(FreeCAD)
				rootS= "FreeCAD"
				self.addSelection(FreeCAD, root, rootS, -1)

			if selectedText == "QtGui":

				from PySide import QtGui

				root = dir(QtGui)
				rootS= "QtGui"
				self.addSelection(QtGui, root, rootS, -1)

			if selectedText == "QtCore":

				from PySide import QtCore

				root = dir(QtCore)
				rootS= "QtCore"
				self.addSelection(QtCore, root, rootS, -1)

			if selectedText == "Path":

				import Path

				root = dir(Path)
				rootS= "Path"
				self.addSelection(Path, root, rootS, -1)

			if selectedText == "Draft":

				import Draft

				root = dir(Draft)
				rootS= "Draft"
				self.addSelection(Draft, root, rootS, -1)

			if selectedText == "TechDraw":

				import TechDraw

				root = dir(TechDraw)
				rootS= "TechDraw"
				self.addSelection(TechDraw, root, rootS, -1)

			if selectedText == "Spreadsheet":

				import Spreadsheet

				root = dir(Spreadsheet)
				rootS= "Spreadsheet"
				self.addSelection(Spreadsheet, root, rootS, -1)

		def loadCustomModule(self):

			try:
				rootS = str(self.rootCO.text())
				module = __import__(rootS, globals(), locals(), [], 0)
				root = dir(module)

				# clear db before root set
				self.clearDB()
				
				self.addSelection(module, root, rootS, -1)

			except:
				self.showError("Can't load module: "+rootS)
				
		def setOutput(self, iObj):

			index = iObj.indexes()[0].row()

			# ########################################				
			# output 1
			# ########################################

			skip = 0

			try:
				result = dir(self.dbSO[self.dbSI][index])
			except:
				skip = 1

			try:
				if skip == 0:

					o1 = ""
					for row in result:
						o1 += row + "\n"
					
					self.o1.setPlainText(o1)
				else:
					self.o1.setPlainText("")
			except:
				skip = 1

			# ########################################				
			# output 2
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index].__dict__
			except:
				skip = 1

			try:
				if skip == 0:

					o2 = ""
					for row in result:
						o2 += row + "\n"
					
					self.o2.setPlainText(o2)
				else:
					self.o2.setPlainText("")
			except:
				skip = 1

			# ########################################				
			# output 3
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index].__doc__
			except:
				skip = 1

			try:
				if skip == 0:
					self.o3.setPlainText(result)
				else:
					self.o3.setPlainText("")
			except:
				skip = 1

			# ########################################				
			# output 4
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index].getAllDerivedFrom()
			except:
				skip = 1

			try:
				if skip == 0:

					o4 = ""
					for row in result:
						o4 += row + "\n"
					
					self.o4.setPlainText(o4)
				else:
					self.o4.setPlainText("")
			except:
				skip = 1

			# ########################################				
			# output 5
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index].Content
			except:
				skip = 1

			try:
				if skip == 0:
					self.o5.setPlainText(result)
				else:
					self.o5.setPlainText("")
			except:
				skip = 1

			# ########################################				
			# output 6
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index]
			except:
				skip = 1

			try:
				if skip == 0 and isinstance(result, str):
					self.o6.setPlainText(str(result))
				else:
					self.o6.setPlainText("")
			except:
				skip = 1

			# ########################################				
			# output 7
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index]
			except:
				skip = 1

			try:
				if skip == 0 and isinstance(result, float):
					self.o7.setPlainText(str(result))
				else:
					self.o7.setPlainText("")
			except:
				skip = 1

			# ########################################				
			# output 8
			# ########################################

			skip = 0

			try:
				result = self.dbSO[self.dbSI][index]
			except:
				skip = 1

			try:
				if skip == 0 and isinstance(result, list):

					o8 = ""
					for row in result:
						o8 += str(row) + "\n"
					
					self.o8.setPlainText(o8)
				else:
					self.o8.setPlainText("")
			except:
				skip = 1
	
		def getSelectionPath(self):

			path = ""
			for item in self.dbSP:
				path += "." + item + "\n"

			return str(path)[1:]

		def resetOutputs(self):

			path = self.getSelectionPath()

			info = ""
			info += "Your current selection path is:"
			info += "\n\n"
			info += path
			info += "\n\n\n"
			info += "Usage:"
			info += "\n"
			info += "→ \t | go deeper"
			info += "\n"
			info += "← \t | go back"
			info += "\n"
			info += "↑ ↓ \t | select object"
			info += "\n\n"
			info += "Use ↑ ↓ arrow keys to select object and start inspection at this path."

			self.o1.setPlainText(info)
			self.o2.setPlainText("")
			self.o3.setPlainText("")
			self.o4.setPlainText("")
			self.o5.setPlainText("")
			self.o6.setPlainText("")
			self.o7.setPlainText("")
			self.o8.setPlainText("")

		def updateSelection(self):

			model = QtGui.QStandardItemModel(self.list)
			
			for o in self.dbSL[self.dbSI]:
				item = QtGui.QStandardItem(str(o))
				model.appendRow(item)
				self.list.setModel(model)

			self.list.selectionModel().selectionChanged.connect(self.setOutput)
			self.resetOutputs()

		def removeSelection(self):

			# stop remove if there is only init objects list
			if self.dbSI > 0:

				self.dbSO.pop()
				self.dbSL.pop()
				self.dbSP.pop()
				self.dbSI = self.dbSI - 1

				self.updateSelection()

			# set last selected
			try:

				# select item
				item = self.dbSLI[self.dbSI]
				flag = QtCore.QItemSelectionModel.Select
				self.list.selectionModel().setCurrentIndex(item, flag)

				# scroll to item
				flag = QtGui.QAbstractItemView.EnsureVisible.PositionAtCenter
				self.list.scrollTo(item, flag)

			except:
				skip = 1

			# remove last selected
			if self.dbSI > 0:
				self.dbSLI.pop()

			self.resetOutputs()

		def addSelection(self, iObj, iList, iPath, iSelected):

			tmpO = []
			tmpL = []

			# init selection view
			if iObj == "":
				tmpO = iList
				tmpL = [ o.Label for o in tmpO ]

			# if object is list (eg. faces, edges)
			elif isinstance(iObj, list):

				tmpO = iObj
				tmpL = iObj

			# all objects types
			else:

				for o in iList:
					try:
						if hasattr(iObj, o):
							tmpO.append(getattr(iObj, o))
							tmpL.append(str(o))
					except:
						skip = 1

			# not add empty lists (this stuck)
			if len(tmpO) > 0 and len(tmpL) > 0:

				# update db
				self.dbSO.append(tmpO)
				self.dbSL.append(tmpL)
				self.dbSP.append(iPath)

				# not select at init
				if iSelected != -1:
					self.dbSLI.insert(self.dbSI, iSelected)

				self.dbSI = self.dbSI + 1

				# update selection list
				self.updateSelection()

		# ############################################################################
		# actions for keyboard keys
		# ############################################################################

		def keyLeft(self):
			self.removeSelection()

		def keyRight(self):

			try:
				selected = self.list.currentIndex()
				index = selected.row()
				Obj = self.dbSO[self.dbSI][index]
				path = str(self.dbSL[self.dbSI][index])
				
				if isinstance(Obj, str):
					skip = 1
				elif isinstance(Obj, float):
					skip = 1
				elif isinstance(Obj, list):
					newList = Obj
					self.addSelection(Obj, newList, path, selected)
				else:
					newList = dir(Obj)
					self.addSelection(Obj, newList, path, selected)
			except:
				skip = 1
	
	# ############################################################################
	# final settings
	# ############################################################################

	userCancelled = "Cancelled"
	userOK = "OK"
	
	form = QtMainClass()
	form.exec_()
	
	if form.result == userCancelled:
		pass

# ###################################################################################################################
# MAIN
# ###################################################################################################################


showQtGUI()


# ###################################################################################################################
