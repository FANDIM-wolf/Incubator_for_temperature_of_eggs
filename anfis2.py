import numpy as np
import csv
import random
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from scipy.interpolate import CubicSpline

from convert import *
from PyQt5 import QtCore, QtGui, QtWidgets
from pprint import pformat

      

import time
from pyfiglet import figlet_format

import sys
from PyQt5.QtCore import pyqtSignal , Qt , QTimer ,  QEventLoop
from PyQt5.QtWidgets import QApplication, QMainWindow , QDialog , QVBoxLayout, QWidget, QSizePolicy , QTableWidgetItem ,  QMessageBox , QLabel , QSplashScreen ,QMessageBox
from PyQt5.QtGui import QMouseEvent , QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from main_window import Ui_MainWindow
    
input1 = ctrl.Antecedent(np.arange(0, 10.28, 0.01), 'input1')
input2 = ctrl.Antecedent(np.arange(38, 64, 0.01), 'input2')
output = ctrl.Consequent(np.arange(36.3, 38, 0.01), 'output')

input1['Q1'] = fuzz.zmf(input1.universe , 0.07443  , 0.3246)
input1['Q2'] = fuzz.gbellmf(input1.universe, 0.146, 2.54, 0.3508)
input1['Q3'] = fuzz.gbellmf(input1.universe, 0.641 , 2.47 , 1.328)
input1['Q4'] = fuzz.gbellmf(input1.universe, 2.58 , 2.5 , 4.558)
input1['Q5'] = fuzz.smf(input1.universe, 4.286 , 9.97)

input2['H1'] = fuzz.smf(input2.universe, 51.55, 62.8)
input2['H2_3'] = fuzz.gbellmf(input2.universe, 8 , 3.01 , 49.56)
input2['H4_5'] = fuzz.zmf(input2.universe, 38.1 , 44.9)



output['T1'] = fuzz.smf(output.universe, 37.58 , 38)
output['T2_3'] = fuzz.gbellmf(output.universe, 0.1717 , 2.61 , 37.6)
output['T4'] = fuzz.gbellmf(output.universe,0.211 , 3 , 37.2)
output['T5'] = fuzz.zmf(output.universe, 36.68 , 37.32)

rule1 = ctrl.Rule(input1['Q1'] & input2['H1'] , output['T1'])
rule2 = ctrl.Rule(input1['Q1'] & input2['H2_3'], output['T2_3'])
rule3 = ctrl.Rule(input1['Q1'] & input2['H4_5'] , output['T4'])
rule4 = ctrl.Rule(input1['Q1'] & input2['H4_5'] , output['T5'])
rule5 = ctrl.Rule(input1['Q2'] & input2['H1'] , output['T1'])
rule6 = ctrl.Rule(input1['Q2'] & input2['H2_3'] , output['T2_3'])
rule7 = ctrl.Rule(input1['Q2'] & input2['H4_5'] , output['T4'])
rule8 = ctrl.Rule(input1['Q2'] & input2['H4_5'] , output['T5'])
rule9 = ctrl.Rule(input1['Q3'] & input2['H1'] , output['T1'])
rule10 = ctrl.Rule(input1['Q3'] & input2['H2_3'] , output['T2_3'])
rule11 = ctrl.Rule(input1['Q3'] & input2['H4_5'] , output['T4'])
rule12 = ctrl.Rule(input1['Q3'] & input2['H4_5'] , output['T5'])
rule13 = ctrl.Rule(input1['Q4'] & input2['H1'] , output['T1'])
rule14 = ctrl.Rule(input1['Q4'] & input2['H2_3'] , output['T2_3'])
rule15 = ctrl.Rule(input1['Q4'] & input2['H4_5'] , output['T4'])
rule16 = ctrl.Rule(input1['Q4'] & input2['H4_5'] , output['T5'])
rule17 = ctrl.Rule(input1['Q5'] & input2['H1'] , output['T1'])
rule18 = ctrl.Rule(input1['Q5'] & input2['H2_3'] , output['T2_3'])
rule19 = ctrl.Rule(input1['Q5'] & input2['H4_5'] , output['T4'])
rule20 = ctrl.Rule(input1['Q5'] & input2['H4_5'] , output['T5'])
anfisctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5,rule6, rule7, rule8, rule9, rule10,
                                rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20])
anfissimulation = ctrl.ControlSystemSimulation(anfisctrl)