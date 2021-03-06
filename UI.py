#encoding=utf-8

import sys
#import matplotlib
import numpy as np
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
#import seaborn as sns
from QuantLib import *
import cal as cl

class Calculation(QWidget):
	def __init__(self):
		super(Calculation,self).__init__()

		self.CreateLabel()
		self.CreateEdit()
		self.CreateCombo()
		self.CreateButton()
		self.CreateCalendar()
		self.comboBoxAct()
		self.EditChange()
		self.Linear_parameters=cl.LinearReg()
		self.moment_parameters=cl.moment()
		self.GMM_parameters=cl.GMM()
		self.GC=self.Linear_parameters.GC

		self.initUI()
	def CreateLabel(self):
		self.lblStartDate=QLabel('起始日期',self)
		self.lblEndDate=QLabel('结束日期',self)
		self.lblUnderlyingCode=QLabel('标的代码',self)
		self.lblUnderlyingName=QLabel('标的名称',self)
		self.lblStrike=QLabel('　执行价格',self)
		self.lblUnderlyingPrice=QLabel('　标的现价',self)

		self.lbltradedays=QLabel('交易天数',self)
		self.lblParametersCal=QLabel('参数拟合方法',self)

		self.lblOptionPrice=QLabel('期权价格',self)
		self.lblOptionType=QLabel('期权类型',self)

		#self.lblCalculate=QLabel('开始计算',self)
		#self.lblReCalculate=QLabel('重置',self)
	def CreateButton(self):
		self.btnCalculate=QPushButton('开始计算',self)
		self.btnCalculate.clicked.connect(self.btncalculate)
		self.btnReCalculate=QPushButton('重置',self)
		self.btnReCalculate.clicked.connect(self.btnrecalculate)

		self.btnStartDate=QPushButton('',self)
		self.btnStartDate.clicked.connect(self.btnStartDateChange)

		self.btnEndDate=QPushButton('',self)
		self.btnEndDate.clicked.connect(self.btnEndDateChange)
	def CreateEdit(self):
		self.UnderlyingCodeEdit=QLineEdit(self)
		self.UnderlyingCodeEdit.setText('204001')
		self.UnderlyingNameEdit=QLineEdit(self)
		self.UnderlyingNameEdit.setText('GC001')

		self.tradedaysEdit=QLineEdit(self)
		self.StrikeEdit=QLineEdit(self)

		self.UnderlyingPriceEdit=QLineEdit(self)
		self.OptionPriceEdit=QLineEdit(self)
	def CreateCombo(self):
	

		self.comboType=QComboBox(self)
		self.comboType.addItem('')
		self.comboType.addItem('call')
		self.comboType.addItem('put')

		self.comboCal=QComboBox(self)
		self.comboCal.addItem('')
		self.comboCal.addItem('矩估计')
		self.comboCal.addItem('最小二乘法')
		self.comboCal.addItem('GMM')
		self.comboCal.addItem('贝叶斯估计')
	def CreateCalendar(self):
		self.calStartDate=QCalendarWidget(self)
		self.calStartDate.hide()
		self.calEndDate=QCalendarWidget(self)
		self.calEndDate.hide()
	
	def comboBoxAct(self):

		self.comboType.activated[str].connect(self.onActivatedType)
		self.comboCal.activated[str].connect(self.onActivatedCalibration)
	def EditChange(self):
		self.StrikeEdit.textChanged[str].connect(self.StrikeChange)
	def initUI(self):


		grid=QGridLayout()
		grid.addWidget(self.lblUnderlyingCode,0,0)
		grid.addWidget(self.UnderlyingCodeEdit,0,1)
		grid.addWidget(self.lblStartDate,0,2)
		grid.addWidget(self.btnStartDate,0,3)
		grid.addWidget(self.calStartDate,0,0,3,6)

		grid.addWidget(self.lblUnderlyingPrice,0,4)	
		grid.addWidget(self.UnderlyingPriceEdit,0,5)
		grid.addWidget(self.lblUnderlyingName,1,0)
		grid.addWidget(self.UnderlyingNameEdit,1,1)
		grid.addWidget(self.lblEndDate,1,2)
		grid.addWidget(self.btnEndDate,1,3)
		grid.addWidget(self.calEndDate,0,0,3,6)			
	
		grid.addWidget(self.lblStrike,1,4)
		grid.addWidget(self.StrikeEdit,1,5)
		
		grid.addWidget(self.lblOptionPrice,3,0)
		grid.addWidget(self.OptionPriceEdit,3,1)

		grid.addWidget(self.lbltradedays,2,2)
		grid.addWidget(self.tradedaysEdit,2,3)
		grid.addWidget(self.lblParametersCal,2,4)
		grid.addWidget(self.comboCal,2,5)

		grid.addWidget(self.lblOptionType,2,0)
		grid.addWidget(self.comboType,2,1)		
		
		grid.addWidget(self.btnCalculate,3,4)
		grid.addWidget(self.btnReCalculate,3,5)
		
		vbox=QVBoxLayout()
		vbox.addLayout(grid)
		self.setLayout(vbox)
		
		self.show()
		
		self.setWindowTitle('option calculation')
		self.setGeometry(300,300,500,200)

	def btncalculate(self):
		'''
		parameters=cl.Paras()
		sigma=parameters.sigma[0]
		alpha=parameters.alpha[0]
		mu=parameters.mu[0]
		spot=parameters.GC.iloc[-1][0]

		min_=parameters.min
		optionType=self.OptionType
		strike=self.strike
		china_calendar=China()
		tradedays=china_calendar.businessDaysBetween(self.st_date,self.ed_date)

		ML=cl.Model(alpha,mu,spot,sigma,tradedays,strike,10000,optionType,min_)
		self.OptionPriceEdit.setText(str(ML.price))
		'''
		if self.ParameterCalibration==u'最小二乘法':		
			parameters=self.Linear_parameters
			sigma=parameters.sigma
			alpha=parameters.alpha[0]
			mu=parameters.mu[0]
			print "最小二乘法"
			print "alpha,mu,sigma"
			print alpha,mu,sigma
		elif self.ParameterCalibration==u'矩估计':
			parameters=self.moment_parameters
			sigma=parameters.sigma[0]
			alpha=parameters.alpha[0]
			mu=parameters.mu[0]
			print "矩估计"
			print "alpha,mu,sigma"
			print alpha,mu,sigma
		elif self.ParameterCalibration=='GMM':
			parameters=self.GMM_parameters
			alpha=parameters.res.x[0]
			mu=parameters.res.x[1]
			sigma=parameters.res.x[2]
			print "GMM"
			print "alpha,mu,sigma"
			print alpha,mu,sigma
		elif self.ParameterCalibration==u'贝叶斯估计':
			pass
		else:
			pass
		
		spot=self.spot
		
		optionType=self.OptionType
		strike=self.strike

		tradedays=self.tradedays
		ETD=cl.ETD(alpha,mu,spot,sigma,tradedays,strike,10000,optionType)
		self.OptionPriceEdit.setText(str(round(ETD.price,4)))

		
	def btnrecalculate(self):
		self.OptionPriceEdit.setText(' ')
		self.StrikeEdit.setText(' ')

		self.comboType.clear()
		self.comboType.addItem('')
		self.comboType.addItem('call')
		self.comboType.addItem('put')
		self.comboCal.clear()
		self.comboCal.addItem('')
		self.comboCal.addItem('矩估计')
		self.comboCal.addItem('最小二乘法')
		self.comboCal.addItem('GMM')
		self.comboCal.addItem('贝叶斯估计')

		self.btnStartDate.setText(' ')
		self.btnEndDate.setText(' ')
		self.UnderlyingPriceEdit.setText(' ')
		
		self.tradedaysEdit.clear()
	def btnStartDateChange(self):
		self.calStartDate.show()
		self.calEndDate.hide()
		self.calStartDate.setGridVisible(True)
		#self.calStartDate.resize(2,2)
		self.calStartDate.clicked[QDate].connect(self.showStartDate)
		
	def showStartDate(self,date):
		txt=date.toString()
		year=int(txt[-4:])
		day=int(txt[-7:-5])
		if (txt[3:5][-1]==u'月'):
			month=int(txt[3])
		else:
			month=int(txt[3:5])
		self.st_date=Date(day,month,year)
		
		time=str(year)+'-'+str(month)+'-'+str(day)
		self.spot=self.GC.loc[:time].iloc[-1][0]		
		self.UnderlyingPriceEdit.setText(str(self.spot))
		
		self.btnStartDate.setText(str(year)+'/'+str(month)+'/'+str(day))
		self.calStartDate.hide()
	
	def btnEndDateChange(self):
		self.calEndDate.show()
		self.calStartDate.hide()
		self.calEndDate.setGridVisible(True)
		#self.calEndDate.resize(2,2)
		self.calEndDate.clicked[QDate].connect(self.showEndDate)
		
		
	def showEndDate(self,date):
		txt=date.toString()
		year=int(txt[-4:])
		day=int(txt[-7:-5])
		if (txt[3:5][-1]==u'月'):
			month=int(txt[3])
		else:
			month=int(txt[3:5])
		self.ed_date=Date(day,month,year)
		
		self.btnEndDate.setText(str(year)+'/'+str(month)+'/'+str(day))
		self.calEndDate.hide()

		china_calendar=China()
		self.tradedays=china_calendar.businessDaysBetween(self.st_date,self.ed_date)
		self.tradedaysEdit.setText(str(self.tradedays))
		
	
	def onActivatedType(self,Type):
		self.OptionType=Type
	def onActivatedCalibration(self,Calibration):
		self.ParameterCalibration=Calibration
	def StrikeChange(self,strike):
		if strike==' ':
			pass
		else:
			self.strike=float(strike)

	
if __name__=='__main__':
	#sns.set(color_codes=True)
	app=QApplication(sys.argv)
	ex=Calculation()
	sys.exit(app.exec_())




























