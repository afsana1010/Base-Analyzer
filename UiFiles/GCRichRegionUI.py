"""
Tools Name : Base Analyzer Tool
Original Developer: Afsana Rahman Snigdha
Original Development Date : 01-01-2012
Version : 1.0
Purpose : Draw the GC Count window and import GCRichRegion file to perform its functional part
"""

#!/usr/bin/python -d
import pdb
import os 
import sys
import fileinput
import math
import re
import csv
import webbrowser
from PyQt4 import QtCore, QtGui
from FunctionalFiles.GCRichRegion import GCRichRegion


class GCRichRegionUI(QtGui.QDialog):

	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		
#create a lebel	
		self.label_input_file=QtGui.QLabel(self)
		self.label_input_file.setText('Select a file of fasta sequence')
		self.label_input_file.setGeometry(QtCore.QRect(35,40,200,24))
		self.label_input_file.move(35, 40)
		self.label_input_file.show()
		
#create a lineedit		
		self.input_file_browse = QtGui.QLineEdit(self)
		self.input_file_browse.move(35, 70)
		self.input_file_browse.setGeometry(QtCore.QRect(35, 70,335,28))
		self.input_file_browse.setEnabled(False)
		self.input_file_browse.show()
		
#create a button		
		self.input_file_browse_button = QtGui.QPushButton('Browse', self)
		self.input_file_browse_button.move(270, 100)
		self.input_file_browse_button.setGeometry(QtCore.QRect(270, 100,100,28))
		self.input_file_browse_button.show()
		self.input_file_browse_button.clicked.connect(self.inputFile)

#create a lebel		
		self.label_percentage_gc=QtGui.QLabel(self)
		self.label_percentage_gc.setText('Considerable GC %')
		self.label_percentage_gc.setGeometry(QtCore.QRect(35, 130,200,24))
		self.label_percentage_gc.move(35, 130)
		self.label_percentage_gc.show()		

#create a combobox
		self.combo_percentage_gc=QtGui.QComboBox(self)
		self.combo_percentage_gc.insertItem(0,'--select--')
		self.combo_percentage_gc.insertItem(1,'60')
		self.combo_percentage_gc.insertItem(2,'70')
		self.combo_percentage_gc.insertItem(3,'80')
		self.combo_percentage_gc.insertItem(4,'90')
		self.combo_percentage_gc.setGeometry(QtCore.QRect(170, 130,80,24))
		self.combo_percentage_gc.move(170, 130)
		self.combo_percentage_gc.show()
		self.combo_percentage_gc.activated[str].connect(self.gcPercetageCombo)
		
#create a lebel				
		self.label_output_file=QtGui.QLabel(self)
		self.label_output_file.setText('Save File To ')
		self.label_output_file.setGeometry(QtCore.QRect(35, 160,200,24))
		self.label_output_file.move(35, 160)
		self.label_output_file.show()

#create a line edit			
		self.file_browse = QtGui.QLineEdit(self)
		self.file_browse.move(35, 190)
		self.file_browse.setGeometry(QtCore.QRect(35,190,335,28))
		self.file_browse.setEnabled(False)
		self.file_browse.show()

#create a button			
		self.browse_button = QtGui.QPushButton('Browse', self)
		self.browse_button.move(270, 220)
		self.browse_button.setGeometry(QtCore.QRect(270, 220,100,28))
		self.browse_button.show()
		self.browse_button.clicked.connect(self.outputFile)

#create a button		
		self.save_button = QtGui.QPushButton('Save', self)
		self.save_button.move(150, 330)
		self.save_button.setGeometry(QtCore.QRect(150, 330,100,28))
		self.save_button.show()
		self.save_button.clicked.connect(self.saveFile)

#create a button		
		self.close_button = QtGui.QPushButton('Close', self)
		self.close_button.move(270, 330)
		self.close_button.setGeometry(QtCore.QRect(270,330,100,28))
		self.close_button.show()
		self.close_button.clicked.connect(self.close)

#create a window		
		self.setFixedSize(400,400)
		self.setGeometry(450, 250,160, 150)
		self.setWindowTitle('GC Rich Region')
		self.setModal(True)
		
		self.sourcefile = ""
		self.updated_file_name = ""
		self.percentage_of_gc = "--select--"

#function to get the value of gc percentage combo
	def gcPercetageCombo(self, text):
		self.percentage_of_gc = text
		
#function to perform writing the output file		
	def saveFile(self):
		if str(self.sourcefile)== "":
			self.msgBox=QtGui.QMessageBox()
			self.msgBox.setWindowTitle("!!!!!!!!!Warnings!!!!!!!!!")
			self.msgBox.setText("Please select a input file")
			self.msgBox.move(500, 330)
			self.msgBox.exec_()
			
		if str(self.updated_file_name)== "":
			self.msgBox=QtGui.QMessageBox()
			self.msgBox.setWindowTitle("!!!!!!!!!Warnings!!!!!!!!!")
			self.msgBox.setText("Please give a output file")
			self.msgBox.move(500, 330)
			self.msgBox.exec_()				

		if str(self.percentage_of_gc)== "--select--":
			self.msgBox=QtGui.QMessageBox()
			self.msgBox.setWindowTitle("!!!!!!!!!Warnings!!!!!!!!!")
			self.msgBox.setText("Please select GC percentage")
			self.msgBox.move(500, 330)
			self.msgBox.exec_()
		
		if str(self.sourcefile)!= ""  and str(self.updated_file_name)!= "" and str(self.percentage_of_gc)!= "--select--":
			self.W = GCRichRegion()
			gcrich = self.W.GCRichRegion(self.sourcefile,self.updated_file_name,self.percentage_of_gc);
			if str(gcrich) == "yes":
				self.msgBox=QtGui.QMessageBox()
				self.msgBox.setWindowTitle("             Success Message             ")
				self.msgBox.setText("Result file save successfully.")
				self.msgBox.move(500, 330)
				ret = self.msgBox.exec_()
				if ret :
					self.close()
					self.input_file_browse.setText("")
					self.file_browse.setText("")
					webbrowser.open(self.updated_file_name)
										
			elif str(gcrich) != "yes":
				self.msgBox=QtGui.QMessageBox()
				self.msgBox.setWindowTitle("!!!!!!!!!Warnings!!!!!!!!!")
				self.msgBox.setText(str(gcrich))
				self.msgBox.move(500, 330)
				self.msgBox.exec_()
				self.input_file_browse.setText("")
				self.file_browse.setText("")
				
#function to take the output file name from user			
	def outputFile(self):								
		output_file_name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '/home',"HTML Files (*.html)")
		if(int(str(output_file_name).find(".")) != -1) and str(output_file_name) !="":
			self.updated_file_name=output_file_name[0:int(str(output_file_name).find("."))] +".html"
			self.file_browse.setText(str(self.updated_file_name));
		elif str(output_file_name) !="":
			self.updated_file_name=output_file_name +".html"
			self.file_browse.setText(str(self.updated_file_name))
			 			
#function to take the input file name from user					
	def inputFile(self):
		self.sourcefile = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home',"Text Files (*.txt)")
		file_size = os.path.getsize(self.sourcefile)
		if file_size > 1073741824:
			self.msgBox=QtGui.QMessageBox()
			self.msgBox.setWindowTitle("!!!!!!!!!Warnings!!!!!!!!!")
			self.msgBox.setText("Input file is too Large.")
			self.msgBox.move(500, 330)
			ret = self.msgBox.exec_()
		elif file_size < 1073741824:	
			self.input_file_browse.setText(str(self.sourcefile))
		
